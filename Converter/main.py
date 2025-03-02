from fastapi import FastAPI
import auth_routes,convert_routes

app=FastAPI()

app.include_router(auth_routes.router)
app.include_router(convert_routes.router)

@app.get("/")
def home() :
    return{"message" : "Working Properly"}