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
        "username": user.get("username") ,
        "created_at": user.get("created_at").isoformat() if user.get("created_at") else None  
    }
