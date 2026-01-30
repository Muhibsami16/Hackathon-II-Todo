from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable, Awaitable


class ErrorHandlerMiddleware:
    """
    Middleware to handle errors globally in the application.

    This middleware catches exceptions and returns appropriate error responses.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_error_handling(message):
            # Call the original send function
            await send(message)

        # Call the inner application
        try:
            await self.app(scope, receive, send_with_error_handling)
        except HTTPException as e:
            # Handle HTTP exceptions
            response = JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )
            await response(scope, receive, send)
        except Exception as e:
            # Handle all other exceptions
            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"}
            )
            await response(scope, receive, send)


# Alternative implementation using FastAPI's exception handlers
def add_exception_handlers(app):
    """
    Add global exception handlers to the FastAPI app.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )