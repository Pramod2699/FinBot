from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.requests import Request


class PrefixMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, prefix: str):
        super().__init__(app)
        self.prefix = prefix

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.scope["path"].startswith(self.prefix):
            request.scope["path"] = request.scope["path"][len(self.prefix) :]
            request.scope["root_path"] = request.scope.get("root_path", "")[
                len(self.prefix) :
            ]

        response = await call_next(request)
        # Ensure a response is always returned
        return response or Response("Unhandled request", status_code=500)
