from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Union



class userRegistration(BaseModel) :
    username: EmailStr
    password: str

class userLogin(BaseModel) :
    username: EmailStr
    password: str

class TokenResponse(BaseModel) :
    access_token : str
    token_type: str

class TokenData(BaseModel) :
    id: Union[str,None]=None

# RETURNING TO USER SCREEN IN MONGODB 

def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),  
        "username": user["username"],  
        "created_at": user["created_at"].isoformat() if "created_at" in user else None  
    }