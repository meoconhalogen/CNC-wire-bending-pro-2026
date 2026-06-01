"""
Unit tests for G-code Generator module
"""

import unittest
import tempfile
import os
from src.dxf_parser import Point, LineSegment
from src.gcode_generator import GCodeGenerator, GCodeFormat


class TestGCodeGenerator(unittest.TestCase):
    """Test G-code Generator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = GCodeGenerator()
    
    def test_generator_initialization(self):
        """Test generator initialization"""
        self.assertIsNotNone(self.generator.config)
        self.assertEqual(self.generator.current_position, Point(0, 0, 0))
        self.assertEqual(self.generator.total_distance, 0)
    
    def test_load_default_config(self):
        """Test loading default configuration"""
        config = self.generator._load_config(None)
        self.assertIn('machine', config)
        self.assertIn('output', config)
    
    def test_format_coordinate(self):
        """Test coordinate formatting"""
        formatted = self.generator._format_coord(1.23456)
        self.assertEqual(formatted, '1.235')  # 3 decimal places
    
    def test_generate_empty_segments(self):
        """Test generation with empty segments"""
        gcode = self.generator.generate([])
        self.assertIn('CNC Wire Bending Program', gcode)
        self.assertIn('G21', gcode)  # Metric
        self.assertIn('G90', gcode)  # Absolute
    
    def test_generate_single_segment(self):
        """Test generation with single segment"""
        segments = [LineSegment(Point(0, 0), Point(10, 10))]
        gcode = self.generator.generate(segments)
        
        self.assertIn('G00', gcode)  # Rapid move
        self.assertIn('G01', gcode)  # Linear move
        self.assertIn('M30', gcode)  # End program
    
    def test_save_gcode(self):
        """Test saving G-code to file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, 'test.gcode')
            gcode_content = "G00 X0 Y0\nG01 X10 Y10\nM30"
            
            self.generator.save_gcode(gcode_content, filepath)
            
            self.assertTrue(os.path.exists(filepath))
            with open(filepath, 'r') as f:
                content = f.read()
                self.assertEqual(content, gcode_content)
    
    def test_calculate_distance(self):
        """Test distance calculation"""
        p1 = Point(0, 0, 0)
        p2 = Point(3, 4, 0)
        dist = self.generator._calculate_distance(p1, p2)
        self.assertAlmostEqual(dist, 5.0, places=5)


class TestGCodeFormat(unittest.TestCase):
    """Test G-code format definitions"""
    
    def test_fanuc_format(self):
        """Test Fanuc format"""
        self.assertEqual(GCodeFormat.FANUC['name'], 'Fanuc')
        self.assertEqual(GCodeFormat.FANUC['rapid'], 'G00')
        self.assertEqual(GCodeFormat.FANUC['linear'], 'G01')
    
    def test_siemens_format(self):
        """Test Siemens format"""
        self.assertEqual(GCodeFormat.SIEMENS['name'], 'Siemens Sinumerik')
        self.assertEqual(GCodeFormat.SIEMENS['rapid'], 'G00')
    
    def test_heidenhain_format(self):
        """Test Heidenhain format"""
        self.assertEqual(GCodeFormat.HEIDENHAIN['name'], 'Heidenhain iTNC 530')
        self.assertEqual(GCodeFormat.HEIDENHAIN['rapid'], 'G00')


if __name__ == '__main__':
    unittest.main()
