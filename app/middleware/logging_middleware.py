import logging
from starlette.middleware.base import BaseHTTPMiddleware

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logging.info(f'Request: {request.method} {request.url}')
        responce = await call_next(request)

        logging.info(f'Response: {responce.status_code}')
        return responce
