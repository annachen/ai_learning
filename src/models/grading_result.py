from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class GradingResult:
    """Represents the result of grading a student's answer."""
    score: float  # Score between 0 and 100
    feedback: str  # Detailed feedback for the student
    metadata: Dict[str, Any]  # Additional information about the grading (e.g., areas of improvement, mastery level)
    confidence: float = 1.0  # LLM's confidence in its grading (0-1)

    def __post_init__(self):
        if not 0 <= self.score <= 100:
            raise ValueError("Score must be between 0 and 100")
        if not 0 <= self.confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1")
        if not self.metadata:
            self.metadata = {}
