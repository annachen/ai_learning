import unittest
import asyncio
from unittest.mock import patch, AsyncMock
from src.services.mock_llm_service import MockLLMService
from src.models.grading_result import GradingResult

from tests.async_test_case import AsyncTestCase

class TestGrading(AsyncTestCase):
    def setUp(self):
        """Set up the test case with MockLLMService."""
        self.service = MockLLMService()
        
    def test_async_grade_answer(self):
        self.async_test(self._test_grade_answer())
        
    async def _test_grade_answer(self):
        """Test grading an answer successfully."""
        
        result = await self.service.grade_answer(
            problem="What is a variable in programming?",
            student_answer="A variable is a container that stores data.",
            expected_answer="A variable is a named storage location that holds data values.",
            metadata={"topic": "Programming Basics"}
        )
        
        self.assertIsInstance(result, GradingResult)
        self.assertEqual(result.score, 75.0)  # MockLLMService returns fixed score
        self.assertIsInstance(result.feedback, str)  # Should have some feedback
        self.assertIsInstance(result.metadata, dict)  # Should have metadata
        
    def test_async_grade_answer_error_handling(self):
        self.async_test(self._test_grade_answer_error_handling())
        
    async def _test_grade_answer_error_handling(self):
        """Test handling of grading errors."""
        result = await self.service.grade_answer(
            problem="",  # Empty problem should trigger an error
            student_answer=""
        )
        
        self.assertEqual(result.score, 75.0)  # MockLLMService returns fixed score
        self.assertIsInstance(result.feedback, str)  # Should have some feedback
        self.assertIsInstance(result.metadata, dict)  # Should have metadata

if __name__ == '__main__':
    unittest.main()
