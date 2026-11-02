import logging
import time

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core import setup_logging, EntityNotFound, NoFieldsToUpdate
from app.api.routers import *

setup_logging() 

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(publishers_router)
app.include_router(authors_router)


@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    
    response = await call_next(request)
    
    process_time = (time.perf_counter() - start_time) * 1000
    
    log_msg = "Handled request: %s %s | Status: %s | Time: %.2fms"
    log_args = (
        request.method, request.url.path, response.status_code, process_time
    )
    
    if response.status_code >= 500:
        logger.error(log_msg, *log_args)
    elif response.status_code >= 400:
        logger.warning(log_msg, *log_args)
    else:
        logger.info(log_msg, *log_args)

    return response


@app.exception_handler(EntityNotFound)
async def entity_not_found_handler(request: Request, exc: EntityNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )


@app.exception_handler(NoFieldsToUpdate)
async def no_fields_to_update_handler(request: Request, exc: NoFieldsToUpdate):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception occurred during %s %s", 
        request.method, request.url.path, 
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )
