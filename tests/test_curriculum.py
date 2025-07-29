import unittest
from src.curriculum import Curriculum
from src.topic import Topic
from src.learning_point import LearningPoint

class TestCurriculum(unittest.TestCase):
    def setUp(self):
        self.curriculum = Curriculum()
        
    def test_initialization(self):
        self.assertEqual(len(self.curriculum.topics), 0)
        self.assertEqual(len(self.curriculum.learning_points), 0)
        
    def test_add_topic(self):
        topic = self.curriculum.add_topic("Python Basics", "Introduction to Python")
        self.assertIn("Python Basics", self.curriculum.topics)
        self.assertEqual(topic.description, "Introduction to Python")
        
    def test_add_duplicate_topic(self):
        topic1 = self.curriculum.add_topic("Python Basics")
        topic2 = self.curriculum.add_topic("Python Basics")
        self.assertEqual(topic1, topic2)
        self.assertEqual(len(self.curriculum.topics), 1)
        
    def test_add_learning_point(self):
        learning_point = self.curriculum.add_learning_point("variables", "Understanding variables")
        self.assertIn("variables", self.curriculum.learning_points)
        self.assertEqual(learning_point.description, "Understanding variables")
        
    def test_add_duplicate_learning_point(self):
        point1 = self.curriculum.add_learning_point("variables", "First description")
        point2 = self.curriculum.add_learning_point("variables", "Second description")
        self.assertEqual(point1, point2)
        self.assertEqual(len(self.curriculum.learning_points), 1)
        
    def test_assign_prerequisite(self):
        self.curriculum.add_topic("Functions")
        self.curriculum.add_topic("Variables")
        self.curriculum.assign_prerequisite("Functions", "Variables")
        self.assertIn("Variables", self.curriculum.topics["Functions"].prerequisites)
        
    def test_assign_nonexistent_prerequisite(self):
        self.curriculum.add_topic("Functions")
        # Should not raise an error
        self.curriculum.assign_prerequisite("Functions", "NonexistentTopic")
        self.assertNotIn("NonexistentTopic", self.curriculum.topics["Functions"].prerequisites)
        
    def test_assign_learning_point_to_topic(self):
        self.curriculum.add_topic("Variables")
        self.curriculum.add_learning_point("variable_declaration", "How to declare variables")
        self.curriculum.assign_learning_point_to_topic("variable_declaration", "Variables")
        
        topic = self.curriculum.topics["Variables"]
        learning_point = self.curriculum.learning_points["variable_declaration"]
        
        self.assertIn(learning_point, topic.learning_points)
        self.assertIn("Variables", learning_point.topics)
        
    def test_get_topic_prerequisites(self):
        self.curriculum.add_topic("Functions")
        self.curriculum.add_topic("Variables")
        self.curriculum.add_topic("Classes")
        
        self.curriculum.assign_prerequisite("Functions", "Variables")
        self.curriculum.assign_prerequisite("Classes", "Functions")
        
        prereqs = self.curriculum.get_topic_prerequisites("Functions")
        self.assertIn("Variables", prereqs)
        
    def test_get_topic_learning_points(self):
        self.curriculum.add_topic("Variables")
        point1 = self.curriculum.add_learning_point("var_declaration", "Declaration")
        point2 = self.curriculum.add_learning_point("var_types", "Types")
        
        self.curriculum.assign_learning_point_to_topic("var_declaration", "Variables")
        self.curriculum.assign_learning_point_to_topic("var_types", "Variables")
        
        learning_points = self.curriculum.get_topic_learning_points("Variables")
        self.assertEqual(len(learning_points), 2)
        self.assertIn(point1, learning_points)
        self.assertIn(point2, learning_points)

if __name__ == '__main__':
    unittest.main()
