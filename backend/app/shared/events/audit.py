from dataclasses import dataclass


@dataclass(slots=True)
class AuditEvent:
    organization_id: str
    actor_id: str
    action: str
    resource: str
    before_state: str
    after_state: str
