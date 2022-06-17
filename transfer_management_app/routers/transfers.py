from typing import List, Optional
from fastapi import (APIRouter, Depends, HTTPException, Path, Query, Response, status)
from sqlalchemy.orm import Session

from .. import crud
from ..dependencies import get_db
from ..exceptions.schemas import BadRequest
from ..schemas import *


router = APIRouter(prefix="/transfers", tags=["Transfers"],
                   responses={status.HTTP_400_BAD_REQUEST: {"model": BadRequest}})
ROOT = "/"
TRANSFER_DETAIL_PATH = ROOT + "{transfer_id}"
VALID_TRANSFER_ID_PATH_PARAM = Path(..., title="ID of a transfer", ge=1)
VALID_FILTER_QUERY_PARAM = Query(default=None, min_length=1)


@router.get(TRANSFER_DETAIL_PATH, response_model=TransferOut, status_code=status.HTTP_200_OK, summary="Get a transfer by ID.")
def get_transfer(*, transfer_id: int = VALID_TRANSFER_ID_PATH_PARAM, db: Session = Depends(get_db)):
    """
    Retrieves a transfer with a specified id.

    **transfer_id**: ID of a transfer to be retrieved.
    """

    db_transfer = crud.get_transfer(db=db, transfer_id=transfer_id)
    if db_transfer:
        return db_transfer
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transfer not found.")


@router.delete(TRANSFER_DETAIL_PATH, status_code=status.HTTP_200_OK, summary="Delete a transfer.")
def delete_transfer(*, transfer_id: int = VALID_TRANSFER_ID_PATH_PARAM,
                    response: Response, db: Session = Depends(get_db)):
    """
    Deletes a transfer with a specified id.

    **transfer_id** ID of a transfer to be deleted.
    """

    db_student = crud.get_transfer(db=db, transfer_id=transfer_id)
    if db_student:
        crud.delete_transfer(db=db, transfer_id=transfer_id)
    response.status_code = status.HTTP_200_OK
    return response


@router.get(ROOT, status_code=status.HTTP_200_OK, response_model=List[TransferOut], summary="Get all transfers.")
def get_transfers(sender_name: Optional[str] = VALID_FILTER_QUERY_PARAM,
                  recipient_name: Optional[str] = VALID_FILTER_QUERY_PARAM,
                  transfer_amount: Optional[str] = VALID_FILTER_QUERY_PARAM,
                  db: Session = Depends(get_db)):
    """
    Retrieves all transfers. Optionally, specify additional query parameters
    to filter the results.

    **sender_name**: Name of a transfer sender.
    **recipient_name**: Name of a transfer recipient.
    **transfer_amount**: Amount of a transfer.
    """

    return crud.get_transfers(db, sender_name, recipient_name, transfer_amount)


@router.post(ROOT, response_model=TransferOut, status_code=status.HTTP_201_CREATED, summary="Create a new transfer.")
def post_transfer(transfer: TransferIn, db: Session = Depends(get_db)):
    """
    Creates a new transfer with a specified information.

    **sender_name**: Name of a transfer sender.
    **recipient_name**: Name of a transfer recipient.
    **transfer_amount**: Amount of a transfer.
    """

    return crud.create_transfer(db=db, transfer=transfer)


@router.put(TRANSFER_DETAIL_PATH, response_model=TransferOut, status_code=status.HTTP_200_OK, summary="Update a transfer.")
def put_transfer(*, transfer_id: int = VALID_TRANSFER_ID_PATH_PARAM, transfer: TransferIn,
                 response: Response, db: Session = Depends(get_db)):
    """
    Update a transfer with a specified information.

    **transfer_id**: ID of a transfer.
    **sender_name**: Name of a transfer sender.
    **recipient_name**: Name of a transfer recipient.
    **transfer_amount**: Amount of a transfer.
    """

    db_transfer = crud.get_transfer(db=db, transfer_id=transfer_id)
    if db_transfer:
        db_student = crud.update_transfer(db=db, db_transfer=db_transfer, update_data=transfer)
        return db_student
    else:
        response.status_code = status.HTTP_201_CREATED
        return crud.create_transfer(db=db, transfer=transfer)
