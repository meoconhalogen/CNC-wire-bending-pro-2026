"""
Unit tests for DXF Parser module
"""

import unittest
import tempfile
import os
from src.dxf_parser import (
    DXFParser, Point, LineSegment, CircleEntity, ArcEntity, PolylineEntity
)


class TestPoint(unittest.TestCase):
    """Test Point dataclass"""
    
    def test_point_creation(self):
        """Test point creation"""
        p = Point(1.5, 2.5, 3.5)
        self.assertEqual(p.x, 1.5)
        self.assertEqual(p.y, 2.5)
        self.assertEqual(p.z, 3.5)
    
    def test_point_repr(self):
        """Test point string representation"""
        p = Point(1.0, 2.0, 3.0)
        repr_str = repr(p)
        self.assertIn('1.000', repr_str)
        self.assertIn('2.000', repr_str)
        self.assertIn('3.000', repr_str)


class TestLineSegment(unittest.TestCase):
    """Test LineSegment dataclass"""
    
    def test_line_segment_creation(self):
        """Test line segment creation"""
        p1 = Point(0, 0)
        p2 = Point(10, 10)
        line = LineSegment(p1, p2)
        
        self.assertEqual(line.start, p1)
        self.assertEqual(line.end, p2)


class TestCircleEntity(unittest.TestCase):
    """Test CircleEntity dataclass"""
    
    def test_circle_creation(self):
        """Test circle creation"""
        center = Point(5, 5)
        circle = CircleEntity(center, 10)
        
        self.assertEqual(circle.center, center)
        self.assertEqual(circle.radius, 10)


class TestArcEntity(unittest.TestCase):
    """Test ArcEntity dataclass"""
    
    def test_arc_creation(self):
        """Test arc creation"""
        center = Point(0, 0)
        arc = ArcEntity(center, 5, 0, 90)
        
        self.assertEqual(arc.center, center)
        self.assertEqual(arc.radius, 5)
        self.assertEqual(arc.start_angle, 0)
        self.assertEqual(arc.end_angle, 90)


class TestPolylineEntity(unittest.TestCase):
    """Test PolylineEntity dataclass"""
    
    def test_polyline_creation(self):
        """Test polyline creation"""
        points = [Point(0, 0), Point(1, 0), Point(1, 1)]
        poly = PolylineEntity(points, is_closed=False)
        
        self.assertEqual(len(poly.points), 3)
        self.assertFalse(poly.is_closed)


class TestDXFParser(unittest.TestCase):
    """Test DXF Parser"""
    
    def test_parser_initialization(self):
        """Test parser initialization"""
        parser = DXFParser('test.dxf')
        self.assertEqual(parser.filepath, 'test.dxf')
        self.assertIsNone(parser.doc)
        self.assertEqual(len(parser.entities), 0)
    
    def test_get_entity_count_empty(self):
        """Test entity count for empty parser"""
        parser = DXFParser('test.dxf')
        self.assertEqual(parser.get_entity_count(), 0)
    
    def test_bounds_calculation(self):
        """Test bounds calculation"""
        parser = DXFParser('test.dxf')
        parser.entities = [
            LineSegment(Point(0, 0), Point(10, 10)),
            LineSegment(Point(5, 5), Point(15, 15))
        ]
        parser._calculate_bounds()
        
        self.assertIsNotNone(parser.bounds)
        self.assertEqual(parser.bounds['min_x'], 0)
        self.assertEqual(parser.bounds['max_x'], 15)
        self.assertEqual(parser.bounds['min_y'], 0)
        self.assertEqual(parser.bounds['max_y'], 15)


if __name__ == '__main__':
    unittest.main()
