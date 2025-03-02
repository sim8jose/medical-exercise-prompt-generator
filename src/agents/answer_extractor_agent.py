import fitz  # PyMuPDF for PDF processing
from typing import Dict, List
from src.agents.base_llm_model import BaseLLMModel
import json 

class AnswerExtractorAgent():
    def __init__(self, model: BaseLLMModel):
        self.model = model

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extracts raw text from a PDF using PyMuPDF."""
        doc = fitz.open(pdf_path)
        text = "\n".join([page.get_text("text") for page in doc])
        return text
    
    def extract_text_from_txt(self, answer_path: str) -> str:
        """Extracts raw text from a Text."""
        with open(answer_path, "r") as file:
            content = file.read()
        
        return content
    def generate_prompt(self, raw_text: str, answer_text: str) -> str:
        """Constructs a system prompt for LLM-based extraction."""
        return f"""
        You are an AI assistant designed to extract structured learning components from medical case study exercises.  
        Your task is to process the provided medical text and extract:
        1. **Context** – The background information relevant to the case.  
        2. **Question** – The specific question the student must answer.  
        3. **Expected Answer** – The correct response expected from the student.  
        4. **Teaching Hint** – A way to help guide the student if they struggle with the question. 

        **Learning Goals**:
        {answer_text}
        
        Ensure your extraction is **structured, clear, and precise**.  
        
        ### Example Extraction:
        #### Input:  
        "A 20-year-old student was admitted after an overdose on sedatives. His blood gas readings were:  
        • PaO₂ = 65 mm Hg  
        • PaCO₂ = 60 mm Hg  
        
        Dr. Wong asks: 'Is alveolar ventilation of the patient adequate?'  
        Expected Answer: The student should recognize that ventilation is inadequate, ideally by explaining that the high PaCO₂ indicates poor ventilation.  
        Hint: Consider the relationship between PaCO₂ levels and ventilation efficiency."
        
        #### Output:
        {{
            "0": {{  
                "context": "A 20-year-old student was admitted after an overdose on sedatives. His blood gas readings were: PaO₂ = 65 mm Hg, PaCO₂ = 60 mm Hg.",  
                "question": "Is alveolar ventilation of the patient adequate?",  
                "expected_answer": "No, ventilation is inadequate because the high PaCO₂ indicates poor ventilation.",  
                "teaching_hint": "Consider the relationship between PaCO₂ levels and ventilation efficiency."  
            }},
            "1": {{
                ...
            }}
        }}
        
        Now, extract structured data from the provided medical case text:
        {raw_text}
        """
    
    def extract_answers(self, raw_text: str, answer_text: str) -> Dict[str, str]:
        """Uses LLM to extract structured answers from medical exercises."""
        prompt = self.generate_prompt(raw_text, answer_text)
        result = self.model.generate_completion(prompt).replace('```json', '').replace('```', '')
        return json.loads(result)  # Ensure `generate_completion()` is implemented
    
if __name__ == "__main__":
    pdf_path = "sample_medical_exercise.pdf"  # Replace with actual file path
    agent = AnswerExtractorAgent()
    raw_text = agent.extract_text_from_pdf(pdf_path)
    extracted_data = agent.extract_answers(raw_text)
    print(extracted_data)
