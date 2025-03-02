from openai import OpenAI  # Using OpenAI LLM API
from dotenv import load_dotenv
import os

load_dotenv()

class BaseLLMModel:
    def __init__(self):
        # self.model = "gpt-4o-mini"
        # self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        # self.cost_per_1m_tokens = 0.3

        self.model = "deepseek-chat"
        self.client = OpenAI(api_key=os.getenv('DEEPSEEK_API_KEY'), base_url="https://api.deepseek.com")
        self.cost_per_1m_tokens = 1.1

        self.total_usage_tokens = 0
        self.total_cost = 0
    
    def generate_completion(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": prompt}]
        )

        
        self.total_usage_tokens += response.usage.total_tokens
        self.total_cost += response.usage.total_tokens / 1e6 * self.cost_per_1m_tokens

        return response.choices[0].message.content