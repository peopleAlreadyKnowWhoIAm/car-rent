import model
import datetime
import enum
import flask_sqlalchemy
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Enum, ForeignKey

from model.car import Car
from model.account import Account


class ReservationStatus(enum.Enum):
    WAITING_CONFIRMATION = 1
    CONFIRMED = 2
    IS_USED = 3
    WAITING_CHECK = 4
    WAITING_PAYMENT = 5
    COMPLETED = 6
    CANCELED = 7


class Reservation(model.db_service.Model):
    __tablename__ = 'reservation'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    status: Mapped[ReservationStatus] = mapped_column(Enum(ReservationStatus), default=ReservationStatus.WAITING_CONFIRMATION)
    start_date: Mapped[datetime.datetime]
    end_date: Mapped[datetime.datetime]
    expected_profit: Mapped[float]
    money_status: Mapped[float]
    car_id: Mapped[int] = mapped_column(ForeignKey("car.id"), init=False, repr=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('account.id'), init=False, repr=False)
    car: Mapped[Car] = relationship(backref="car")
    user: Mapped[Account] = relationship(backref="account")
    fines: Mapped[float] = mapped_column(default=0)

    def to_dict(self) -> dict[str]:
        return {
            'id': self.id,
            'status': self.status.name,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'expected_profit': self.expected_profit,
            'fines': self.fines,
            'money_status': self.money_status,
            'car': self.car.to_dict(),
            'user': self.user.to_dict(),
        }