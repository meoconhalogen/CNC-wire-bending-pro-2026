"""
DXF Parser Module
Reads and parses DXF files to extract geometric entities
"""

import ezdxf
from typing import List, Dict, Tuple, Any
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class EntityType(Enum):
    """Supported DXF entity types"""
    LINE = "LINE"
    CIRCLE = "CIRCLE"
    ARC = "ARC"
    POLYLINE = "LWPOLYLINE"
    SPLINE = "SPLINE"
    POINT = "POINT"


@dataclass
class Point:
    """2D Point representation"""
    x: float
    y: float
    z: float = 0.0
    
    def __repr__(self):
        return f"Point({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


@dataclass
class LineSegment:
    """Line segment entity"""
    start: Point
    end: Point
    entity_type: EntityType = EntityType.LINE
    
    def __repr__(self):
        return f"Line({self.start} -> {self.end})"


@dataclass
class CircleEntity:
    """Circle entity"""
    center: Point
    radius: float
    entity_type: EntityType = EntityType.CIRCLE
    
    def __repr__(self):
        return f"Circle(center={self.center}, r={self.radius:.3f})"


@dataclass
class ArcEntity:
    """Arc entity"""
    center: Point
    radius: float
    start_angle: float  # degrees
    end_angle: float    # degrees
    entity_type: EntityType = EntityType.ARC
    
    def __repr__(self):
        return f"Arc(center={self.center}, r={self.radius:.3f}, {self.start_angle:.1f}° -> {self.end_angle:.1f}°)"


@dataclass
class PolylineEntity:
    """Polyline entity"""
    points: List[Point]
    is_closed: bool = False
    entity_type: EntityType = EntityType.POLYLINE
    
    def __repr__(self):
        return f"Polyline({len(self.points)} points, closed={self.is_closed})"


class DXFParser:
    """
    DXF File Parser
    Extracts geometric entities from DXF files
    """
    
    def __init__(self, filepath: str):
        """
        Initialize DXF parser
        
        Args:
            filepath: Path to DXF file
        """
        self.filepath = filepath
        self.doc = None
        self.entities = []
        self.bounds = None
        
    def parse(self) -> List[Any]:
        """
        Parse DXF file and extract entities
        
        Returns:
            List of parsed entities
        """
        try:
            self.doc = ezdxf.readfile(self.filepath)
            logger.info(f"Loaded DXF file: {self.filepath}")
            
            msp = self.doc.modelspace()
            
            for dxf_entity in msp:
                parsed = self._parse_entity(dxf_entity)
                if parsed:
                    self.entities.append(parsed)
            
            logger.info(f"Parsed {len(self.entities)} entities")
            self._calculate_bounds()
            
            return self.entities
            
        except Exception as e:
            logger.error(f"Error parsing DXF file: {str(e)}")
            raise
    
    def _parse_entity(self, dxf_entity) -> Any:
        """
        Parse individual DXF entity
        
        Args:
            dxf_entity: DXF entity object
            
        Returns:
            Parsed entity or None
        """
        entity_type = dxf_entity.dxftype()
        
        try:
            if entity_type == "LINE":
                return self._parse_line(dxf_entity)
            elif entity_type == "CIRCLE":
                return self._parse_circle(dxf_entity)
            elif entity_type == "ARC":
                return self._parse_arc(dxf_entity)
            elif entity_type == "LWPOLYLINE":
                return self._parse_polyline(dxf_entity)
            elif entity_type == "SPLINE":
                return self._parse_spline(dxf_entity)
            elif entity_type == "POINT":
                return self._parse_point(dxf_entity)
            else:
                logger.warning(f"Unsupported entity type: {entity_type}")
                return None
                
        except Exception as e:
            logger.warning(f"Error parsing entity {entity_type}: {str(e)}")
            return None
    
    def _parse_line(self, entity) -> LineSegment:
        """Parse LINE entity"""
        start = Point(entity.dxf.start.x, entity.dxf.start.y, entity.dxf.start.z)
        end = Point(entity.dxf.end.x, entity.dxf.end.y, entity.dxf.end.z)
        return LineSegment(start, end)
    
    def _parse_circle(self, entity) -> CircleEntity:
        """Parse CIRCLE entity"""
        center = Point(entity.dxf.center.x, entity.dxf.center.y, entity.dxf.center.z)
        radius = entity.dxf.radius
        return CircleEntity(center, radius)
    
    def _parse_arc(self, entity) -> ArcEntity:
        """Parse ARC entity"""
        center = Point(entity.dxf.center.x, entity.dxf.center.y, entity.dxf.center.z)
        radius = entity.dxf.radius
        start_angle = entity.dxf.start_angle
        end_angle = entity.dxf.end_angle
        return ArcEntity(center, radius, start_angle, end_angle)
    
    def _parse_polyline(self, entity) -> PolylineEntity:
        """Parse LWPOLYLINE entity"""
        points = []
        for point in entity.get_points():
            points.append(Point(point[0], point[1], point[2] if len(point) > 2 else 0))
        
        is_closed = entity.dxf.flags & 1 == 1
        return PolylineEntity(points, is_closed)
    
    def _parse_spline(self, entity) -> PolylineEntity:
        """Parse SPLINE entity by approximating with line segments"""
        # Approximate spline with control points
        points = []
        for control_point in entity.control_points:
            points.append(Point(control_point[0], control_point[1], 
                              control_point[2] if len(control_point) > 2 else 0))
        return PolylineEntity(points, False)
    
    def _parse_point(self, entity) -> Point:
        """Parse POINT entity"""
        return Point(entity.dxf.location.x, entity.dxf.location.y, entity.dxf.location.z)
    
    def _calculate_bounds(self) -> None:
        """Calculate bounding box of all entities"""
        if not self.entities:
            self.bounds = None
            return
        
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        
        for entity in self.entities:
            if isinstance(entity, LineSegment):
                min_x = min(min_x, entity.start.x, entity.end.x)
                max_x = max(max_x, entity.start.x, entity.end.x)
                min_y = min(min_y, entity.start.y, entity.end.y)
                max_y = max(max_y, entity.start.y, entity.end.y)
            elif isinstance(entity, CircleEntity):
                min_x = min(min_x, entity.center.x - entity.radius)
                max_x = max(max_x, entity.center.x + entity.radius)
                min_y = min(min_y, entity.center.y - entity.radius)
                max_y = max(max_y, entity.center.y + entity.radius)
            elif isinstance(entity, PolylineEntity):
                for point in entity.points:
                    min_x = min(min_x, point.x)
                    max_x = max(max_x, point.x)
                    min_y = min(min_y, point.y)
                    max_y = max(max_y, point.y)
            elif isinstance(entity, Point):
                min_x = min(min_x, entity.x)
                max_x = max(max_x, entity.x)
                min_y = min(min_y, entity.y)
                max_y = max(max_y, entity.y)
        
        self.bounds = {
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y,
            'width': max_x - min_x,
            'height': max_y - min_y
        }
        
        logger.info(f"Bounds: {self.bounds}")
    
    def get_bounds(self) -> Dict[str, float]:
        """Get bounding box of parsed entities"""
        return self.bounds
    
    def get_entity_count(self) -> int:
        """Get total number of entities"""
        return len(self.entities)


# Configure logging
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)