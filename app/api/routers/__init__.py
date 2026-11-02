from app.api.routers.publishers import router as publishers_router
from app.api.routers.authors import router as authors_router
from app.api.routers.books import router as books_router

__all__ = ["publishers_router", "authors_router", "books_router"]
