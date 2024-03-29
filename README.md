# sIMS: *simple* inventory management system
sIMS is a tailor-made inventory management system specifically designed for San Roque National High School. This program converts the procurement, management, and distribution of school resources into digital processes. The system utilizes a Flask application as its server application and uses MySQL as its database system. 

## Requirements
* Python 3.10.x or higher
* MySQL 8.0 or higher

## Installation
Clone this repository to your local machine. Then, create a Python virtual environment inside the local repository by running the following command through the terminal inside the directory:
```powershell
py -m venv venv
```

After creating the virtual environment, activate it by running the following:
```powershell
./venv/scripts/activate
```
Once the virtual environment has been activated, further terminal prompts should show `(venv)` at the beginning.

Install this project's dependencies by running the following:
```powershell
pip install -r requirements.txt
```

Finally, import the MySQL database dump file that comes with the repository (`sims.sql`) into your machine's local MySQL connection. This may be done by selecting `Server > Data Import` after connecting through the MySQL Workbench.

## Running the application
To run the application, first make sure that the MySQL80 service is running on your machine. This can be done by checking the Windows Task Manager, navigating to the Services tab, and ensuring that the MySQL80 service status is *Running*.

Once MySQL is running, open the terminal in the repository's root folder.

Then, activate the Python virtual environment as was done during the installation.
```powershell
./venv/scripts/activate
```

Finally, enter the following command to run the application:
```powershell
waitress-serve --host 0.0.0.0 --port 80 --call src:create_app
```

The application will now be accessible through a web browser at `localhost`. Do **not** close the terminal window, otherwise the application will close itself.

To stop the application, press `Ctrl + C` in the terminal or close the terminal.

## Placeholder accounts
**NOTE:** These user accounts come with `sims.sql` purely to serve as dummy accounts for testing.
For actual use, please change these credentials, especially those of the Admin account, to their official credentials.

| Username | Password      | Role      |
| -------- | ------------- | --------- |
| bajo     | Aquaflask20   | Custodian |
| asaito   | fortunecookie | Personnel |
| hpham    | Attention1    | Admin     |

Please be reminded that an Admin account **must** exist to be able to add other users using sIMS.
Removing the Admin account will require Admin account credentials to be written directly using MySQL.
