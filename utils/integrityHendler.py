from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

UNIQUE_CONSTRAINT_VIOLATION_CODE = 1062
FOREIGN_KEY_CONSTRAINT_VIOLATION_CODE = 1452


def integrityHandler(errorException: IntegrityError):
    errorCode = errorException.orig.args[0]

    if errorCode == UNIQUE_CONSTRAINT_VIOLATION_CODE:
        raise HTTPException(400, 'The entered information is available in the database!')

    if errorCode == FOREIGN_KEY_CONSTRAINT_VIOLATION_CODE:
        raise HTTPException(400, 'The entered information is not available in the database!')

    raise HTTPException(400, 'Data processing error!')
