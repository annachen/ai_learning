from abc import ABC, abstractmethod
from typing import List
from ..models.exercise import Exercise
from ..learning_point import LearningPoint

class LLMService(ABC):
    """Abstract base class for LLM service implementations."""
    
    @abstractmethod
    async def generate_exercises(self, 
                               learning_points: List[LearningPoint], 
                               count: int = 1,
                               difficulty: str = "intermediate",
                               exercise_type: str = "open_ended") -> List[Exercise]:
        """
        Generate exercises based on given learning points.
        
        Args:
            learning_points: List of LearningPoint objects to generate exercises for
            count: Number of exercises to generate
            difficulty: Desired difficulty level ("beginner", "intermediate", "advanced")
            exercise_type: Type of exercise to generate ("multiple_choice", "open_ended", "coding")
            
        Returns:
            List of Exercise objects
        """
        pass
