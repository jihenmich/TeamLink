from pydantic import BaseModel

class EmployeeBase(BaseModel):
    name: str

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int
    hours_worked: int

    class Config:
        orm_mode = True
