import unittest
from src.learning_point import LearningPoint

class TestLearningPoint(unittest.TestCase):
    def setUp(self):
        self.learning_point = LearningPoint("variables", "Understanding variables in programming")
        
    def test_initialization(self):
        self.assertEqual(self.learning_point.name, "variables")
        self.assertEqual(self.learning_point.description, "Understanding variables in programming")
        self.assertEqual(len(self.learning_point.topics), 0)
        
    def test_add_topic(self):
        self.learning_point.add_topic("Python Basics")
        self.assertIn("Python Basics", self.learning_point.topics)
        
    def test_remove_topic(self):
        self.learning_point.add_topic("Python Basics")
        self.learning_point.remove_topic("Python Basics")
        self.assertNotIn("Python Basics", self.learning_point.topics)
        
    def test_remove_nonexistent_topic(self):
        # Should not raise an error
        self.learning_point.remove_topic("Nonexistent Topic")
        
    def test_get_topics(self):
        self.learning_point.add_topic("Python Basics")
        self.learning_point.add_topic("Variables")
        topics = self.learning_point.get_topics()
        self.assertEqual(len(topics), 2)
        self.assertIn("Python Basics", topics)
        self.assertIn("Variables", topics)
        
    def test_get_topics_returns_copy(self):
        self.learning_point.add_topic("Python Basics")
        topics = self.learning_point.get_topics()
        topics.add("New Topic")
        self.assertNotIn("New Topic", self.learning_point.topics)

if __name__ == '__main__':
    unittest.main()
