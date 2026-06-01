"""
Advanced G-code Generator with Arc Support
Supports G02/G03 for circular moves
"""

import logging
from typing import List
import math

from src.dxf_parser import Point, ArcEntity
from src.geometry import Geometry

logger = logging.getLogger(__name__)


class ArcGCodeGenerator:
    """
    Advanced G-code generator supporting arcs
    """
    
    @staticmethod
    def generate_arc_gcode(arc: ArcEntity, feed_rate: float = 50,
                          clockwise: bool = True) -> str:
        """
        Generate G-code for arc movement
        
        Args:
            arc: Arc entity
            feed_rate: Feed rate in mm/min
            clockwise: Clockwise (G02) or counterclockwise (G03)
            
        Returns:
            G-code string for arc
        """
        gcode = []
        
        # Determine arc direction
        arc_cmd = "G02" if clockwise else "G03"
        
        # Get start and end points
        start_point = Geometry.point_on_circle(arc.center, arc.radius, arc.start_angle)
        end_point = Geometry.point_on_circle(arc.center, arc.radius, arc.end_angle)
        
        # Calculate offset from start point to center
        i_offset = arc.center.x - start_point.x
        j_offset = arc.center.y - start_point.y
        
        # Generate G-code
        gcode.append(f"G01 X{start_point.x:.3f} Y{start_point.y:.3f}")
        gcode.append(
            f"{arc_cmd} X{end_point.x:.3f} Y{end_point.y:.3f} "
            f"I{i_offset:.3f} J{j_offset:.3f} F{feed_rate}"
        )
        
        return "\n".join(gcode)
    
    @staticmethod
    def approximate_arc_with_segments(arc: ArcEntity, 
                                     max_angle: float = 10) -> List[Point]:
        """
        Approximate arc with line segments
        
        Args:
            arc: Arc entity
            max_angle: Maximum angle per segment (degrees)
            
        Returns:
            List of points approximating the arc
        """
        points = []
        angle_diff = arc.end_angle - arc.start_angle
        num_segments = max(1, math.ceil(abs(angle_diff) / max_angle))
        
        for i in range(num_segments + 1):
            t = i / num_segments if num_segments > 0 else 0
            angle = arc.start_angle + angle_diff * t
            point = Geometry.point_on_circle(arc.center, arc.radius, angle)
            points.append(point)
        
        return points
    
    @staticmethod
    def arc_to_gcode(arc: ArcEntity, decimal_places: int = 3) -> str:
        """
        Convert arc to G02/G03 G-code
        
        Args:
            arc: Arc entity
            decimal_places: Number of decimal places
            
        Returns:
            G-code string
        """
        fmt = f".{decimal_places}f"
        
        # Determine direction
        angle_diff = arc.end_angle - arc.start_angle
        is_clockwise = angle_diff < 0
        arc_cmd = "G02" if is_clockwise else "G03"
        
        # Get points
        start_point = Geometry.point_on_circle(arc.center, arc.radius, arc.start_angle)
        end_point = Geometry.point_on_circle(arc.center, arc.radius, arc.end_angle)
        
        # Calculate offsets
        i_offset = arc.center.x - start_point.x
        j_offset = arc.center.y - start_point.y
        
        # Generate G-code
        x_end = format(end_point.x, fmt)
        y_end = format(end_point.y, fmt)
        i_val = format(i_offset, fmt)
        j_val = format(j_offset, fmt)
        
        return f"{arc_cmd} X{x_end} Y{y_end} I{i_val} J{j_val}"
