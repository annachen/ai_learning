import unittest
import asyncio
from src.services.exercise_generator import ExerciseGenerator
from src.services.mock_llm_service import MockLLMService
from src.learning_point import LearningPoint
from src.models.exercise import Exercise

class TestExerciseGenerator(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MockLLMService()
        self.generator = ExerciseGenerator(self.mock_llm)
        self.learning_point = LearningPoint(
            "variables", 
            "Understanding variables in programming"
        )

    def test_initialization(self):
        self.assertIsInstance(self.generator.llm_service, MockLLMService)

    def test_generate_exercises_basic(self):
        exercises = asyncio.run(
            self.generator.generate_exercises_for_learning_points(
                learning_points=[self.learning_point],
                count_per_point=2
            )
        )
        self.assertEqual(len(exercises), 2)
        self.assertTrue(all(isinstance(ex, Exercise) for ex in exercises))
        self.assertTrue(
            all("variables" in ex.related_learning_points for ex in exercises)
        )

    def test_generate_exercises_multiple_points(self):
        second_point = LearningPoint(
            "functions",
            "Understanding functions and their usage"
        )
        exercises = asyncio.run(
            self.generator.generate_exercises_for_learning_points(
                learning_points=[self.learning_point, second_point],
                count_per_point=1
            )
        )
        self.assertEqual(len(exercises), 2)
        learning_point_names = {
            lp for ex in exercises for lp in ex.related_learning_points
        }
        self.assertEqual(learning_point_names, {"variables", "functions"})

    def test_generate_exercises_with_difficulty(self):
        exercises = asyncio.run(
            self.generator.generate_exercises_for_learning_points(
                learning_points=[self.learning_point],
                count_per_point=1,
                difficulty="advanced"
            )
        )
        self.assertTrue(
            all(ex.difficulty_level == "advanced" for ex in exercises)
        )

    def test_generate_exercises_with_type(self):
        exercises = asyncio.run(
            self.generator.generate_exercises_for_learning_points(
                learning_points=[self.learning_point],
                count_per_point=1,
                exercise_type="multiple_choice"
            )
        )
        self.assertTrue(
            all(ex.exercise_type == "multiple_choice" for ex in exercises)
        )

    def test_generate_exercises_empty_points(self):
        exercises = asyncio.run(
            self.generator.generate_exercises_for_learning_points(
                learning_points=[],
                count_per_point=1
            )
        )
        self.assertEqual(len(exercises), 0)

    def test_invalid_count_per_point(self):
        with self.assertRaises(ValueError):
            asyncio.run(
                self.generator.generate_exercises_for_learning_points(
                    learning_points=[self.learning_point],
                    count_per_point=-1
                )
            )

if __name__ == '__main__':
    unittest.main()
