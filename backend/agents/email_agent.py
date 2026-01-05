from typing import Dict, Any

class EmailAgent:
    def __init__(self, llm_engine):
        self.llm_engine = llm_engine
    
    def execute(self, user_input: str, context: Dict) -> Dict:
        return {"success": True, "message": "Emails processed"}
