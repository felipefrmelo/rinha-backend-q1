from functools import wraps

from orjson import dumps

from .data import Response
from ...services.exceptions import ValidationError, UserNotFound
from ...domain.exceptions import LimitExceeded


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValidationError as e:
            return Response(status_code=422, body=dumps({"error": str(e)}))
        except UserNotFound:
            return Response(status_code=404, body=dumps({"error": "User not found"}))
        except LimitExceeded:
            return Response(status_code=422, body=dumps({"error": "Limit exceeded"}))
    return wrapper
