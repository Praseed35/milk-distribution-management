from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Customer(Base):

    __tablename__ = "customers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_code = Column(
        String(20),
        unique=True,
        nullable=False
    )

    customer_name = Column(
        String(100),
        nullable=False
    )

    primary_phone = Column(
        String(15),
        unique=True,
        nullable=False
    )

    alternate_phone = Column(
        String(15),
        nullable=True
    )

    address = Column(
        String(255),
        nullable=True
    )

    route_id = Column(
        Integer,
        ForeignKey("routes.id"),
        nullable=False
    )

    remarks = Column(
        String(255),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    route = relationship(
        "Route",
        back_populates="customers"
    )