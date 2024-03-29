from flask import Blueprint, Response, render_template, request, session, current_app

from src.blueprints.format_data import format_items
from src.blueprints.auth import login_required
from src.blueprints.database import connect_db
from src.blueprints.decode_keyword import decode_keyword, escape
from src.blueprints.exceptions import ItemNotFoundError, ExistingItemError, OngoingRequestItemError, SelfNotFoundError, SelfRoleError

bp_inventory = Blueprint('bp_inventory', __name__, url_prefix = "/inventory")

# route for inventory
@bp_inventory.route('/')
def inventory ():
    return render_template("inventory/inventory.html", active = "inventory")

# route for item search
@bp_inventory.route('/search')
def search_items ():
    keywords = [] if "keywords" not in request.args else [decode_keyword(x).lower() for x in request.args.get("keywords").split(" ")]
    conditions = []
    for x in keywords:
        conditions.append(f"(ItemID LIKE '%{x}%' OR ItemName LIKE '%{x}%' OR Category LIKE '%{x}%' OR ItemDescription LIKE '%{x}%')")
    query = f"SELECT * from stock {'' if len(conditions) == 0 else 'WHERE (' + ' AND '.join(conditions) + ')'} ORDER BY ItemID"

    cxn = None
    try:
        cxn = connect_db()
        db = cxn.cursor()
        db.execute(query)
        items = db.fetchall()
    except Exception as e:
        current_app.logger.error(str(e))
        return { "error": str(e) }, 500
    finally:
        if cxn is not None: cxn.close()

    return { "items": format_items(items) }

# route for item addition
@bp_inventory.route('/add', methods = ["GET", "POST"])
@login_required
def add_items ():
    if request.method == 'GET':
        if session['user']['RoleID'] != 1: return render_template("error.html", errcode = 403, errmsg = "You do not have permission to add items to the database."), 403
        else: return render_template("inventory/add.html")

    if request.method == 'POST':        
        cxn = None
        values = request.get_json()
        try:
            cxn = connect_db()
            db = cxn.cursor()

            db.execute(f"SELECT RoleID FROM user WHERE Username = '{session['user']['Username']}'")
            f = db.fetchone()
            if f is None: raise SelfNotFoundError(username = session['user']['Username'])
            if f[0] == 2 and f[0] != session['user']['RoleID']: raise SelfRoleError(username = session['user']['Username'], role = f[0])

            for v in values['values']:
                db.execute(f"SELECT * FROM item WHERE ItemID = '{v['ItemID']}'")
                if db.fetchone() is not None: raise ExistingItemError(item = v['ItemID'])

                if(v['Category'] is None):
                    db.execute(f"INSERT INTO item (ItemID,ItemName,Category,ItemDescription,ShelfLife,Unit) VALUES ('{v['ItemID']}', '{escape(v['ItemName'])}', {'NULL'}, '{escape(v['ItemDescription'])}', {'NULL' if v['ShelfLife'] is None else v['ShelfLife']}, '{v['Unit']}')")
                else:
                    db.execute(f"INSERT INTO item (ItemID,ItemName,Category,ItemDescription,ShelfLife,Unit) VALUES ('{v['ItemID']}', '{escape(v['ItemName'])}', '{v['Category']}', '{escape(v['ItemDescription'])}', {'NULL' if v['ShelfLife'] is None else v['ShelfLife']}, '{v['Unit']}')")
            cxn.commit()
        except Exception as e:
            current_app.logger.error(str(e))
            return { "error": str(e) }, 500
        finally:
            if cxn is not None: cxn.close()
        
        return Response(status = 200)
    
# route for item disposal
@bp_inventory.route('/dispose', methods = ["GET", "POST"])
@login_required
def dispose_items ():
    if request.method == "GET":
        if session['user']['RoleID'] != 1: return render_template("error.html", errcode = 403, errmsg = "You do not have permission to dispose items from the database."), 403
        else: return render_template("inventory/remove.html")

    if request.method == "POST":
        items = request.get_json()["items"]
        cxn = None
        try:
            cxn = connect_db()
            db = cxn.cursor()

            db.execute(f"SELECT RoleID FROM user WHERE Username = '{session['user']['Username']}'")
            f = db.fetchone()
            if f is None: raise SelfNotFoundError(username = session['user']['Username'])
            if f[0] == 2 and f[0] != session['user']['RoleID']: raise SelfRoleError(username = session['user']['Username'], role = f[0])

            #Create request here
            db.execute(f"INSERT INTO request (RequestedBy, StatusID, ActingAdmin, IssuedBy, DateIssued, DateReceived, Purpose) VALUES ('{session['user']['FirstName'].upper() + ' ' + session['user']['LastName'].upper() }', 4, '{session['user']['Username']}', '{session['user']['Username']}', CURDATE(), CURDATE(), 'For disposal')")
            db.execute("SELECT LAST_INSERT_ID()")
            requestID = db.fetchone()[0]
            hasProperty = False
            
            for x in items:
                db.execute(f"SELECT * FROM item WHERE ItemID = '{x['ItemID']}'")
                if db.fetchone() is None: raise ItemNotFoundError(item = x)
                
                # Decrement from delivery
                db.execute(f"SELECT AvailableUnit, DeliveryPrice FROM delivery WHERE DeliveryID = {int(x['DeliveryID'])}")
                data = db.fetchone()

                if int(data[1]) >= 15000: hasProperty = True

                if int(data[0]) < int(x["ToDispose"]): raise Exception
                db.execute(f"UPDATE delivery SET AvailableUnit = {int(data[0]) - int(x['ToDispose'])} WHERE DeliveryID = {int(x['DeliveryID'])}")

                # Create request
                db.execute(f"INSERT INTO request_item (RequestID, ItemID, RequestQuantity, QuantityIssued, Remarks, RequestPrice) VALUES ({requestID}, '{x['ItemID']}', {int(x['ToDispose'])}, {int(x['ToDispose'])}, '{x['Remarks']}', {data[1]})")
            if(hasProperty): db.execute(f"UPDATE request SET hasPropertyApproved = 1 WHERE RequestID = {requestID}")
            cxn.commit()
        except Exception as e:
            current_app.logger.error(str(e))
            return { "error": str(e) }, 500
        finally:
            if cxn is not None: cxn.close()

        return Response(status = 200)

# route for item update
@bp_inventory.route('/update', methods = ["GET", "POST"])
@login_required
def update_items ():
    if request.method == "GET":
        if session['user']['RoleID'] != 1: return render_template("error.html", errcode = 403, errmsg = "You do not have permission to update items in the database."), 403
        else: return render_template("inventory/update.html")

    if request.method == "POST":
        values = request.get_json()["values"]
        cxn = None
        try:
            cxn = connect_db()
            db = cxn.cursor()

            db.execute(f"SELECT RoleID FROM user WHERE Username = '{session['user']['Username']}'")
            f = db.fetchone()
            if f is None: raise SelfNotFoundError(username = session['user']['Username'])
            if f[0] == 2 and f[0] != session['user']['RoleID']: raise SelfRoleError(username = session['user']['Username'], role = f[0])

            for v in values:
                db.execute(f"SELECT * FROM item WHERE ItemID = '{v}'")
                if db.fetchone() is None: raise ItemNotFoundError(item = values[v]['ItemID'])

                db.execute(f"SELECT * FROM item WHERE ItemID = '{values[v]['ItemID']}'")
                if db.fetchone() is not None and v != values[v]['ItemID']: raise ExistingItemError(item = v)

                if(values[v]["Category"] is None):
                    db.execute(f"UPDATE item SET ItemID = '{values[v]['ItemID']}', ItemName = '{escape(values[v]['ItemName'])}', Category = NULL, ItemDescription = '{escape(values[v]['ItemDescription'])}', ShelfLife = {'NULL' if values[v]['ShelfLife'] is None else values[v]['ShelfLife']}, Unit = '{values[v]['Unit']}' WHERE ItemID = '{v}'")
                else:
                    db.execute(f"UPDATE item SET ItemID = '{values[v]['ItemID']}', ItemName = '{escape(values[v]['ItemName'])}', Category = '{values[v]['Category']}', ItemDescription = '{escape(values[v]['ItemDescription'])}', ShelfLife = {'NULL' if values[v]['ShelfLife'] is None else values[v]['ShelfLife']}, Unit = '{values[v]['Unit']}' WHERE ItemID = '{v}'")
            cxn.commit()
        except Exception as e:
            current_app.logger.error(str(e))
            return { "error": str(e) }, 500
        finally:
            if cxn is not None: cxn.close()
        
        return Response(status = 200)

# route for item request
@bp_inventory.route('/request', methods = ["GET", "POST"])
def request_items ():
    if (request.method == "GET"): return render_template("inventory/request.html")
        
    if (request.method == "POST"):
        req = request.get_json()["items"]
        purpose = request.get_json()["purpose"]
        name = request.get_json()["name"]
        cxn = None
        try:
            cxn = connect_db()
            db = cxn.cursor()

            db.execute(f"INSERT INTO request (RequestedBy, Purpose) VALUES ('{name.upper()}', '{purpose}')")
            db.execute("SELECT LAST_INSERT_ID()")
            requestID = db.fetchone()[0]

            for x in req:
                db.execute(f"SELECT * FROM item WHERE ItemID = '{x['ItemID']}'")
                if db.fetchone() is None: raise ItemNotFoundError(item = x['ItemID'])

                db.execute(f"INSERT INTO request_item (RequestID, ItemID, RequestQuantity, RequestPrice) VALUES ({requestID}, '{x['ItemID']}', {x['RequestQuantity']}, {x['RequestPrice']})")
            cxn.commit()
        except Exception as e:
            current_app.logger.error(str(e))
            return { "error": str(e) }, 500
        finally:
            if cxn is not None: cxn.close()

        return Response(status = 200)
