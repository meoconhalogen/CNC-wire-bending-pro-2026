"""
Unit tests for Geometry module
"""

import unittest
import math
from src.dxf_parser import Point
from src.geometry import Geometry


class TestPoint(unittest.TestCase):
    """Test Point class"""
    
    def test_point_creation(self):
        """Test point creation"""
        p = Point(1.0, 2.0, 3.0)
        self.assertEqual(p.x, 1.0)
        self.assertEqual(p.y, 2.0)
        self.assertEqual(p.z, 3.0)
    
    def test_point_default_z(self):
        """Test point with default Z"""
        p = Point(1.0, 2.0)
        self.assertEqual(p.z, 0.0)


class TestGeometry(unittest.TestCase):
    """Test Geometry utilities"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.p1 = Point(0, 0)
        self.p2 = Point(3, 4)
        self.p3 = Point(5, 0)
        self.p4 = Point(10, 0)
    
    def test_distance_2d(self):
        """Test 2D distance calculation"""
        dist = Geometry.distance_2d(self.p1, self.p2)
        self.assertAlmostEqual(dist, 5.0, places=5)
    
    def test_distance_3d(self):
        """Test 3D distance calculation"""
        p1 = Point(0, 0, 0)
        p2 = Point(1, 1, 1)
        dist = Geometry.distance(p1, p2)
        expected = math.sqrt(3)
        self.assertAlmostEqual(dist, expected, places=5)
    
    def test_angle(self):
        """Test angle calculation"""
        # Horizontal line (0 degrees)
        angle = Geometry.angle(self.p1, self.p3)
        self.assertAlmostEqual(angle, 0, places=5)
        
        # 90 degrees
        p_up = Point(0, 10)
        angle = Geometry.angle(self.p1, p_up)
        self.assertAlmostEqual(angle, 90, places=5)
    
    def test_angle_between_points(self):
        """Test angle between three points"""
        # Right angle: 90 degrees
        p1 = Point(0, 0)
        p2 = Point(1, 0)
        p3 = Point(1, 1)
        angle = Geometry.angle_between(p1, p2, p3)
        self.assertAlmostEqual(angle, 90, places=5)
    
    def test_point_on_circle(self):
        """Test point on circle calculation"""
        center = Point(0, 0)
        radius = 10
        
        # 0 degrees
        p = Geometry.point_on_circle(center, radius, 0)
        self.assertAlmostEqual(p.x, 10, places=5)
        self.assertAlmostEqual(p.y, 0, places=5)
        
        # 90 degrees
        p = Geometry.point_on_circle(center, radius, 90)
        self.assertAlmostEqual(p.x, 0, places=5)
        self.assertAlmostEqual(p.y, 10, places=5)
    
    def test_point_on_line(self):
        """Test interpolation on line"""
        p1 = Point(0, 0)
        p2 = Point(10, 10)
        
        # Midpoint
        p = Geometry.point_on_line(p1, p2, 0.5)
        self.assertAlmostEqual(p.x, 5, places=5)
        self.assertAlmostEqual(p.y, 5, places=5)
        
        # Start point
        p = Geometry.point_on_line(p1, p2, 0)
        self.assertAlmostEqual(p.x, 0, places=5)
        self.assertAlmostEqual(p.y, 0, places=5)
        
        # End point
        p = Geometry.point_on_line(p1, p2, 1)
        self.assertAlmostEqual(p.x, 10, places=5)
        self.assertAlmostEqual(p.y, 10, places=5)
    
    def test_line_intersection(self):
        """Test line intersection"""
        # Perpendicular lines
        p1 = Point(0, 0)
        p2 = Point(10, 0)
        p3 = Point(5, -5)
        p4 = Point(5, 5)
        
        found, point = Geometry.line_intersection(p1, p2, p3, p4)
        self.assertTrue(found)
        self.assertAlmostEqual(point.x, 5, places=5)
        self.assertAlmostEqual(point.y, 0, places=5)
        
        # Parallel lines
        p1 = Point(0, 0)
        p2 = Point(10, 0)
        p3 = Point(0, 1)
        p4 = Point(10, 1)
        
        found, point = Geometry.line_intersection(p1, p2, p3, p4)
        self.assertFalse(found)
    
    def test_point_to_line_distance(self):
        """Test distance from point to line"""
        p1 = Point(0, 0)
        p2 = Point(10, 0)
        p_test = Point(5, 5)
        
        dist = Geometry.point_to_line_distance(p_test, p1, p2)
        self.assertAlmostEqual(dist, 5, places=5)
    
    def test_rotate_point(self):
        """Test point rotation"""
        center = Point(0, 0)
        point = Point(10, 0)
        
        # Rotate 90 degrees
        rotated = Geometry.rotate_point(point, center, 90)
        self.assertAlmostEqual(rotated.x, 0, places=5)
        self.assertAlmostEqual(rotated.y, 10, places=5)
        
        # Rotate 180 degrees
        rotated = Geometry.rotate_point(point, center, 180)
        self.assertAlmostEqual(rotated.x, -10, places=5)
        self.assertAlmostEqual(rotated.y, 0, places=5)
    
    def test_arc_length(self):
        """Test arc length calculation"""
        radius = 10
        # Quarter circle
        length = Geometry.arc_length(radius, 0, 90)
        expected = math.pi * radius / 2
        self.assertAlmostEqual(length, expected, places=5)


if __name__ == '__main__':
    unittest.main()
