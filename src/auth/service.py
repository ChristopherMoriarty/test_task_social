import json

from fastapi import Response, status
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from auth.manager import get_user_manager
from auth.models import User
from config import SECRET_AUTH


class MyCookieTransport(CookieTransport):
    async def get_login_response(self, token: str) -> Response:
        
        response_data = json.dumps({
            "status": "success",
            "data": None,
            "detail": "successfully authorized",
        })
        
        response = Response(content=response_data, status_code=status.HTTP_200_OK)
        response.headers["Content-Type"] = "application/json"
        return self._set_login_cookie(response, token)
    
    async def get_logout_response(self) -> Response:
        
        response_data = json.dumps({
            "status": "success",
            "data": None,
            "detail": "successfully logout",
        })
        
        response = Response(content=response_data, status_code=status.HTTP_200_OK)
        response.headers["Content-Type"] = "application/json"
        return self._set_logout_cookie(response)


cookie_transport = MyCookieTransport(cookie_name="token", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
