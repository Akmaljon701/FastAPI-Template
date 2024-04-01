from fastapi import Request, Response
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse


async def unit_of_work_middleware(request: Request, call_next) -> Response:
    try:
        response = await call_next(request)

        # Committing the DB transaction after the API endpoint has finished successfully
        # So that all the changes made as part of the router are written into the database all together
        # This is an implementation of the Unit of Work pattern https://martinfowler.com/eaaCatalog/unitOfWork.html
        if "db" in request.state._state:
            request.state.db.commit()

        return response
    except:
        # Rolling back the database state to the version before the API endpoint call
        # As the exception happened, all the database changes made as part of the API call
        # should be reverted to keep data consistency
        if "db" in request.state._state:
            request.state.db.rollback()
        raise
    finally:
        if "db" in request.state._state:
            request.state.db.close()


async def handle_integrity_errors(request, call_next):
    try:
        response = await call_next(request)
        return response
    except IntegrityError as e:
        error_msg = str(e.orig)
        error_code = error_msg.split("(")[1].split(",")[0].strip()
        if error_code == '1062':
            return JSONResponse({'detail': error_msg}, status_code=400)
        elif error_code == '1452':
            return JSONResponse({'detail': error_msg}, status_code=400)
        else:
            return JSONResponse({'detail': 'Unexpected error!'}, status_code=400)


