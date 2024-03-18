from fastapi import HTTPException
from fastapi import status

credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      detail="Could not validate credentials",
                                      headers={"WWW-Authenticate": "Bearer"}, )
NOT_FOUND = HTTPException(detail="Not found!", status_code=404)
CREATED = HTTPException(status_code=201, detail="Created successfully!")
UPDATED = HTTPException(detail="Successfully updated!", status_code=200)
ALREADY_EXISTS = HTTPException(detail="Already exists!", status_code=400)
INCORRECT_PASS = HTTPException(detail="Password is incorrect!", status_code=400)
FILE_TYPE_ERROR = HTTPException(detail="File type error!", status_code=422)
