import sqlalchemy.orm
import flask_sqlalchemy

class DbBase(sqlalchemy.orm.DeclarativeBase, sqlalchemy.orm.MappedAsDataclass):
    pass

db = flask_sqlalchemy.SQLAlchemy(model_class=DbBase)


# Import models
import model.car
import model.account
import model.reservation
