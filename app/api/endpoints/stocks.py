from fastapi import APIRouter

router = APIRouter()

@router.get("/stocks")
async def read_items():
    return {"message": "Endpoint works!"}