import model
import enum
from  sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, LargeBinary, Enum

class CarStatus(enum.Enum):
    AVALAIBLE = 1
    RESERVED = 2
    DAMAGED = 3

class CarMode(enum.Enum):
    STANDARD = 1
    SPORT = 2
    VINTAGE = 3
    BUSINESS = 4

class Car(model.db_service.Model):
    __tablename__ = 'car'

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    model: Mapped[str] = mapped_column(String(80))
    brand: Mapped[str] = mapped_column(String(32))
    year: Mapped[int]
    price: Mapped[float]
    image: Mapped[str] = mapped_column(String(255))
    status: Mapped[CarStatus] = mapped_column(Enum(CarStatus))
    mode: Mapped[CarMode] = mapped_column(Enum(CarMode))

    def to_dict(self) -> dict[str]:
        return {
            'id': self.id,
            'model': self.model,
            'brand': self.brand,
            'year': self.year,
            'price': self.price,
            'status': self.status.name,
            'mode': self.mode.name,
            'image': self.image,
        }