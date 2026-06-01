"""
Geometry Module
Basic geometric operations and calculations
"""

import math
from typing import Tuple, List
from src.dxf_parser import Point


class Geometry:
    """Geometric operations and utilities"""
    
    @staticmethod
    def distance(p1: Point, p2: Point) -> float:
        """
        Calculate Euclidean distance between two points
        
        Args:
            p1, p2: Points
            
        Returns:
            Distance
        """
        return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2 + (p2.z - p1.z)**2)
    
    @staticmethod
    def distance_2d(p1: Point, p2: Point) -> float:
        """Calculate 2D distance (ignoring Z)"""
        return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
    
    @staticmethod
    def angle(p1: Point, p2: Point) -> float:
        """
        Calculate angle from p1 to p2 in degrees (0-360)
        
        Args:
            p1, p2: Points
            
        Returns:
            Angle in degrees
        """
        angle_rad = math.atan2(p2.y - p1.y, p2.x - p1.x)
        angle_deg = math.degrees(angle_rad)
        return angle_deg % 360
    
    @staticmethod
    def angle_between(p1: Point, p2: Point, p3: Point) -> float:
        """
        Calculate angle at p2 between p1-p2-p3
        
        Args:
            p1, p2, p3: Points
            
        Returns:
            Angle in degrees (0-180)
        """
        v1_x = p1.x - p2.x
        v1_y = p1.y - p2.y
        v2_x = p3.x - p2.x
        v2_y = p3.y - p2.y
        
        dot = v1_x * v2_x + v1_y * v2_y
        cross = v1_x * v2_y - v1_y * v2_x
        
        angle_rad = math.atan2(cross, dot)
        return abs(math.degrees(angle_rad))
    
    @staticmethod
    def arc_length(radius: float, start_angle: float, end_angle: float) -> float:
        """
        Calculate arc length
        
        Args:
            radius: Arc radius
            start_angle: Start angle in degrees
            end_angle: End angle in degrees
            
        Returns:
            Arc length
        """
        angle_diff = abs(end_angle - start_angle)
        angle_rad = math.radians(angle_diff)
        return radius * angle_rad
    
    @staticmethod
    def point_on_circle(center: Point, radius: float, angle: float) -> Point:
        """
        Calculate point on circle at given angle
        
        Args:
            center: Circle center
            radius: Circle radius
            angle: Angle in degrees
            
        Returns:
            Point on circle
        """
        angle_rad = math.radians(angle)
        x = center.x + radius * math.cos(angle_rad)
        y = center.y + radius * math.sin(angle_rad)
        return Point(x, y, center.z)
    
    @staticmethod
    def point_on_line(p1: Point, p2: Point, t: float) -> Point:
        """
        Calculate interpolated point on line
        
        Args:
            p1, p2: Line endpoints
            t: Parameter (0-1)
            
        Returns:
            Interpolated point
        """
        x = p1.x + (p2.x - p1.x) * t
        y = p1.y + (p2.y - p1.y) * t
        z = p1.z + (p2.z - p1.z) * t
        return Point(x, y, z)
    
    @staticmethod
    def line_intersection(p1: Point, p2: Point, p3: Point, p4: Point) -> Tuple[bool, Point]:
        """
        Calculate intersection of two lines
        
        Args:
            p1, p2: First line endpoints
            p3, p4: Second line endpoints
            
        Returns:
            Tuple (found, intersection_point)
        """
        x1, y1 = p1.x, p1.y
        x2, y2 = p2.x, p2.y
        x3, y3 = p3.x, p3.y
        x4, y4 = p4.x, p4.y
        
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        
        if abs(denom) < 1e-10:
            return False, None  # Lines are parallel
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denom
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denom
        
        if 0 <= t <= 1 and 0 <= u <= 1:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            return True, Point(x, y, 0)
        
        return False, None
    
    @staticmethod
    def point_to_line_distance(point: Point, p1: Point, p2: Point) -> float:
        """
        Calculate perpendicular distance from point to line
        
        Args:
            point: Point
            p1, p2: Line endpoints
            
        Returns:
            Perpendicular distance
        """
        num = abs((p2.y - p1.y) * point.x - (p2.x - p1.x) * point.y + p2.x * p1.y - p2.y * p1.x)
        denom = math.sqrt((p2.y - p1.y)**2 + (p2.x - p1.x)**2)
        
        if denom < 1e-10:
            return Geometry.distance_2d(point, p1)
        
        return num / denom
    
    @staticmethod
    def simplify_path(points: List[Point], tolerance: float) -> List[Point]:
        """
        Simplify path using Douglas-Peucker algorithm
        
        Args:
            points: List of points
            tolerance: Simplification tolerance
            
        Returns:
            Simplified point list
        """
        if len(points) < 3:
            return points
        
        def rdp(pts, tol):
            if len(pts) < 3:
                return pts
            
            # Find point with max distance
            max_dist = 0
            max_idx = 0
            for i in range(1, len(pts) - 1):
                dist = Geometry.point_to_line_distance(pts[i], pts[0], pts[-1])
                if dist > max_dist:
                    max_dist = dist
                    max_idx = i
            
            if max_dist > tol:
                left = rdp(pts[:max_idx + 1], tol)
                right = rdp(pts[max_idx:], tol)
                return left[:-1] + right
            else:
                return [pts[0], pts[-1]]
        
        return rdp(points, tolerance)
    
    @staticmethod
    def offset_point(point: Point, direction: float, distance: float) -> Point:
        """
        Move point in given direction and distance
        
        Args:
            point: Starting point
            direction: Direction in degrees
            distance: Distance to move
            
        Returns:
            New point
        """
        angle_rad = math.radians(direction)
        x = point.x + distance * math.cos(angle_rad)
        y = point.y + distance * math.sin(angle_rad)
        return Point(x, y, point.z)
    
    @staticmethod
    def rotate_point(point: Point, center: Point, angle: float) -> Point:
        """
        Rotate point around center
        
        Args:
            point: Point to rotate
            center: Rotation center
            angle: Rotation angle in degrees
            
        Returns:
            Rotated point
        """
        angle_rad = math.radians(angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        dx = point.x - center.x
        dy = point.y - center.y
        
        x = center.x + dx * cos_a - dy * sin_a
        y = center.y + dx * sin_a + dy * cos_a
        
        return Point(x, y, point.z)