from pydantic import BaseModel

from app.schemas.rbac import RBACPermissions


class AccessRuleUpdate(RBACPermissions):
    pass


class UserRoleUpdate(BaseModel):
    role_id: int


class BusinessElementCreate(BaseModel):
    name: str


class BusinessElementRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
