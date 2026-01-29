# app.py
"""
Main FastAPI application with authentication.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes.users import router as user_router
from routes.members import router as members_router
from routes.dining_rooms import router as dining_rooms_router
from routes.time_slots import router as time_slots_router 

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sterling Catering API",
    description="Premium catering booking system with dynamic fee management",
    version="1.0.0"
)

# CORS middleware (configure for your frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(members_router, prefix="/members", tags=["Members"])
app.include_router(dining_rooms_router, prefix="/dining-rooms", tags=["Dining Rooms"])
app.include_router(time_slots_router, prefix="/time-slots", tags=["Time Slots"]) 



@app.get("/", tags=["Health Check"])
def home():
    return {"message": "Sterling Catering API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)