from fastapi import APIRouter

router = APIRouter()

@router.get("/watchlist")
async def read_items():
    return {"message": "Endpoint works!"}