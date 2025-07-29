from typing import List
import os
import json
from openai import AsyncOpenAI
from .llm_service import LLMService
from ..models.exercise import Exercise
from ..learning_point import LearningPoint

class OpenAIService(LLMService):
    """OpenAI implementation of the LLM service."""
    
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo"):
        """Initialize the OpenAI service."""
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set in OPENAI_API_KEY environment variable")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = model
        
    def _create_prompt(self, 
                      learning_points: List[LearningPoint],
                      difficulty: str,
                      exercise_type: str) -> str:
        points_desc = "\n".join([
            f"- {point.name}: {point.description}"
            for point in learning_points
        ])
        
        type_instructions = {
            "multiple_choice": "Create multiple choice questions with 4 options (A, B, C, D). Include all options in the answer field.",
            "open_ended": "Create open-ended questions that test understanding.",
            "coding": "Create coding exercises that require writing code. Include a sample solution in the answer field."
        }
        
        difficulty_instructions = {
            "beginner": "Keep the questions simple and straightforward.",
            "intermediate": "Include some complexity and deeper understanding.",
            "advanced": "Make the questions challenging and test complex understanding."
        }
        
        return f"""Generate an educational exercise based on these learning points:

{points_desc}

Exercise Type: {type_instructions[exercise_type]}
Difficulty Level: {difficulty_instructions[difficulty]}

Respond with ONLY a JSON object that has these exact fields:
{{
    "question": "the exercise question",
    "expected_answer": "the correct answer or solution",
    "explanation": "explanation of why this is the correct answer"
}}"""

    async def generate_exercises(self,
                               learning_points: List[LearningPoint],
                               count: int = 1,
                               difficulty: str = "intermediate",
                               exercise_type: str = "open_ended") -> List[Exercise]:
        if not learning_points:
            return []
            
        prompt = self._create_prompt(learning_points, difficulty, exercise_type)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert educational content creator. Respond only with the requested JSON format."},
                    {"role": "user", "content": prompt}
                ],
                n=count,
                temperature=0.7
            )
            
            exercises = []
            for choice in response.choices:
                content = choice.message.content
                try:
                    response_data = json.loads(content)
                    exercise = Exercise(
                        question=response_data["question"],
                        expected_answer=response_data["expected_answer"],
                        explanation=response_data["explanation"],
                        difficulty_level=difficulty,
                        exercise_type=exercise_type,
                        related_learning_points=[point.name for point in learning_points]
                    )
                    exercises.append(exercise)
                except Exception as e:
                    print(f"Failed to parse exercise from response: {str(e)}")
                    print(f"Response content: {content}")
                    continue
                    
            return exercises
            
        except Exception as e:
            print(f"Error calling OpenAI API: {str(e)}")
            return []
