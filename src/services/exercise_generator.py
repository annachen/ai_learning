from typing import List, Optional
from .llm_service import LLMService
from ..models.exercise import Exercise
from ..learning_point import LearningPoint

class ExerciseGenerator:
    """Service for generating educational exercises using LLM."""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
        
    async def generate_exercises_for_learning_points(
        self,
        learning_points: List[LearningPoint],
        count_per_point: int = 1,
        difficulty: str = "intermediate",
        exercise_type: str = "open_ended"
    ) -> List[Exercise]:
        """
        Generate exercises for a list of learning points.
        
        Args:
            learning_points: List of LearningPoint objects to generate exercises for
            count_per_point: Number of exercises to generate per learning point
            difficulty: Desired difficulty level ("beginner", "intermediate", "advanced")
            exercise_type: Type of exercise to generate ("multiple_choice", "open_ended", "coding")
            
        Returns:
            List of Exercise objects
            
        Raises:
            ValueError: If count_per_point is less than 0
        """
        if count_per_point < 0:
            raise ValueError("count_per_point must be non-negative")
        exercises = []
        for point in learning_points:
            point_exercises = await self.llm_service.generate_exercises(
                learning_points=[point],
                count=count_per_point,
                difficulty=difficulty,
                exercise_type=exercise_type
            )
            exercises.extend(point_exercises)
        return exercises
