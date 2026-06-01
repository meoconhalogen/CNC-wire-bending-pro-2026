"""
Unit tests for Path Optimizer module
"""

import unittest
from src.dxf_parser import Point, LineSegment
from src.path_optimizer import PathOptimizer


class TestPathOptimizer(unittest.TestCase):
    """Test Path Optimizer"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.optimizer = PathOptimizer(tolerance=0.1)
    
    def test_optimizer_initialization(self):
        """Test optimizer initialization"""
        self.assertEqual(self.optimizer.tolerance, 0.1)
        self.assertEqual(len(self.optimizer.optimized_entities), 0)
    
    def test_optimize_empty_list(self):
        """Test optimization of empty entity list"""
        result = self.optimizer.optimize([])
        self.assertEqual(len(result), 0)
    
    def test_optimize_single_segment(self):
        """Test optimization with single segment"""
        entities = [LineSegment(Point(0, 0), Point(10, 10))]
        result = self.optimizer.optimize(entities)
        self.assertEqual(len(result), 1)
    
    def test_calculate_total_length(self):
        """Test total length calculation"""
        segments = [
            LineSegment(Point(0, 0), Point(3, 0)),
            LineSegment(Point(3, 0), Point(3, 4))
        ]
        length = self.optimizer.calculate_total_length(segments)
        # 3 + 4 = 7
        self.assertAlmostEqual(length, 7.0, places=5)
    
    def test_get_statistics_empty(self):
        """Test statistics for empty optimizer"""
        stats = self.optimizer.get_statistics()
        self.assertEqual(len(stats), 0)
    
    def test_get_statistics_with_segments(self):
        """Test statistics with segments"""
        segments = [
            LineSegment(Point(0, 0), Point(10, 0)),
            LineSegment(Point(10, 0), Point(10, 10))
        ]
        self.optimizer.optimized_entities = segments
        stats = self.optimizer.get_statistics()
        
        self.assertEqual(stats['num_segments'], 2)
        self.assertAlmostEqual(stats['total_length'], 20.0, places=5)
        self.assertAlmostEqual(stats['avg_segment_length'], 10.0, places=5)
    
    def test_convert_to_segments(self):
        """Test conversion of entities to segments"""
        entities = [
            LineSegment(Point(0, 0), Point(10, 0)),
            LineSegment(Point(10, 0), Point(10, 10))
        ]
        segments = self.optimizer._convert_to_segments(entities)
        self.assertEqual(len(segments), 2)


if __name__ == '__main__':
    unittest.main()
