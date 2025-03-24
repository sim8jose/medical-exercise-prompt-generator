from src.agents.answer_extractor_agent import AnswerExtractorAgent
from src.agents.case_scenario_generator import CaseScenarioGenerator
from src.agents.role_playing_prompt_creator import RolePlayingPromptCreator
from src.agents.base_llm_model import BaseLLMModel

import logging

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def save_prompt_to_file(prompt: str, output_file: str):
    if output_file == None or output_file == '':
        return
    
    # Save the prompt to a text file
    with open(output_file, 'w') as file:
        file.write(prompt)
        

    print(f"Prompt has been saved to {output_file}")
def main(pdf_path: str, answer_path: str, output_path: str, character_name: str = "Dr. Wong", teaching_level: str = "Junior", log_callback=None):
    """Orchestrates the three agents to generate a complete role-playing prompt from a medical PDF."""
    
    def log_message(message):
        if log_callback:
            log_callback(message)
        logging.info(message)  # Still log to console/file
    
    log_message("Initializing agents...")
    
    # Initialize agents
    model = BaseLLMModel()
    answer_extractor = AnswerExtractorAgent(model)
    scenario_generator = CaseScenarioGenerator(model)
    role_prompt_creator = RolePlayingPromptCreator(model)
    
    # Step 1: Extract raw text from PDF
    log_message(f"Extracting raw text from PDF: {pdf_path}")
    raw_text = answer_extractor.extract_text_from_pdf(pdf_path)
    answer_text = answer_extractor.extract_text_from_txt(answer_path)
    
    log_message("Extracting structured answers from text...")
    extracted_data = answer_extractor.extract_answers(raw_text, answer_text)
    
    log_message("Generating case scenarios...")
    case_scenarios = scenario_generator.generate_scenarios(extracted_data)
    
    log_message("Generating the final role-playing prompt...")
    role_playing_prompt = role_prompt_creator.generate_role_playing_prompt(
        extracted_data, case_scenarios, character_name, teaching_level
    )

    log_message("Generated Role-Playing Prompt:")
    log_message(role_playing_prompt)

    log_message(f"Total Token Usage: {model.total_usage_tokens}")
    log_message(f"Estimated Cost: {model.total_cost:.8f} $")

    # Save the prompt if an output path is provided
    save_prompt_to_file(role_playing_prompt, output_path)
    log_message(f"Prompt saved to {output_path}")

    return role_playing_prompt, model.total_usage_tokens, model.total_cost


if __name__ == "__main__":
    pdf_path = "assets/medical_exercise/1/MEDU3400 HUF2-13 Interpretation of blood gases II 11-10-2023. stu.pdf"  # Replace with actual file path
    answer_path = "assets/medical_exercise/1/MEDU3400 HUF2-13 Interpretation of blood gases II 11-10-2023_answer.text"

    pdf_path = "assets/medical_exercise/2/question.pdf"  # Replace with actual file path
    answer_path = "assets/medical_exercise/2/answer.pdf"
    output_path = "assets/medical_exercise/2/generated_prompt.text"

    main(pdf_path, answer_path, output_path, character_name="Dr. Wong", teaching_level="Junior")