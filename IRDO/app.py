from sys import exit
from os import environ
from pathlib import Path
from flask_migrate import Migrate#, MigrateCommand
# from flask_script import Manager 
from flask_bcrypt import Bcrypt

from config import app_config_dict
from IRDO import create_app, db

get_config_mode = environ.get('IRDO_CONFIG_MODE', 'Debug')

try:
    config_mode = app_config_dict[get_config_mode.capitalize()]
except KeyError:
    exit("Invalid Config Mode!")

app = create_app(Path.cwd, config_mode)
# bcrypt = Bcrypt(app)

db.init_app(app) 
migrate = Migrate(app, db)
# Manager.add_command(db, MigrateCommand)


if __name__ == '__main__':
    # Manager.run()
    app.run(debug=True)

