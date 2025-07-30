import unittest
from unittest.mock import patch, AsyncMock
import os
import asyncio
from src.services.openai_service import OpenAIService
from src.learning_point import LearningPoint
from src.models.exercise import Exercise

from tests.async_test_case import AsyncTestCase

class TestOpenAIService(AsyncTestCase):
    def setUp(self):
        # Use a test API key and patch the AsyncOpenAI client
        self.test_api_key = "test-key"
        self.patcher = patch('openai.AsyncOpenAI')
        self.mock_openai = self.patcher.start()
        self.service = OpenAIService(api_key=self.test_api_key)
        self.learning_point = LearningPoint(
            "variables",
            "Understanding variables in programming"
        )
        
    def tearDown(self):
        self.patcher.stop()
        
    def test_initialization(self):
        self.assertEqual(self.service.model, "gpt-3.5-turbo")
        self.assertEqual(self.service.api_key, self.test_api_key)
        
    def test_initialization_without_api_key(self):
        os.environ.pop("OPENAI_API_KEY", None)
        with self.assertRaises(ValueError):
            OpenAIService()
            
    @patch('openai.AsyncOpenAI')
    def test_create_prompt(self, mock_openai):
        prompt = self.service._create_prompt(
            learning_points=[self.learning_point],
            difficulty="intermediate",
            exercise_type="multiple_choice"
        )
        self.assertIn("variables: Understanding variables in programming", prompt)
        self.assertIn("multiple choice questions", prompt.lower())
        # The string "intermediate" is not directly used in the prompt template,
        # instead it maps to "include some complexity and deeper understanding"
        self.assertIn("complexity", prompt.lower())
        
    def test_generate_exercises(self):
        self.async_test(self._test_generate_exercises())
        
    @patch('openai.AsyncOpenAI')
    async def _test_generate_exercises(self, mock_openai):
        # Mock the OpenAI response
        # Setup mock response with proper json content
        mock_message = AsyncMock()
        mock_message.content = '{"question": "What is a variable in programming?", "expected_answer": "A variable is a named storage location in memory.", "explanation": "This tests basic understanding of variables."}'
        
        mock_choice = AsyncMock()
        mock_choice.message = mock_message
        
        mock_response = AsyncMock()
        mock_response.choices = [mock_choice]
        
        mock_client = AsyncMock()
        mock_client.chat = AsyncMock()
        mock_client.chat.completions = AsyncMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_response)
        mock_openai.return_value = mock_client
        
        exercises = await self.service.generate_exercises(
            learning_points=[self.learning_point]
        )
        
        self.assertEqual(len(exercises), 1)
        self.assertIsInstance(exercises[0], Exercise)
        self.assertIn("variable", exercises[0].question)
        self.assertEqual(exercises[0].difficulty_level, "intermediate")
        self.assertEqual(exercises[0].exercise_type, "open_ended")
        
    def test_generate_exercises_empty_input(self):
        self.async_test(self._test_generate_exercises_empty_input())
        
    @patch('openai.AsyncOpenAI')
    async def _test_generate_exercises_empty_input(self, mock_openai):
        exercises = await self.service.generate_exercises(
            learning_points=[]
        )
        self.assertEqual(len(exercises), 0)
        mock_openai.return_value.chat.completions.create.assert_not_called()
        
    def test_generate_exercises_api_error(self):
        self.async_test(self._test_generate_exercises_api_error())
        
    @patch('openai.AsyncOpenAI')
    async def _test_generate_exercises_api_error(self, mock_openai):
        mock_openai.return_value.chat.completions.create = AsyncMock(
            side_effect=Exception("API Error")
        )
        
        exercises = await self.service.generate_exercises(
            learning_points=[self.learning_point]
        )
        self.assertEqual(len(exercises), 0)

if __name__ == '__main__':
    unittest.main()
