from fastapi_users.authentication import BearerTransport

base_transport = BearerTransport(
    # todo: update url
    tokenUrl="auth/jwt/login"
)
