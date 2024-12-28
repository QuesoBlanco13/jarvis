from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from config import settings
import os

class CodeAssistant:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._load_model()

    def _load_model(self):
        try:
            # Using a smaller model suitable for Raspberry Pi
            model_name = "Salesforce/codegen-350M-mono"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float32,
                low_cpu_mem_usage=True
            )
        except Exception as e:
            print(f"Error loading model: {e}")
            # Fallback to simple template-based responses
            self.model = None
            self.tokenizer = None

    async def generate_code(self, prompt: str):
        if not self.model or not self.tokenizer:
            return {"error": "Model not loaded", "generated_code": "// Simple placeholder code"}
        
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt")
            outputs = self.model.generate(
                inputs,
                max_length=150,
                num_return_sequences=1,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id
            )
            generated_code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return {"generated_code": generated_code}
        except Exception as e:
            return {"error": str(e)}

    async def edit_code(self, code: str, instructions: str):
        combined_prompt = f"Original code:\n{code}\nInstructions:\n{instructions}\nModified code:"
        return await self.generate_code(combined_prompt)
