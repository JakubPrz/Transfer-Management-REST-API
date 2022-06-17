from typing import Callable, Optional
from sqlalchemy import delete, update
from sqlalchemy.orm import Session

from . import models, schemas
from .models import Transfer


def with_commit(func: Callable) -> Callable:
    """
    A decorator for auto-commit after DB operation.

    :param func: A decorated DB operation function
    :return: A decorated function.
    """

    def inner(*args, **kwargs):
        func(*args, **kwargs)
        kwargs.get("db").commit()

    return inner


def get_transfer(db: Session, transfer_id: int) -> Transfer | None:
    """
    Retrieves a transfer with a given transfer_id.

    :param db: A session object representing a connection to the DB.
    :param transfer_id: An ID of a transfer to be retrieved.
    :return: Instance of a `Transfer` model if exists or None.
    """

    return db.query(models.Transfer).filter(
        models.Transfer.id == transfer_id).first()


def get_transfers(db: Session,
                  sender_name: Optional[str] = None,
                  recipient_name: Optional[str] = None,
                  transfer_amount: Optional[int | float] = None) -> list[Transfer]:
    """
    Retrieves all transfers. Optionally, filters them by specified keyword
    arguments assuming connection with 'AND' statements.

    :param db: A session object representing a connection to the DB.
    :param sender_name: Name of a transfer sender.
    :param recipient_name: Name of a transfer recipient.
    :param transfer_amount: Amount of a transfer.
    :return: A list containing transfers matching the query or empty list.
    """

    filters = {k: v for k, v in {
        'sender_name': sender_name,
        'recipient_name': recipient_name,
        'transfer_amount': transfer_amount
    }.items() if v is not None}  # remove keys with None values
    return db.query(models.Transfer).filter_by(**filters).all()


def create_transfer(db: Session, transfer: schemas.TransferIn) -> Transfer:
    """
    Creates a new transfer and commits the change to the database.

    :param db: A session object representing a connection to the DB.
    :param transfer: A pydantic model object representing a new transfer.
    :return: Instance of a `Transfer` model representing a new transfer.
    """

    db_transfer = models.Transfer(**transfer.dict())
    db.add(db_transfer)
    db.commit()
    db.refresh(db_transfer)
    return db_transfer


@with_commit
def delete_transfer(db: Session, transfer_id: int) -> None:
    """
    Deletes a transfer with a specified transfer_id.

    :param db: A session object representing a connection to the DB.
    :param transfer_id: An ID of a transfer to be deleted.
    :return: None.
    """

    db.execute(
        delete(models.Transfer)
        .where(models.Transfer.id == transfer_id)
    )


@with_commit
def update_transfer(db: Session, db_transfer: models.Transfer, update_data: schemas.TransferIn) -> Transfer:
    """
    Updates a transfer with a specified transfer_id.

    :param db: A session object representing a connection to the DB.
    :param db_transfer: An instance of a Transfer model to be updated.
    :param update_data: A pydantic model object representing un updated transfer
    :return: A Transfer instance refreshed with updated data.
    """

    db.execute(
        update(models.Transfer)
        .where(models.Transfer.id == db_transfer.id)
        .values(**update_data.dict())
    )
    db.refresh(db_transfer)
    return db_transfer
