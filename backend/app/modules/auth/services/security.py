from datetime import UTC, datetime, timedelta

import jwt
from app.core.config.settings import settings
from app.shared.exceptions.http import UnauthorizedException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class JWTService:
    def create_access_token(self, subject: str, organization_id: str, role: str) -> str:
        payload = {
            "sub": subject,
            "org": organization_id,
            "role": role,
            "type": "access",
            "exp": datetime.now(UTC) + timedelta(minutes=settings.access_token_exp_minutes),
        }
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    def create_refresh_token(self, subject: str, organization_id: str) -> str:
        payload = {
            "sub": subject,
            "org": organization_id,
            "type": "refresh",
            "exp": datetime.now(UTC) + timedelta(minutes=settings.refresh_token_exp_minutes),
        }
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    def decode_token(self, token: str) -> dict[str, str]:
        try:
            decoded = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except jwt.PyJWTError as exc:
            raise UnauthorizedException("Invalid token") from exc
        return {k: str(v) for k, v in decoded.items()}


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
