from src.agents.answer_extractor_agent import AnswerExtractorAgent
from src.agents.case_scenario_generator import CaseScenarioGenerator
from src.agents.role_playing_prompt_creator import RolePlayingPromptCreator
from src.agents.base_llm_model import BaseLLMModel

import logging

# Set up basic logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def save_prompt_to_file(prompt: str, output_file: str):
    # Save the prompt to a text file
    with open(output_file, 'w') as file:
        file.write(prompt)
        
    print(f"Prompt has been saved to {output_file}")

def main(pdf_path: str, answer_path: str, output_path: str, character_name: str = "Dr. Wong", teaching_level: str = "Junior"):
    """Orchestrates the three agents to generate a complete role-playing prompt from a medical PDF."""
    
    logging.info("Initializing agents...")
    
    # Initialize agents
    model = BaseLLMModel()
    answer_extractor = AnswerExtractorAgent(model)
    scenario_generator = CaseScenarioGenerator(model)
    role_prompt_creator = RolePlayingPromptCreator(model)
    
    # Step 1: Extract raw text from PDF
    logging.info(f"Extracting raw text from PDF: {pdf_path}")
    raw_text = answer_extractor.extract_text_from_pdf(pdf_path)
    answer_text = answer_extractor.extract_text_from_txt(answer_path)
    
    logging.debug(f"Raw Text: {raw_text[:200]}...")  # Log only the first 200 chars for brevity
    logging.debug(f"Answer Text: {answer_text[:200]}...")  # Log only the first 200 chars for brevity

    # Step 2: Extract structured answers from the text
    logging.info("Extracting structured answers from text...")
    extracted_data = answer_extractor.extract_answers(raw_text, answer_text)
    
    logging.debug(f"Extracted Data: {extracted_data}")  # Log the extracted data
    
    # Step 3: Generate case scenarios based on the extracted data
    logging.info("Generating case scenarios...")
    case_scenarios = scenario_generator.generate_scenarios(extracted_data)
    
    logging.debug(f"Case scenarios: {case_scenarios}")  # Log the generated scenarios
    
    # Step 4: Generate the final role-playing prompt
    logging.info("Generating the final role-playing prompt...")
    role_playing_prompt = role_prompt_creator.generate_role_playing_prompt(
        extracted_data, case_scenarios, character_name, teaching_level
    )

    logging.info("Generated Role-Playing Prompt:\n")
    logging.info(role_playing_prompt)

    logging.info(f"Total Token Usage: {model.total_usage_tokens}")
    logging.info(f"Estimated Cost: {model.total_cost:.8f} $")

    # Run the function to generate and save the prompt
    save_prompt_to_file(role_playing_prompt, output_path)
    logging.info(f"Prompt saved to {output_path}")


if __name__ == "__main__":
    pdf_path = "assets/medical_exercise/1/MEDU3400 HUF2-13 Interpretation of blood gases II 11-10-2023. stu.pdf"  # Replace with actual file path
    answer_path = "assets/medical_exercise/1/MEDU3400 HUF2-13 Interpretation of blood gases II 11-10-2023_answer.text"

    pdf_path = "assets/medical_exercise/2/question.pdf"  # Replace with actual file path
    answer_path = "assets/medical_exercise/2/answer.pdf"
    output_path = "assets/medical_exercise/2/generated_prompt.text"

    main(pdf_path, answer_path, output_path, character_name="Dr. Wong", teaching_level="Junior")