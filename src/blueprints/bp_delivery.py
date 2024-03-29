from flask import Blueprint, Response, render_template, request, session, current_app

from src.blueprints.auth import login_required
from src.blueprints.database import connect_db
from src.blueprints.format_data import format_deliveries
from src.blueprints.decode_keyword import decode_keyword
from src.blueprints.exceptions import ItemNotFoundError, SelfNotFoundError, SelfRoleError

bp_delivery = Blueprint("bp_delivery", __name__, url_prefix = "/deliveries")

@bp_delivery.route('/')
@login_required
def deliveries ():
    if session['user']['RoleID'] != 1: return render_template("error.html", errcode = 403, errmsg = "You do not have permission to view deliveries."), 403
    else: return render_template("deliveries/deliveries.html", active = "deliveries")

@bp_delivery.route('/search')
@login_required
def search_deliveries ():
    if session['user']['RoleID'] != 1: return render_template("error.html", errcode = 403, errmsg = "You do not have permission to search for deliveries."), 403

    keywords = [] if "keywords" not in request.args else [decode_keyword(x).lower() for x in request.args.get("keywords").split(" ")]
    conditions = []
    for x in keywords:
        conditions.append(f"(ItemID LIKE '%{x}%' OR ItemName LIKE '%{x}%' OR ItemDescription LIKE '%{x}%' OR Source LIKE '%{x}%' OR Supplier LIKE '%{x}%' OR Category LIKE '%{x}%')")
    query = f"SELECT DeliveryID, ItemID, ItemName, Category, ItemDescription, DeliveryQuantity, Unit, DeliveryPrice, ShelfLife, DATE_FORMAT(delivery.DeliveryDate, '%d %b %Y') as DeliveryDate, Source, ReceivedBy, IsExpired, Supplier, AvailableUnit FROM delivery INNER JOIN item USING (ItemID) INNER JOIN expiration USING (DeliveryID) {'' if len(conditions) == 0 else 'WHERE (' + ' AND '.join(conditions) + ')'} ORDER BY DeliveryID DESC"
    
    cxn = None
    try:
        cxn = connect_db()
        db = cxn.cursor()
        db.execute(query)
        deliveries = db.fetchall()
    except Exception as e:
        current_app.logger.error(str(e))
        return { "error": str(e) }, 500
    finally:
        if cxn is not None: cxn.close()

    return { "deliveries": format_deliveries(deliveries) }

@bp_delivery.route('/add', methods = ["GET", "POST"])
@login_required
def add_deliveries ():
    if request.method == 'GET':
        if session['user']['RoleID'] != 1: return render_template("error.html", errcode = 403, errmsg = "You do not have permission to add deliveries to the database."), 403
        else: return render_template("deliveries/add.html")

    if request.method == 'POST':
        values = request.get_json()
        cxn = None
        try:
            cxn = connect_db()
            db = cxn.cursor()

            db.execute(f"SELECT RoleID FROM user WHERE Username = '{session['user']['Username']}'")
            f = db.fetchone()
            if f is None: raise SelfNotFoundError(username = session['user']['Username'])
            if f[0] != 1: raise SelfRoleError(username = session['user']['Username'], role = f[0])

            for v in values['values']:
                db.execute(f"SELECT * FROM item WHERE ItemID = '{v['ItemID']}'")
                if db.fetchone() is None: raise ItemNotFoundError(item = v['ItemID'])

                db.execute(f"INSERT INTO delivery (ItemID, DeliveryQuantity, DeliveryDate, ReceivedBy, Source, Supplier, DeliveryPrice, AvailableUnit) VALUES ('{v['ItemID']}', {v['DeliveryQuantity']}, '{v['DeliveryDate']}', '{session['user']['Username']}', '{v['Source']}', '{v['Supplier']}', '{v['DeliveryPrice']}', {v['DeliveryQuantity']})")
                db.execute(f"UPDATE item SET Price = {v['DeliveryPrice']} WHERE ItemID = '{v['ItemID']}'")
            cxn.commit()
        except Exception as e:
            current_app.logger.error(str(e))
            return { "error": str(e) }, 500
        finally:
            if cxn is not None: cxn.close()
        
        return Response(status = 200)