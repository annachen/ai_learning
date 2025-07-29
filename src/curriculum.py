from typing import Dict, Set, List
from .topic import Topic
from .learning_point import LearningPoint

class Curriculum:
    def __init__(self):
        self.topics: Dict[str, Topic] = {}
        self.learning_points: Dict[str, LearningPoint] = {}
        
    def add_topic(self, name: str, description: str = "") -> Topic:
        """Add a new topic to the curriculum."""
        if name not in self.topics:
            self.topics[name] = Topic(name, description)
        return self.topics[name]
        
    def add_learning_point(self, name: str, description: str) -> LearningPoint:
        """Add a new learning point to the curriculum."""
        if name not in self.learning_points:
            self.learning_points[name] = LearningPoint(name, description)
        return self.learning_points[name]
        
    def assign_prerequisite(self, topic: str, prerequisite: str) -> None:
        """Assign a prerequisite to a topic."""
        if topic in self.topics and prerequisite in self.topics:
            self.topics[topic].add_prerequisite(prerequisite)
            
    def assign_learning_point_to_topic(self, learning_point_name: str, topic_name: str) -> None:
        """Assign a learning point to a topic."""
        if learning_point_name in self.learning_points and topic_name in self.topics:
            self.topics[topic_name].add_learning_point(self.learning_points[learning_point_name])
            
    def get_topic_prerequisites(self, topic_name: str) -> Set[str]:
        """Get all prerequisites for a given topic."""
        if topic_name in self.topics:
            return self.topics[topic_name].get_prerequisites()
        return set()
        
    def get_topic_learning_points(self, topic_name: str) -> List[LearningPoint]:
        """Get all learning points for a given topic."""
        if topic_name in self.topics:
            return self.topics[topic_name].get_learning_points()
        return []
        
    def __str__(self) -> str:
        return f"Curriculum(topics={len(self.topics)}, learning_points={len(self.learning_points)})"
