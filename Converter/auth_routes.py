from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.collection import Collection
from datetime import datetime
import schema, utils
from database import get_users_collection
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from oauth2 import Authentication

router = APIRouter()

auth=Authentication()

@router.post("/register")
def register(user: schema.userRegistration, users_collection: Collection = Depends(get_users_collection)) :
    existing_user = users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="This username is already registered"
        )

    hashed_password = utils.hash(user.password)

    inserting_user = users_collection.insert_one({
        "username": user.username,
        "password": hashed_password,
        "created_at": datetime.utcnow()
    })

    new_user = users_collection.find_one({"_id": inserting_user.inserted_id})
    
    return schema.user_serializer(new_user)  


@router.post("/login", response_model=schema.TokenResponse)
def login(user_credentials: OAuth2PasswordRequestForm= Depends(), users_collection: Collection= Depends(get_users_collection)) :
    user= users_collection.find_one({"username" : user_credentials.username})
    if not user :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    if not utils.verify(user_credentials.password, user["password"]) :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    
    access_token = auth.create_token(data={"_id": str(user["_id"])})
    return{"access_token" : access_token , "token_type" : "bearer"}