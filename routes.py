from fastapi import APIRouter, HTTPException
from typing import List
from models import Bank, BankCreate,Branch,City,BranchCreate
from database import database

router = APIRouter()

# --- Bank Endpoints ---

@router.post("/banks/", response_model=Bank)
async def create_bank(bank: BankCreate):
    check_query = "SELECT id FROM banks WHERE id = :id"
    existing_bank = await database.fetch_one(query=check_query, values={"id": bank.id})
    if existing_bank:
        raise HTTPException(status_code=400, detail=f"Bank with ID {bank.id} already exists")

    query = """
        INSERT INTO banks (id, name)
        VALUES (:id, :name)
        RETURNING id, name
    """
    try:
        result = await database.fetch_one(query=query, values=bank.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/banks/", response_model=List[BankCreate])
async def get_banks():
    query = "SELECT id, name FROM banks"
    try:
        results = await database.fetch_all(query=query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/banks/{bank_id}", response_model=BankCreate)
async def get_bank(bank_id: int):
    query = "SELECT id, name FROM banks WHERE id = :id"
    try:
        result = await database.fetch_one(query=query, values={"id": bank_id})
        if not result:
            raise HTTPException(status_code=404, detail="Bank not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/banks/{bank_id}", response_model=BankCreate)
async def update_bank(bank_id: int, bank: BankCreate):
    check_query = "SELECT id FROM banks WHERE id = :id"
    existing_bank = await database.fetch_one(query=check_query, values={"id": bank_id})
    if not existing_bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    query = """
        UPDATE banks
        SET name = :name
        WHERE id = :id
        RETURNING id, name
    """
    values = {"id": bank_id, "name": bank.name}
    try:
        result = await database.fetch_one(query=query, values=values)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/banks/{bank_id}")
async def delete_bank(bank_id: int):
    check_query = "SELECT id FROM banks WHERE id = :id"
    existing_bank = await database.fetch_one(query=check_query, values={"id": bank_id})
    if not existing_bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    query = "DELETE FROM banks WHERE id = :id"
    try:
        await database.execute(query=query, values={"id": bank_id})
        return {"detail": "Bank deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# --- Branch Endpoints ---

@router.post("/branches/", response_model=Branch)
async def create_branch(branch: BranchCreate):
    check_query = "SELECT ifsc FROM branches WHERE ifsc = :ifsc"
    existing_branch = await database.fetch_one(query=check_query, values={"ifsc": branch.ifsc})
    if existing_branch:
        raise HTTPException(status_code=400, detail=f"Branch with IFSC {branch.ifsc} already exists")

    check_bank_query = "SELECT id FROM banks WHERE id = :bank_id"
    if not await database.fetch_one(query=check_bank_query, values={"bank_id": branch.bank_id}):
        raise HTTPException(status_code=400, detail=f"Bank with ID {branch.bank_id} does not exist")

    query = """
        INSERT INTO branches (ifsc, bank_id, branch, address, city, district, state)
        VALUES (:ifsc, :bank_id, :branch, :address, :city, :district, :state)
        RETURNING ifsc, bank_id, (SELECT name FROM banks WHERE id = :bank_id) AS bank_name,
                  branch, address, city, district, state
    """
    try:
        result = await database.fetch_one(query=query, values=branch.dict())
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create branch")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/branches/", response_model=List[Branch])
async def get_branches():
    query = """
        SELECT ifsc, bank_id, bank_name, branch, address, city, district, state
        FROM bank_branches
    """
    try:
        results = await database.fetch_all(query=query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/branches/{ifsc}", response_model=Branch)
async def get_branch(ifsc: str):
    query = """
        SELECT ifsc, bank_id, bank_name, branch, address, city, district, state
        FROM bank_branches
        WHERE ifsc = :ifsc
    """
    try:
        result = await database.fetch_one(query=query, values={"ifsc": ifsc})
        if not result:
            raise HTTPException(status_code=404, detail="Branch not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/branches/{ifsc}", response_model=Branch)
async def update_branch(ifsc: str, branch: BranchCreate):
    check_query = "SELECT ifsc FROM branches WHERE ifsc = :ifsc"
    existing_branch = await database.fetch_one(query=check_query, values={"ifsc": ifsc})
    if not existing_branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    check_bank_query = "SELECT id FROM banks WHERE id = :bank_id"
    if not await database.fetch_one(query=check_bank_query, values={"bank_id": branch.bank_id}):
        raise HTTPException(status_code=400, detail=f"Bank with ID {branch.bank_id} does not exist")

    query = """
        UPDATE branches
        SET bank_id = :bank_id, branch = :branch, address = :address, city = :city,
            district = :district, state = :state
        WHERE ifsc = :ifsc
        RETURNING ifsc, bank_id, (SELECT name FROM banks WHERE id = :bank_id) AS bank_name,
                  branch, address, city, district, state
    """
    try:
        result = await database.fetch_one(query=query, values={**branch.dict(), "ifsc": ifsc})
        if not result:
            raise HTTPException(status_code=500, detail="Failed to update branch")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/branches/{ifsc}")
async def delete_branch(ifsc: str):
    check_query = "SELECT ifsc FROM branches WHERE ifsc = :ifsc"
    existing_branch = await database.fetch_one(query=check_query, values={"ifsc": ifsc})
    if not existing_branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    query = "DELETE FROM branches WHERE ifsc = :ifsc"
    try:
        await database.execute(query=query, values={"ifsc": ifsc})
        return {"detail": "Branch deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# --- Additional Query Endpoints ---

@router.get("/branches/city/{city}/{bank_id}", response_model=List[City])
async def get_branches_by_city(city: str, bank_id: int):
    query = """
        SELECT bank_name, ifsc, branch, city
        FROM bank_branches
        WHERE (city) = (:city) AND bank_id = :bank_id
    """
    try:
        result = await database.fetch_all(query=query, values={"city": city, "bank_id": bank_id})
        if not result:
            raise HTTPException(status_code=404, detail="No branches found for the given city and bank ID")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
