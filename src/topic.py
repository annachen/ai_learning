from typing import List, Set, Dict
from .learning_point import LearningPoint

class Topic:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.prerequisites: Set[str] = set()
        self.learning_points: List[LearningPoint] = []
        
    def add_prerequisite(self, prerequisite: str) -> None:
        """Add a prerequisite topic that must be completed before this one."""
        self.prerequisites.add(prerequisite)
        
    def remove_prerequisite(self, prerequisite: str) -> None:
        """Remove a prerequisite topic."""
        self.prerequisites.discard(prerequisite)
        
    def add_learning_point(self, learning_point: LearningPoint) -> None:
        """Add a learning point to this topic."""
        if learning_point not in self.learning_points:
            self.learning_points.append(learning_point)
            learning_point.add_topic(self.name)
            
    def remove_learning_point(self, learning_point: LearningPoint) -> None:
        """Remove a learning point from this topic."""
        if learning_point in self.learning_points:
            self.learning_points.remove(learning_point)
            learning_point.remove_topic(self.name)
            
    def get_prerequisites(self) -> Set[str]:
        """Get all prerequisite topics."""
        return self.prerequisites.copy()
        
    def get_learning_points(self) -> List[LearningPoint]:
        """Get all learning points associated with this topic."""
        return self.learning_points.copy()
        
    def __str__(self) -> str:
        return f"Topic(name='{self.name}', prerequisites={self.prerequisites}, learning_points={len(self.learning_points)})"
