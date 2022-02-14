from typing import Union

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.session import Session, sessionmaker


class BaseModel:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


db = SQLAlchemy(
    model_class=BaseModel,
)

migrate = Migrate(db=db, compare_type=True)


def getSession() -> Union[Session, sessionmaker]: return db.session()
