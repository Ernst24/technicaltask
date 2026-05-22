from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class RolesOrm(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_name: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    permissions: Mapped[list["PermissionsOrm"]] = relationship(
        "PermissionsOrm", back_populates="role"
    )


class PermissionsOrm(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("roles.id", ondelete="CASCADE")
    )

    resource: Mapped[str] = mapped_column(String(20), nullable=False)
    action: Mapped[str] = mapped_column(String(20), nullable=False)

    role: Mapped["RolesOrm"] = relationship("RolesOrm", back_populates="permissions")

    role_resource_action_uc = UniqueConstraint(role_id, resource, action)
