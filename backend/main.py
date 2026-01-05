from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List
from backend.core.llm_engine import LLMEngine
from backend.agents.task_agent import TaskAgent
from backend.agents.email_agent import EmailAgent
from backend.agents.calendar_agent import CalendarAgent
from backend.core.avatar_system import AvatarSystem
from backend.integrations import router as integrations_router
import uvicorn

app = FastAPI(title="Present Operating System (POS)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(integrations_router)

# Initialize LLM first, then agents
llm = LLMEngine()
task_agent = TaskAgent(llm)
email_agent = EmailAgent(llm)
calendar_agent = CalendarAgent(llm)
avatar_system = AvatarSystem()

@app.get("/")
def root() -> Dict:
    return {"message": "POS System Running", "version": "1.0"}

@app.post("/chat")
def chat_with_martin(prompt: str = Query(...)) -> Dict:
    response = llm.think(prompt, {})
    return {"response": response}

@app.post("/tasks/create")
def create_task(request: str = Query(...)) -> Dict:
    return task_agent.execute(request, {})

@app.get("/tasks")
def list_tasks() -> Dict:
    return task_agent.list_tasks({})

@app.post("/emails/process")
def process_emails() -> Dict:
    return email_agent.execute("process emails", {})

@app.post("/calendar/schedule")
def schedule_task() -> Dict:
    return calendar_agent.execute("show schedule", {})

@app.get("/avatars/stats")
def get_avatar_stats() -> Dict:
    return avatar_system.get_stats()

@app.get("/api/integrations/health")
def integrations_health():
    return {
        "status": "ok",
        "gmail": "configured",
        "calendar": "configured",
        "telegram": "configured"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
