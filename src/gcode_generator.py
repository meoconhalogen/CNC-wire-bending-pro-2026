"""
G-code Generator Module
Converts optimized paths to CNC machine G-code
"""

import logging
from typing import List, Any
from datetime import datetime
import yaml

from src.dxf_parser import LineSegment, Point

logger = logging.getLogger(__name__)


class GCodeGenerator:
    """
    Generates G-code for wire bending CNC machines
    Supports multiple G-code dialects (Fanuc, Siemens, Heidenhain)
    """
    
    def __init__(self, config_file: str = None):
        """
        Initialize G-code generator
        
        Args:
            config_file: Path to YAML config file
        """
        self.config = self._load_config(config_file)
        self.gcode_lines = []
        self.current_position = Point(0, 0, 0)
        self.total_distance = 0
    
    def _load_config(self, config_file: str) -> dict:
        """Load configuration from YAML file"""
        if not config_file:
            # Default configuration
            return {
                'machine': {'max_speed': 100, 'feed_rate': 50},
                'output': {'format': 'fanuc', 'decimal_places': 3, 'include_comments': True}
            }
        
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    
    def generate(self, segments: List[LineSegment]) -> str:
        """
        Generate G-code from segments
        
        Args:
            segments: List of line segments
            
        Returns:
            G-code as string
        """
        self.gcode_lines = []
        self.current_position = Point(0, 0, 0)
        self.total_distance = 0
        
        # Add header
        self._add_header()
        
        # Add startup code
        self._add_startup()
        
        # Generate movement code
        for i, segment in enumerate(segments):
            self._add_segment(segment, i + 1)
        
        # Add shutdown code
        self._add_shutdown()
        
        return '\n'.join(self.gcode_lines)
    
    def _add_header(self):
        """Add file header and comments"""
        self.gcode_lines.append(f"(CNC Wire Bending Program)")
        self.gcode_lines.append(f"(Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        self.gcode_lines.append(f"(Machine: {self.config['machine'].get('name', 'CNC Wire Bender')})")
        self.gcode_lines.append("")
    
    def _add_startup(self):
        """Add startup/initialization code"""
        fmt = self.config['output']['format'].lower()
        
        if fmt == 'fanuc':
            self.gcode_lines.append("G21 (Metric)")
            self.gcode_lines.append("G90 (Absolute positioning)")
            self.gcode_lines.append("G40 (Cancel cutter radius)")
            self.gcode_lines.append(f"F{self.config['machine']['feed_rate']} (Feed rate)")
            self.gcode_lines.append("M3 (Spindle on)")
            self.gcode_lines.append("")
        elif fmt == 'siemens':
            self.gcode_lines.append("G21 (Metric)")
            self.gcode_lines.append("G90 (Absolute)")
            self.gcode_lines.append("")
        elif fmt == 'heidenhain':
            self.gcode_lines.append("BLK FORM 0.1 Z X 0 Y 0 Z 0")
            self.gcode_lines.append("L CYCL DEF 7.0 DATUM")
            self.gcode_lines.append("")
    
    def _add_segment(self, segment: LineSegment, segment_num: int):
        """Add G-code for a single segment"""
        # Rapid move to start point
        self._add_rapid_move(segment.start)
        
        # Linear move to end point
        self._add_linear_move(segment.end)
    
    def _add_rapid_move(self, point: Point):
        """Add rapid positioning move"""
        distance = self._calculate_distance(self.current_position, point)
        
        if distance > 0.001:  # Only if distance is significant
            self._emit_gcode(
                f"G00 X{self._format_coord(point.x)} Y{self._format_coord(point.y)}",
                f"Rapid to ({point.x:.2f}, {point.y:.2f})"
            )
            self.current_position = point
    
    def _add_linear_move(self, point: Point):
        """Add linear feed move"""
        distance = self._calculate_distance(self.current_position, point)
        
        if distance > 0.001:
            self._emit_gcode(
                f"G01 X{self._format_coord(point.x)} Y{self._format_coord(point.y)}",
                f"Move to ({point.x:.2f}, {point.y:.2f}) - {distance:.2f}mm"
            )
            self.current_position = point
            self.total_distance += distance
    
    def _add_shutdown(self):
        """Add shutdown/exit code"""
        fmt = self.config['output']['format'].lower()
        
        self.gcode_lines.append("")
        if fmt == 'fanuc':
            self.gcode_lines.append("M5 (Spindle off)")
            self.gcode_lines.append("G00 X0 Y0 (Return to origin)")
            self.gcode_lines.append("M30 (End program)")
        elif fmt == 'siemens':
            self.gcode_lines.append("M30 (End)")
        elif fmt == 'heidenhain':
            self.gcode_lines.append("M30 (End of program)")
        
        self.gcode_lines.append(f"(Total wire length: {self.total_distance:.2f}mm)")
    
    def _emit_gcode(self, code: str, comment: str = None):
        """Emit a G-code line with optional comment"""
        if comment and self.config['output'].get('include_comments', True):
            self.gcode_lines.append(f"{code:40} ({comment})")
        else:
            self.gcode_lines.append(code)
    
    def _format_coord(self, value: float) -> str:
        """Format coordinate value"""
        decimals = self.config['output'].get('decimal_places', 3)
        return f"{value:.{decimals}f}"
    
    def _calculate_distance(self, p1: Point, p2: Point) -> float:
        """Calculate distance between two points"""
        import math
        return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2 + (p2.z - p1.z)**2)
    
    def save_gcode(self, gcode: str, filepath: str):
        """
        Save G-code to file
        
        Args:
            gcode: G-code string
            filepath: Output file path
        """
        with open(filepath, 'w') as f:
            f.write(gcode)
        logger.info(f"G-code saved to {filepath}")


class GCodeFormat:
    """G-code format definitions for different machines"""
    
    FANUC = {
        'name': 'Fanuc',
        'rapid': 'G00',
        'linear': 'G01',
        'arc_cw': 'G02',
        'arc_ccw': 'G03',
        'start_code': ['G21', 'G90', 'G40'],
        'end_code': ['M5', 'M30']
    }
    
    SIEMENS = {
        'name': 'Siemens Sinumerik',
        'rapid': 'G00',
        'linear': 'G01',
        'arc_cw': 'G02',
        'arc_ccw': 'G03',
        'start_code': ['G21', 'G90'],
        'end_code': ['M30']
    }
    
    HEIDENHAIN = {
        'name': 'Heidenhain iTNC 530',
        'rapid': 'G00',
        'linear': 'G01',
        'arc_cw': 'G02',
        'arc_ccw': 'G03',
        'start_code': ['BLK FORM 0.1 Z X 0 Y 0 Z 0'],
        'end_code': ['M30']
    }