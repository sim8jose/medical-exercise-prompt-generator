from src.agents.base_llm_model import BaseLLMModel
from typing import Dict

class RolePlayingPromptCreator():
    def __init__(self, model : BaseLLMModel):
        self.model = model

    def generate_prompt(self, extracted_data: Dict[str, str], case_scenarios: Dict, character_name: str, teaching_level: str) -> str:
        """Constructs a RoleLLM-style system prompt for an interactive learning experience."""
        prompt = f"""
        You are an AI medical tutor named {character_name}, an expert in clinical reasoning and medical education.  
        Your role is to guide medical students through patient case scenarios, ensuring they understand the rationale behind their decisions.  
        
        **Teaching Level: {teaching_level}**  
        - Encourage **critical thinking** by prompting students to explain their reasoning.  
        - Provide **step-by-step guidance** based on student responses.  
        - Offer **hints instead of direct answers** when students struggle.  
        - Adjust explanations based on the student’s performance.  
        
        **Case Scenario:**  
        {extracted_data}
        
        **Student Actions & Feedback:**  
        """
        
        for id, scenario in case_scenarios.items():
            context = scenario['context']
            question = scenario['question']

            prompt += f"""
            {id}. {context}
            **Question:** {question}  
            """

            for key, value in scenario['actions'].items():
                response = value['response']
                correctness = value['correctness']
                explanation = value['explanation']
                prompt += f"""
                (Option {key}): {response}  
                - **Correctness:** {correctness}  
                - **Tutor Response:** {explanation}  
                """
        
        return prompt
    
    def generate_role_playing_prompt(self, extracted_data: Dict[str, str], case_scenarios: Dict, character_name: str, teaching_level: str) -> str:
        """Uses LLM to generate a complete role-playing prompt for interactive learning."""
        prompt = self.generate_prompt(extracted_data, case_scenarios, character_name, teaching_level)
        return prompt
    
if __name__ == "__main__":
    extracted_data = {
        "context": "A 20-year-old student was admitted after an overdose on sedatives. His blood gas readings were: PaO₂ = 65 mm Hg, PaCO₂ = 60 mm Hg.",
        "question": "Is alveolar ventilation of the patient adequate?",
        "expected_answer": "No, ventilation is inadequate because the high PaCO₂ indicates poor ventilation."
    }
    
    case_scenarios = {
        "actions": {
            "A": {"response": "Yes, because oxygen levels are within range.", "correctness": "Incorrect", "explanation": "Oxygen levels alone do not determine ventilation adequacy. Elevated PaCO₂ indicates hypoventilation."},
            "B": {"response": "No, because the high PaCO₂ indicates poor ventilation.", "correctness": "Correct", "explanation": "Correct! High PaCO₂ suggests hypoventilation, meaning ventilation is inadequate."},
            "C": {"response": "It cannot be determined without additional tests.", "correctness": "Incorrect", "explanation": "PaCO₂ levels are sufficient to determine ventilation adequacy without additional tests."}
        }
    }
    
    agent = RolePlayingPromptCreator()
    role_playing_prompt = agent.generate_role_playing_prompt(extracted_data, case_scenarios, character_name="Dr. Wong", teaching_level="Junior")
    print(role_playing_prompt)
