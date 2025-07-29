import unittest
from src.topic import Topic
from src.learning_point import LearningPoint

class TestTopic(unittest.TestCase):
    def setUp(self):
        self.topic = Topic("Python Basics", "Introduction to Python programming")
        self.learning_point = LearningPoint("variables", "Understanding variables")
        
    def test_initialization(self):
        self.assertEqual(self.topic.name, "Python Basics")
        self.assertEqual(self.topic.description, "Introduction to Python programming")
        self.assertEqual(len(self.topic.prerequisites), 0)
        self.assertEqual(len(self.topic.learning_points), 0)
        
    def test_add_prerequisite(self):
        self.topic.add_prerequisite("Computer Fundamentals")
        self.assertIn("Computer Fundamentals", self.topic.prerequisites)
        
    def test_remove_prerequisite(self):
        self.topic.add_prerequisite("Computer Fundamentals")
        self.topic.remove_prerequisite("Computer Fundamentals")
        self.assertNotIn("Computer Fundamentals", self.topic.prerequisites)
        
    def test_add_learning_point(self):
        self.topic.add_learning_point(self.learning_point)
        self.assertIn(self.learning_point, self.topic.learning_points)
        self.assertIn(self.topic.name, self.learning_point.topics)
        
    def test_add_duplicate_learning_point(self):
        self.topic.add_learning_point(self.learning_point)
        initial_length = len(self.topic.learning_points)
        self.topic.add_learning_point(self.learning_point)
        self.assertEqual(len(self.topic.learning_points), initial_length)
        
    def test_remove_learning_point(self):
        self.topic.add_learning_point(self.learning_point)
        self.topic.remove_learning_point(self.learning_point)
        self.assertNotIn(self.learning_point, self.topic.learning_points)
        self.assertNotIn(self.topic.name, self.learning_point.topics)
        
    def test_get_prerequisites(self):
        self.topic.add_prerequisite("Computer Fundamentals")
        self.topic.add_prerequisite("Basic Math")
        prereqs = self.topic.get_prerequisites()
        self.assertEqual(len(prereqs), 2)
        self.assertIn("Computer Fundamentals", prereqs)
        self.assertIn("Basic Math", prereqs)
        
    def test_get_prerequisites_returns_copy(self):
        self.topic.add_prerequisite("Computer Fundamentals")
        prereqs = self.topic.get_prerequisites()
        prereqs.add("New Prerequisite")
        self.assertNotIn("New Prerequisite", self.topic.prerequisites)

if __name__ == '__main__':
    unittest.main()
