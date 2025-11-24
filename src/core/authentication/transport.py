from fastapi_users.authentication import BearerTransport

bearer_transport = BearerTransport(
    # todo: update url
    tokenUrl="auth/jwt/login"
)
