import unittest
import asyncio
from unittest.mock import patch, AsyncMock
from src.services.openai_service import OpenAIService
from src.models.grading_result import GradingResult

class TestGrading(unittest.TestCase):
    def setUp(self):
        self.service = OpenAIService(api_key="test-key")
        
    def test_create_grading_prompt(self):
        problem = "What is a variable in programming?"
        student_answer = "A variable is a container that stores data."
        expected_answer = "A variable is a named storage location that holds data values."
        metadata = {
            "topic": "Programming Basics",
            "difficulty": "beginner",
            "student_level": "beginner"
        }
        
        prompt = self.service._create_grading_prompt(
            problem, student_answer, expected_answer, metadata
        )
        
        # Check that all important parts are in the prompt
        self.assertIn(problem, prompt)
        self.assertIn(student_answer, prompt)
        self.assertIn(expected_answer, prompt)
        self.assertIn("Programming Basics", prompt)
        self.assertIn("beginner", prompt)
        
    @patch('openai.AsyncOpenAI')
    async def test_grade_answer(self, mock_openai):
        # Mock OpenAI response
        mock_response = AsyncMock()
        mock_response.choices = [
            AsyncMock(
                message=AsyncMock(
                    content='''
                    {
                        "score": 85,
                        "feedback": "Good understanding of variables, but could be more precise.",
                        "metadata": {
                            "key_concepts_understood": ["data storage", "containers"],
                            "areas_for_improvement": ["technical terminology"],
                            "mastery_level": "intermediate",
                            "confidence": 0.9
                        }
                    }
                    '''
                )
            )
        ]
        mock_openai.return_value.chat.completions.create = AsyncMock(
            return_value=mock_response
        )
        
        result = await self.service.grade_answer(
            problem="What is a variable in programming?",
            student_answer="A variable is a container that stores data.",
            expected_answer="A variable is a named storage location that holds data values.",
            metadata={"topic": "Programming Basics"}
        )
        
        self.assertIsInstance(result, GradingResult)
        self.assertEqual(result.score, 85)
        self.assertTrue("Good understanding" in result.feedback)
        self.assertEqual(result.confidence, 0.9)
        self.assertIn("key_concepts_understood", result.metadata)
        
    @patch('openai.AsyncOpenAI')
    async def test_grade_answer_error_handling(self, mock_openai):
        # Mock API error
        mock_openai.return_value.chat.completions.create = AsyncMock(
            side_effect=Exception("API Error")
        )
        
        result = await self.service.grade_answer(
            problem="test",
            student_answer="test"
        )
        
        self.assertEqual(result.score, 0)
        self.assertTrue("Failed to grade" in result.feedback)
        self.assertEqual(result.confidence, 0)
        self.assertIn("error", result.metadata)

if __name__ == '__main__':
    unittest.main()
