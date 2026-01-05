from typing import Dict, Any

class TaskAgent:
    def __init__(self, llm_engine):
        self.llm_engine = llm_engine
        self.tasks = []
    
    def execute(self, user_input: str, context: Dict) -> Dict:
        return {"success": True, "message": f"Task: {user_input}"}
    
    def list_tasks(self, context: Dict) -> Dict:
        return {"success": True, "tasks": []}
