from pydantic import BaseModel

class BankBase(BaseModel):
    name: str

class BankCreate(BaseModel):
    id: int
    name: str
class BranchCreate(BaseModel):
    ifsc:str
    bank_id:int 
    branch:str
    address:str
    city:str
    district:str
    state:str


class Branch(BaseModel):
    bank_name: str
    ifsc: str
    branch:str
    address:str
    city:str
    district:str
    state:str

class City(BaseModel):
    bank_name:str
    ifsc:str
    branch:str
    city:str


class Bank(BankBase):
    id: int
    name:str
    branch:str
    ifsc:str
    city:str

    class Config:
        from_attributes = True