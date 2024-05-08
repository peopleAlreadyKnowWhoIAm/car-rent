import model
import enum
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Enum

class AccountPrivilege(enum.Enum):
    COMMON = 1
    PRIVILEDGED = 2

class Account(model.db.Model):
    __tablename__ = 'account'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80))
    last_name: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(80))
    password: Mapped[bytes] = mapped_column(String(64))
    privilege_level: Mapped[AccountPrivilege] = mapped_column(Enum(AccountPrivilege))

    def to_dict(self) -> dict[str]:
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'privilege_level': self.privilege_level.name
        }