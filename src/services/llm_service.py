from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..models.exercise import Exercise
from ..models.grading_result import GradingResult
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

    @abstractmethod
    async def grade_answer(self,
                          problem: str,
                          student_answer: str,
                          expected_answer: str = None,
                          metadata: Dict[str, Any] = None) -> GradingResult:
        """
        Grade a student's answer using the LLM.
        
        Args:
            problem: The question or problem statement
            student_answer: The student's answer to grade
            expected_answer: The expected or model answer (optional)
            metadata: Additional context for grading, such as:
                     - topic: The topic being tested
                     - difficulty: The difficulty level
                     - student_level: The student's current level
                     - previous_attempts: Number of previous attempts
                     - time_spent: Time spent on the answer
                     
        Returns:
            GradingResult containing score, feedback, and metadata
        """
        pass
