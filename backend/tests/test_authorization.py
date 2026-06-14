import pytest
from app.modules.auth.services.authorization import AuthorizationService, Principal
from app.shared.exceptions.http import ForbiddenException


def test_authorization_guard_denies_missing_permission():
    service = AuthorizationService()
    with pytest.raises(ForbiddenException):
        service.check_permission(
            Principal(user_id="u1", organization_id="o1", role="Viewer"),
            "notification:create",
        )
