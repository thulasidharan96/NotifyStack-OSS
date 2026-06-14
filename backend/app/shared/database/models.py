from enum import StrEnum

from app.shared.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from sqlalchemy import Boolean, Enum, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


class RoleName(StrEnum):
    OWNER = "Owner"
    ADMIN = "Admin"
    DEVELOPER = "Developer"
    VIEWER = "Viewer"


class NotificationStatus(StrEnum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    CANCELLED = "CANCELLED"


class Organization(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "organizations"
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    projects = relationship("Project", back_populates="organization")


class Project(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "projects"
    __table_args__ = (UniqueConstraint("organization_id", "name", name="uq_project_org_name"),)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    organization = relationship("Organization", back_populates="projects")


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))


class Role(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "roles"
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    name: Mapped[RoleName] = mapped_column(Enum(RoleName), index=True)


class Permission(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "permissions"
    resource: Mapped[str] = mapped_column(String(255), index=True)
    action: Mapped[str] = mapped_column(String(255), index=True)


class ApiKey(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "api_keys"
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    key_hash: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class Template(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "templates"
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)


class TemplateVersion(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "template_versions"
    template_id: Mapped[str] = mapped_column(ForeignKey("templates.id"), index=True)
    version: Mapped[int] = mapped_column(Integer)
    content: Mapped[str] = mapped_column(Text)


class Event(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "events"
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    event_name: Mapped[str] = mapped_column(String(255), index=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    payload: Mapped[str] = mapped_column(Text)


class EventDefinition(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "event_definitions"
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    event_name: Mapped[str] = mapped_column(String(255), index=True)


class Notification(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "notifications"
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    channel: Mapped[str] = mapped_column(String(32), index=True)
    status: Mapped[NotificationStatus] = mapped_column(Enum(NotificationStatus), index=True)
    content: Mapped[str] = mapped_column(Text)


class Delivery(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "deliveries"
    notification_id: Mapped[str] = mapped_column(ForeignKey("notifications.id"), index=True)
    provider_id: Mapped[str] = mapped_column(ForeignKey("providers.id"), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    response: Mapped[str] = mapped_column(Text, default="")


class Provider(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "providers"
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    channel: Mapped[str] = mapped_column(String(32), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class ProviderConfig(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "provider_configs"
    provider_id: Mapped[str] = mapped_column(ForeignKey("providers.id"), index=True)
    config_json: Mapped[str] = mapped_column(Text)


class NotificationPreference(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "notification_preferences"
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    user_id: Mapped[str] = mapped_column(String(255), index=True)
    channel: Mapped[str] = mapped_column(String(32), index=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class WorkflowDefinition(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workflow_definitions"
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)


class WorkflowStep(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workflow_steps"
    workflow_definition_id: Mapped[str] = mapped_column(ForeignKey("workflow_definitions.id"), index=True)
    step_order: Mapped[int] = mapped_column(Integer)
    step_type: Mapped[str] = mapped_column(String(64))


class AuditLog(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "audit_logs"
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    actor_id: Mapped[str] = mapped_column(String(255), index=True)
    action: Mapped[str] = mapped_column(String(255), index=True)
    resource: Mapped[str] = mapped_column(String(255), index=True)
    before_state: Mapped[str] = mapped_column(Text, default="")
    after_state: Mapped[str] = mapped_column(Text, default="")


Index("ix_templates_org_project", Template.organization_id, Template.project_id)
Index("ix_notifications_org_project", Notification.organization_id, Notification.project_id)
Index("ix_events_org_project", Event.organization_id, Event.project_id)
