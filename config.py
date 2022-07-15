import os
import connexion

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

# crear instancia a aplicaccion connexion
conn_app = connexion.App(__name__, specification_dir=basedir)

# obtener la instancia flask de connexion
app = conn_app.app

# url database
sqlite_url = "sqlite:///" + os.path.join(basedir,"gente.db")

# configurar sqlalchemy correspondiente
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# crear instancia a db
db = SQLAlchemy(app)

# inicializar marshmallow
ma = Marshmallow(app)

