import unittest
import asyncio
from src.services.mock_llm_service import MockLLMService
from src.learning_point import LearningPoint
from src.models.exercise import Exercise

class TestMockLLMService(unittest.TestCase):
    def setUp(self):
        self.llm_service = MockLLMService()
        self.learning_point = LearningPoint(
            "variables", 
            "Understanding variables in programming"
        )

    def test_generate_exercises(self):
        exercises = asyncio.run(
            self.llm_service.generate_exercises(
                learning_points=[self.learning_point],
                count=2
            )
        )
        self.assertEqual(len(exercises), 2)
        for exercise in exercises:
            self.assertIn("variables", exercise.question)
            self.assertEqual(exercise.difficulty_level, "intermediate")
            self.assertEqual(exercise.exercise_type, "open_ended")
            self.assertEqual(exercise.related_learning_points, ["variables"])

    def test_multiple_learning_points(self):
        second_point = LearningPoint(
            "functions",
            "Understanding functions and their usage"
        )
        exercises = asyncio.run(
            self.llm_service.generate_exercises(
                learning_points=[self.learning_point, second_point],
                count=1
            )
        )
        self.assertEqual(len(exercises), 2)  # One exercise per learning point
        self.assertIn("variables", exercises[0].question)
        self.assertIn("functions", exercises[1].question)

    def test_different_difficulty_levels(self):
        exercises = asyncio.run(
            self.llm_service.generate_exercises(
                learning_points=[self.learning_point],
                count=1,
                difficulty="advanced"
            )
        )
        self.assertEqual(exercises[0].difficulty_level, "advanced")

    def test_different_exercise_types(self):
        exercises = asyncio.run(
            self.llm_service.generate_exercises(
                learning_points=[self.learning_point],
                count=1,
                exercise_type="multiple_choice"
            )
        )
        self.assertEqual(exercises[0].exercise_type, "multiple_choice")

    def test_zero_count(self):
        exercises = asyncio.run(
            self.llm_service.generate_exercises(
                learning_points=[self.learning_point],
                count=0
            )
        )
        self.assertEqual(len(exercises), 0)

    def test_empty_learning_points(self):
        exercises = asyncio.run(
            self.llm_service.generate_exercises(
                learning_points=[],
                count=1
            )
        )
        self.assertEqual(len(exercises), 0)

if __name__ == '__main__':
    unittest.main()
