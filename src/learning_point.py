from typing import List, Set

class LearningPoint:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.topics: Set[str] = set()
        
    def add_topic(self, topic: str) -> None:
        """Add a topic to this learning point."""
        self.topics.add(topic)
        
    def remove_topic(self, topic: str) -> None:
        """Remove a topic from this learning point."""
        self.topics.discard(topic)
        
    def get_topics(self) -> Set[str]:
        """Get all topics associated with this learning point."""
        return self.topics.copy()
        
    def __str__(self) -> str:
        return f"LearningPoint(name='{self.name}', topics={self.topics})"
