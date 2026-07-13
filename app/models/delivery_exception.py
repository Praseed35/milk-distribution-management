from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class DeliveryException(Base):

    __tablename__ = "delivery_exceptions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_subscription_id = Column(
        Integer,
        ForeignKey("customer_subscriptions.id"),
        nullable=False
    )

    start_date = Column(
        Date,
        nullable=False
    )

    end_date = Column(
        Date,
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    reason = Column(
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

    customer_subscription = relationship(
        "CustomerSubscription",
        back_populates="delivery_exceptions"
    )