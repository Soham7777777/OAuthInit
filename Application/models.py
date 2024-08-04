from Application import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from flask_login import UserMixin

class User(db.Model, UserMixin): # type: ignore
    user_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    sub: Mapped[str] = mapped_column(unique=True, nullable=False, init=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, init=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, init=True)
    dp_url: Mapped[str] = mapped_column(String(128), nullable=False, init=True)

    def get_id(self):
        return str(self.user_id)


# class User(db.Model, UserMixin): # type: ignore
#     user_id: Mapped[int] = mapped_column(primary_key=True, init=False)
#     sub: Mapped[str] = mapped_column(unique=True, nullable=False, init=True)

#     def get_id(self):
#         return str(self.user_id)