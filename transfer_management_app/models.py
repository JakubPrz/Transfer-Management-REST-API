from sqlalchemy import Column, Integer, String, Float

from .database import Base


class Transfer(Base):
    __tablename__ = "transfers"
    id = Column(Integer, primary_key=True, index=True)
    sender_name = Column(String, nullable=False)
    recipient_name = Column(String, nullable=False)
    transfer_amount = Column(Float, default=0)
