"""
Tests for the explanation_generator module.
"""
import sys
import os
import unittest

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

from src.explanation_generator import generate_simple_explanation

class TestExplanationGenerator(unittest.TestCase):
    """Test cases for the explanation generator module."""
    
    def test_generate_simple_explanation_with_abstract(self):
        """Test generating an explanation when an abstract is available."""
        title = "Deep Learning for Computer Vision"
        abstract = "This paper presents a novel approach to computer vision using deep learning."
        explanation = generate_simple_explanation(title, abstract)
        
        # Check that the explanation contains the title
        self.assertIn("deep learning for computer vision", explanation.lower())
        
        # Check that the explanation contains part of the abstract
        self.assertIn("novel approach", explanation.lower())
    
    def test_generate_simple_explanation_without_abstract(self):
        """Test generating an explanation when no abstract is available."""
        title = "Deep Learning for Computer Vision"
        abstract = "Abstract not available"
        explanation = generate_simple_explanation(title, abstract)
        
        # Check that the explanation contains the title
        self.assertIn("deep learning for computer vision", explanation.lower())
        
        # Check that the explanation contains a generic phrase
        self.assertIn("new approaches", explanation.lower())

if __name__ == '__main__':
    unittest.main() 