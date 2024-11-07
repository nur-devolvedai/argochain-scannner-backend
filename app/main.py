# app/main.py
# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.security import OAuth2PasswordRequestForm
# from datetime import timedelta
# from app.database import db
# from app.auth.auth import hash_password, verify_password, create_access_token
# from app.schemas.user import UserCreate, UserResponse, Token
# from app.config import settings

# app/main.py
from fastapi import FastAPI, HTTPException, Depends # type: ignore
from fastapi.security import OAuth2PasswordRequestForm # type: ignore
from datetime import timedelta
from app.database import db
from app.auth.auth import hash_password, verify_password, create_access_token
from app.schemas.user import UserCreate, UserResponse, Token
from app.config import settings
from bson import ObjectId # type: ignore

from pydantic import BaseModel # type: ignore

app = FastAPI()

# @app.post("/auth/register", response_model=UserResponse)
# async def register(user: UserCreate):
#     existing_user = await db["users"].find_one({"email": user.email})
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     hashed_password = hash_password(user.password)
#     user_data = {"email": user.email, "hashed_password": hashed_password}
#     result = await db["users"].insert_one(user_data)
#     created_user = await db["users"].find_one({"_id": result.inserted_id})
#     return {"id": str(created_user["_id"]), "email": created_user["email"]}


@app.post("/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password
    hashed_password = hash_password(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password
    }
    
    # Save the user in MongoDB
    result = await db["users"].insert_one(user_data)
    created_user = await db["users"].find_one({"_id": result.inserted_id})

    return {
        "id": str(created_user["_id"]),
        "username": created_user["username"],
        "email": created_user["email"]
    }


# @app.post("/auth/login", response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await db["users"].find_one({"email": form_data.username})
#     if not user or not verify_password(form_data.password, user["hashed_password"]):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
    
#     access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
#     access_token = create_access_token(
#         data={"sub": user["email"]}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# @app.post("/auth/login", response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await db["users"].find_one({"email": form_data.username})
#     if not user or not verify_password(form_data.password, user["hashed_password"]):
#         raise HTTPException(status_code=400, detail="Invalid credentials")
    
#     access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
#     access_token = create_access_token(
#         data={"sub": user["email"]}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# Define a Pydantic model for login input
class LoginData(BaseModel):
    email: str
    password: str


@app.post("/auth/login")
async def login(login_data: LoginData):
    user = await db["users"].find_one({"email": login_data.email})
    if not user or not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
