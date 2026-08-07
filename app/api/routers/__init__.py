from app.api.routers.books import router as book_router
from app.api.routers.authors import router as author_router
from app.api.routers.publishers import router as publisher_router

__all__ = ["book_router", "author_router", "publisher_router"]
