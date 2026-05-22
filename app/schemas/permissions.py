from enum import Enum

from pydantic import BaseModel


class ResourceEnum(str, Enum):
    DOCUMENT = "document"
    USER = "user"
    ANALYTICS = "analytics"
    TICKET = "ticket"


class ActionEnum(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    BAN = "ban"


class PermissionSchema(BaseModel):
    id: int
    role_id: int
    resource: ResourceEnum
    action: ActionEnum


class PermissionCreateSchema(BaseModel):
    role_id: int
    resource: ResourceEnum
    action: ActionEnum
