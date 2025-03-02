# Medical Tutor LLM - Interactive Role-Playing AI

## Overview
This project uses an LLM-based system to guide medical students through interactive case-based learning. The system consists of three AI agents:

1. **Answer Extractor Agent** - Extracts structured medical questions and answers from PDFs.
2. **Case Scenario Generator** - Generates medical case-based scenarios with correct and incorrect actions.
3. **Role-Playing Prompt Creator** - Formats the cases into interactive role-playing prompts with a tutor NPC.

## Installation & Setup
### **1. Create and Activate Environment**
Run the following commands to set up the environment:
```bash
conda env create -f environment.yml
conda activate medical-llm-env
```

### **2. Set Up Your Own LLM in `BaseLLMModel`**
Modify `base_llm_model.py` to integrate your own LLM. Example:
```python
import openai  # Replace with your custom LLM provider if needed

class BaseLLMModel:
    def __init__(self, model="gpt-4", api_key=None):
        self.model = model
        self.api_key = api_key or "your_default_api_key_here"
    
    def generate_completion(self, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            api_key=self.api_key,
            messages=[{"role": "system", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
```
Alternatively, store your API key in a `.env` file:
```ini
LLM_API_KEY=your_api_key_here
```

## Running the System
### **1. Process a Medical Case PDF**
Run the main pipeline to process a PDF and generate interactive prompts:
```bash
python main_pipeline.py --pdf sample_medical_exercise.pdf --character "Dr. Wong" --teaching_level "Junior"
```

### **2. Running Individual Agents**
You can also run each agent separately:
```bash
python answer_extractor_agent.py --pdf sample_medical_exercise.pdf
python case_scenario_generator.py --input extracted_data.json
python role_playing_prompt_creator.py --input case_scenarios.json --character "Dr. Smith" --teaching_level "Advanced"
```

## Notes
- Ensure your LLM is properly set up in `base_llm_model.py`.
- Modify the teaching level and character parameters to customize responses.
- The system is designed to be modular, allowing easy expansion for new cases and teaching styles.