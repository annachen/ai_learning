import unittest
from unittest.mock import patch, AsyncMock
import os
import asyncio
from src.services.openai_service import OpenAIService
from src.learning_point import LearningPoint
from src.models.exercise import Exercise

class TestOpenAIService(unittest.TestCase):
    def setUp(self):
        # Use a test API key for testing
        os.environ["OPENAI_API_KEY"] = "test-api-key"
        self.service = OpenAIService()
        self.learning_point = LearningPoint(
            "variables",
            "Understanding variables in programming"
        )
        
    def test_initialization(self):
        self.assertEqual(self.service.model, "gpt-4-0125-preview")
        self.assertEqual(self.service.api_key, "test-api-key")
        
    def test_initialization_without_api_key(self):
        os.environ.pop("OPENAI_API_KEY", None)
        with self.assertRaises(ValueError):
            OpenAIService()
            
    def test_create_prompt(self):
        prompt = self.service._create_prompt(
            learning_points=[self.learning_point],
            difficulty="intermediate",
            exercise_type="multiple_choice"
        )
        self.assertIn("variables: Understanding variables in programming", prompt)
        self.assertIn("multiple choice questions", prompt.lower())
        self.assertIn("intermediate", prompt.lower())
        
    @patch('openai.AsyncOpenAI')
    async def test_generate_exercises(self, mock_openai):
        # Mock the OpenAI response
        mock_response = AsyncMock()
        mock_response.choices = [
            AsyncMock(
                message=AsyncMock(
                    content="""
                    Question: What is a variable in programming?
                    Answer: A variable is a named storage location in memory.
                    Explanation: This tests basic understanding of variables.
                    """
                )
            )
        ]
        mock_openai.return_value.chat.completions.create = AsyncMock(
            return_value=mock_response
        )
        
        exercises = await self.service.generate_exercises(
            learning_points=[self.learning_point]
        )
        
        self.assertEqual(len(exercises), 1)
        self.assertIsInstance(exercises[0], Exercise)
        self.assertIn("variable", exercises[0].question)
        self.assertEqual(exercises[0].difficulty_level, "intermediate")
        self.assertEqual(exercises[0].exercise_type, "open_ended")
        
    @patch('openai.AsyncOpenAI')
    async def test_generate_exercises_empty_input(self, mock_openai):
        exercises = await self.service.generate_exercises(
            learning_points=[]
        )
        self.assertEqual(len(exercises), 0)
        mock_openai.return_value.chat.completions.create.assert_not_called()
        
    @patch('openai.AsyncOpenAI')
    async def test_generate_exercises_api_error(self, mock_openai):
        mock_openai.return_value.chat.completions.create = AsyncMock(
            side_effect=Exception("API Error")
        )
        
        exercises = await self.service.generate_exercises(
            learning_points=[self.learning_point]
        )
        self.assertEqual(len(exercises), 0)

if __name__ == '__main__':
    unittest.main()
