from typing import List, Dict, Any
from .llm_service import LLMService
from ..models.exercise import Exercise
from ..models.grading_result import GradingResult
from ..learning_point import LearningPoint

class MockLLMService(LLMService):
    """Mock implementation of LLM service for testing and demonstration."""
    
    async def generate_exercises(self,
                               learning_points: List[LearningPoint],
                               count: int = 1,
                               difficulty: str = "intermediate",
                               exercise_type: str = "open_ended") -> List[Exercise]:
        """
        Mock implementation that generates simple exercises.
        Replace this with actual LLM implementation.
        """
        exercises = []
        for _ in range(count):
            for point in learning_points:
                exercise = Exercise(
                    question=f"Explain the concept of {point.name} in your own words.",
                    expected_answer=None,  # LLM would generate this
                    explanation=f"This question tests understanding of {point.description}",
                    difficulty_level=difficulty,
                    exercise_type=exercise_type,
                    related_learning_points=[point.name]
                )
                exercises.append(exercise)
        return exercises
        
    async def grade_answer(self,
                          problem: str,
                          student_answer: str,
                          expected_answer: str = None,
                          metadata: Dict[str, Any] = None) -> GradingResult:
        """Mock implementation of answer grading."""
        return GradingResult(
            score=75.0,
            feedback="Mock grading feedback",
            metadata={
                "key_concepts_understood": ["mock concept"],
                "areas_for_improvement": ["mock area"],
                "mastery_level": "intermediate"
            },
            confidence=1.0
        )
        exercises = []
        for _ in range(count):
            for point in learning_points:
                exercise = Exercise(
                    question=f"Explain the concept of {point.name} in your own words.",
                    expected_answer=None,  # LLM would generate this
                    explanation=f"This question tests understanding of {point.description}",
                    difficulty_level=difficulty,
                    exercise_type=exercise_type,
                    related_learning_points=[point.name]
                )
                exercises.append(exercise)
        return exercises
