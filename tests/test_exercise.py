import unittest
from dataclasses import asdict
from src.models.exercise import Exercise

class TestExercise(unittest.TestCase):
    def setUp(self):
        self.exercise_data = {
            "question": "What is a variable?",
            "expected_answer": "A variable is a named storage location.",
            "explanation": "Tests basic understanding of variables.",
            "difficulty_level": "beginner",
            "exercise_type": "open_ended",
            "related_learning_points": ["variables", "data_types"]
        }
        
    def test_exercise_initialization(self):
        exercise = Exercise(**self.exercise_data)
        self.assertEqual(exercise.question, self.exercise_data["question"])
        self.assertEqual(exercise.expected_answer, self.exercise_data["expected_answer"])
        self.assertEqual(exercise.explanation, self.exercise_data["explanation"])
        self.assertEqual(exercise.difficulty_level, self.exercise_data["difficulty_level"])
        self.assertEqual(exercise.exercise_type, self.exercise_data["exercise_type"])
        self.assertEqual(exercise.related_learning_points, self.exercise_data["related_learning_points"])
        
    def test_exercise_initialization_with_minimal_data(self):
        exercise = Exercise(question="What is a loop?")
        self.assertEqual(exercise.question, "What is a loop?")
        self.assertIsNone(exercise.expected_answer)
        self.assertIsNone(exercise.explanation)
        self.assertIsNone(exercise.difficulty_level)
        self.assertIsNone(exercise.exercise_type)
        self.assertEqual(exercise.related_learning_points, [])
        
    def test_exercise_asdict(self):
        exercise = Exercise(**self.exercise_data)
        exercise_dict = asdict(exercise)
        self.assertEqual(exercise_dict, self.exercise_data)

if __name__ == '__main__':
    unittest.main()
