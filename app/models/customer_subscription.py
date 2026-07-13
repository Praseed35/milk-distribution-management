from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.constants.shifts import Shift
from app.database import Base


class CustomerSubscription(Base):

    __tablename__ = "customer_subscriptions"

    __table_args__ = (
        UniqueConstraint(
            "customer_id",
            "milk_type_id",
            "shift",
            name="uq_customer_milk_type_shift"
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    milk_type_id = Column(
        Integer,
        ForeignKey("milk_types.id"),
        nullable=False
    )

    shift = Column(
        Enum(Shift),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
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

    customer = relationship(
        "Customer",
        back_populates="customer_subscriptions"
    )

    milk_type = relationship(
        "MilkType",
        back_populates="customer_subscriptions"
    )

    delivery_exceptions = relationship(
        "DeliveryException",
        back_populates="customer_subscription"
    )