"""
Path Optimizer Module
Optimizes the bending path to reduce execution time and wire waste
"""

import logging
from typing import List, Any, Tuple
from src.geometry import Geometry
from src.dxf_parser import Point, LineSegment, ArcEntity

logger = logging.getLogger(__name__)


class PathOptimizer:
    """
    Optimizes wire bending paths
    - Minimizes total path length
    - Reorders entities for efficiency
    - Merges nearby segments
    """
    
    def __init__(self, tolerance: float = 0.1):
        """
        Initialize path optimizer
        
        Args:
            tolerance: Tolerance for segment merging (mm)
        """
        self.tolerance = tolerance
        self.optimized_entities = []
    
    def optimize(self, entities: List[Any]) -> List[Any]:
        """
        Optimize entity order and path
        
        Args:
            entities: List of entities from DXF parser
            
        Returns:
            Optimized entity list
        """
        if not entities:
            return []
        
        logger.info(f"Optimizing {len(entities)} entities")
        
        # Convert all entities to line segments for unified handling
        segments = self._convert_to_segments(entities)
        logger.info(f"Converted to {len(segments)} segments")
        
        # Merge close segments
        segments = self._merge_close_segments(segments)
        logger.info(f"After merging: {len(segments)} segments")
        
        # Order segments to minimize travel distance
        segments = self._order_segments(segments)
        logger.info(f"Segments reordered")
        
        self.optimized_entities = segments
        return segments
    
    def _convert_to_segments(self, entities: List[Any]) -> List[LineSegment]:
        """
        Convert various entity types to line segments
        
        Args:
            entities: Mixed entity list
            
        Returns:
            List of line segments
        """
        segments = []
        
        for entity in entities:
            if isinstance(entity, LineSegment):
                segments.append(entity)
            elif isinstance(entity, ArcEntity):
                # Approximate arc with line segments
                arc_segments = self._arc_to_segments(entity)
                segments.extend(arc_segments)
            elif hasattr(entity, 'points'):  # Polyline
                for i in range(len(entity.points) - 1):
                    seg = LineSegment(entity.points[i], entity.points[i + 1])
                    segments.append(seg)
                if entity.is_closed and len(entity.points) > 1:
                    seg = LineSegment(entity.points[-1], entity.points[0])
                    segments.append(seg)
        
        return segments
    
    def _arc_to_segments(self, arc: ArcEntity, num_segments: int = 10) -> List[LineSegment]:
        """
        Approximate arc with line segments
        
        Args:
            arc: Arc entity
            num_segments: Number of segments to use
            
        Returns:
            List of line segments approximating the arc
        """
        segments = []
        angle_diff = arc.end_angle - arc.start_angle
        
        for i in range(num_segments):
            t = i / num_segments
            angle1 = arc.start_angle + angle_diff * t
            angle2 = arc.start_angle + angle_diff * (t + 1 / num_segments)
            
            p1 = Geometry.point_on_circle(arc.center, arc.radius, angle1)
            p2 = Geometry.point_on_circle(arc.center, arc.radius, angle2)
            
            segments.append(LineSegment(p1, p2))
        
        return segments
    
    def _merge_close_segments(self, segments: List[LineSegment]) -> List[LineSegment]:
        """
        Merge segments that are close to collinear
        
        Args:
            segments: List of segments
            
        Returns:
            Merged segment list
        """
        if len(segments) < 2:
            return segments
        
        merged = []
        i = 0
        
        while i < len(segments):
            current = segments[i]
            
            # Look for consecutive segments that can be merged
            j = i + 1
            while j < len(segments):
                next_seg = segments[j]
                
                # Check if segments are connected and collinear
                dist = Geometry.distance_2d(current.end, next_seg.start)
                
                if dist < self.tolerance:
                    # Check collinearity
                    dist_to_line = Geometry.point_to_line_distance(
                        next_seg.start, current.start, current.end
                    )
                    
                    if dist_to_line < self.tolerance:
                        # Merge segments
                        current = LineSegment(current.start, next_seg.end)
                        j += 1
                    else:
                        break
                else:
                    break
            
            merged.append(current)
            i = j if j > i + 1 else i + 1
        
        return merged
    
    def _order_segments(self, segments: List[LineSegment]) -> List[LineSegment]:
        """
        Reorder segments to minimize total travel distance (TSP approximation)
        
        Args:
            segments: List of segments
            
        Returns:
            Reordered segment list
        """
        if len(segments) < 2:
            return segments
        
        # Greedy nearest neighbor algorithm
        ordered = []
        remaining = segments.copy()
        
        # Start with first segment
        current = remaining.pop(0)
        ordered.append(current)
        
        while remaining:
            # Find nearest segment
            min_dist = float('inf')
            best_idx = 0
            best_reversed = False
            
            for idx, seg in enumerate(remaining):
                # Distance from current end to segment start
                dist_normal = Geometry.distance_2d(current.end, seg.start)
                
                # Distance from current end to segment end (reversed)
                dist_reversed = Geometry.distance_2d(current.end, seg.end)
                
                if dist_normal < min_dist:
                    min_dist = dist_normal
                    best_idx = idx
                    best_reversed = False
                
                if dist_reversed < min_dist:
                    min_dist = dist_reversed
                    best_idx = idx
                    best_reversed = True
            
            # Take best segment
            seg = remaining.pop(best_idx)
            
            # Reverse if needed
            if best_reversed:
                seg = LineSegment(seg.end, seg.start)
            
            ordered.append(seg)
            current = seg
        
        return ordered
    
    def calculate_total_length(self, segments: List[LineSegment]) -> float:
        """
        Calculate total path length
        
        Args:
            segments: List of segments
            
        Returns:
            Total length in mm
        """
        total = 0
        for seg in segments:
            total += Geometry.distance_2d(seg.start, seg.end)
        return total
    
    def get_statistics(self) -> dict:
        """Get optimization statistics"""
        if not self.optimized_entities:
            return {}
        
        total_length = self.calculate_total_length(self.optimized_entities)
        
        return {
            'num_segments': len(self.optimized_entities),
            'total_length': total_length,
            'avg_segment_length': total_length / len(self.optimized_entities) if self.optimized_entities else 0
        }