from fastapi import Request, Response


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