from fastapi import FastAPI, Depends
from src.router import auth_routes, customer_routes
from src.dependencies.auth import get_current_user


app = FastAPI()

# Rutas públicas
app.include_router(auth_routes.router)

# Rutas protegidas
app.include_router(customer_routes.router, dependencies=[Depends(get_current_user)])


@app.get("/")
async def root():
    return {"message": "Welcome to the Customer Management API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
