import os

print(os.getcwd())

from src.agents.answer_extractor_agent import AnswerExtractorAgent
from src.agents.case_scenario_generator import CaseScenarioGenerator
from src.agents.role_playing_prompt_creator import RolePlayingPromptCreator
from src.agents.base_llm_model import BaseLLMModel


def main(pdf_path: str, answer_path: str, character_name: str = "Dr. Wong", teaching_level: str = "Junior"):
    """Orchestrates the three agents to generate a complete role-playing prompt from a medical PDF."""
    
    # Initialize agents
    model = BaseLLMModel()
    answer_extractor = AnswerExtractorAgent(model)
    scenario_generator = CaseScenarioGenerator(model)
    role_prompt_creator = RolePlayingPromptCreator(model)
    
    # Step 1: Extract raw text from PDF
    raw_text = answer_extractor.extract_text_from_pdf(pdf_path)
    answer_text = answer_extractor.extract_text_from_txt(answer_path)
    # print(f"Raw Text: {raw_text}")
    # print(f"Answer Text: {answer_text}")

    # Step 2: Extract structured answers from the text
    extracted_data = answer_extractor.extract_answers(raw_text, answer_text)
    # print(f"Extracted Text: {extracted_data}")
    
    # Step 3: Generate case scenarios based on the extracted data
    case_scenarios = scenario_generator.generate_scenarios(extracted_data)
    # print(f"Case scenarios: {case_scenarios}")
    
    # Step 4: Generate the final role-playing prompt
    role_playing_prompt = role_prompt_creator.generate_role_playing_prompt(
        extracted_data, case_scenarios, character_name, teaching_level
    )
    
    print("Generated Role-Playing Prompt:\n")
    print(role_playing_prompt)

    print(f"Total Token Usage : {model.total_usage_tokens}")
    print(f"Estimate cost     : {model.total_cost:.8f} $")
    
if __name__ == "__main__":
    pdf_path = "assets/medical_exercise/MEDU3400 HUF2-13 Interpretation of blood gases II 11-10-2023. stu.pdf"  # Replace with actual file path
    answer_path = "assets/medical_exercise/MEDU3400 HUF2-13 Interpretation of blood gases II 11-10-2023_answer.text"

    main(pdf_path, answer_path, character_name="Dr. Wong", teaching_level="Junior")