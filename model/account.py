import model
import enum
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Enum

class AccountPrivilege(enum.Enum):
    COMMON = 1
    PRIVILEDGED = 2

class Account(model.db_service.Model):
    __tablename__ = 'account'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80))
    last_name: Mapped[str] = mapped_column(String(80))
    city: Mapped[str] = mapped_column(String(80))
    phone_number: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(80), unique=True)
    password: Mapped[bytes] = mapped_column(String(64))
    privilege_level: Mapped[AccountPrivilege] = mapped_column(Enum(AccountPrivilege), default=AccountPrivilege.COMMON)

    def to_dict(self) -> dict[str]:
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'privilege_level': self.privilege_level.name,
            'password': self.password,
        }