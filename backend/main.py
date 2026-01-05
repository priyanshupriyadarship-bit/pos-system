from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.integrations import router as integrations_router

app = FastAPI(
    title="POS System API",
    description="Present Operating System - AI Personal Management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "POS System API",
        "status": "online",
        "docs": "/docs",
        "health": "/api/integrations/health"
    }

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "POS API"}

# Include integrations router
app.include_router(integrations_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
