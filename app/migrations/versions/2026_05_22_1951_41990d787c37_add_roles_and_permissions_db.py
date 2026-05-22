"""add roles and permissions db

Revision ID: 41990d787c37
Revises: 6dfdd5e19d00
Create Date: 2026-05-22 19:51:26.102777

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "41990d787c37"
down_revision: Union[str, Sequence[str], None] = "6dfdd5e19d00"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("role_name", sa.String(length=20), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("role_name"),
    )
    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("resource", sa.String(length=20), nullable=False),
        sa.Column("action", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("role_id", "resource", "action"),
    )
    op.add_column("users", sa.Column("role_id", sa.Integer(), nullable=False))
    op.create_foreign_key(None, "users", "roles", ["role_id"], ["id"])
    op.drop_column("users", "role")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("role", sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "users", type_="foreignkey")
    op.drop_column("users", "role_id")
    op.drop_table("permissions")
    op.drop_table("roles")
