from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Exercise:
    """Represents an educational exercise or question."""
    question: str
    expected_answer: Optional[str] = None
    explanation: Optional[str] = None
    difficulty_level: Optional[str] = None  # e.g., "beginner", "intermediate", "advanced"
    exercise_type: Optional[str] = None  # e.g., "multiple_choice", "open_ended", "coding"
    related_learning_points: List[str] = None

    def __post_init__(self):
        if self.related_learning_points is None:
            self.related_learning_points = []
