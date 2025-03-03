from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
from config import settings
from datetime import datetime,timedelta
from fastapi import HTTPException,status,Depends
import schema


oauth2_scheme= OAuth2PasswordBearer(tokenUrl="login")

class Authentication:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algo = settings.ALGORITHM
        self.access_token_expire_time = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def create_token(self,data: dict) :
        to_encode= data.copy()
        expire= datetime.utcnow()+timedelta(minutes=self.access_token_expire_time)

        to_encode.update({"exp":expire})

        encoded_jwt=jwt.encode(to_encode,self.secret_key,algorithm=self.algo)

        return encoded_jwt
    
    def verify_token(self,token: str , credential_exception) :
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token!")
        try :
            decode_jwt_token=jwt.decode(token,self.secret_key,algorithms=[self.algo])
            user_id: str= decode_jwt_token.get("_id")
            if id is None:
                raise credential_exception
            token_data= schema.TokenData(id=user_id)
        except JWTError :
            raise credential_exception
        
        return token_data
    
    def get_current_user(self, token: str= Depends(oauth2_scheme)) :
        credential_exception= HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
                                        detail=f"Token is missing,Please Login first",
                                        headers={"WWW-Authenticate": "Bearer"})
        return self.verify_token(token,credential_exception)


