from pydantic import BaseModel


class TransferBase(BaseModel):
    sender_name: str
    recipient_name: str
    transfer_amount: float


class TransferIn(TransferBase):
    pass


class TransferOut(TransferBase):
    id: int

    class Config:
        orm_mode = True
