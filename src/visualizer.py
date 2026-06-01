"""
Visualizer Module
Generates visualization of wire bending paths
"""

import logging
from typing import List, Optional, Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import numpy as np

from src.dxf_parser import LineSegment, CircleEntity, ArcEntity, PolylineEntity, Point
from src.geometry import Geometry

logger = logging.getLogger(__name__)


class PathVisualizer:
    """
    Visualizes wire bending paths
    """
    
    def __init__(self, figsize: Tuple[int, int] = (12, 10), dpi: int = 100):
        """
        Initialize visualizer
        
        Args:
            figsize: Figure size (width, height)
            dpi: Dots per inch
        """
        self.figsize = figsize
        self.dpi = dpi
        self.fig = None
        self.ax = None
    
    def plot_path(self, segments: List[LineSegment], title: str = "Wire Bending Path",
                  show_grid: bool = True, show_numbers: bool = True,
                  save_path: Optional[str] = None) -> None:
        """
        Plot wire bending path
        
        Args:
            segments: List of line segments
            title: Plot title
            show_grid: Show grid
            show_numbers: Show segment numbers
            save_path: Optional path to save figure
        """
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        if not segments:
            logger.warning("No segments to plot")
            return
        
        # Plot segments
        for i, segment in enumerate(segments):
            x = [segment.start.x, segment.end.x]
            y = [segment.start.y, segment.end.y]
            
            # Plot line
            self.ax.plot(x, y, 'b-', linewidth=2, alpha=0.7)
            
            # Plot start point
            self.ax.plot(segment.start.x, segment.start.y, 'go', markersize=6)
            
            # Plot end point
            self.ax.plot(segment.end.x, segment.end.y, 'ro', markersize=6)
            
            # Add arrow
            arrow = FancyArrowPatch(
                (segment.start.x, segment.start.y),
                (segment.end.x, segment.end.y),
                arrowstyle='->', mutation_scale=20, alpha=0.5, color='blue'
            )
            self.ax.add_patch(arrow)
            
            # Show segment number
            if show_numbers:
                mid_x = (segment.start.x + segment.end.x) / 2
                mid_y = (segment.start.y + segment.end.y) / 2
                self.ax.text(mid_x, mid_y, str(i + 1), fontsize=8,
                           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
        
        # Configure plot
        self.ax.set_aspect('equal')
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.set_xlabel('X (mm)', fontsize=12)
        self.ax.set_ylabel('Y (mm)', fontsize=12)
        
        if show_grid:
            self.ax.grid(True, alpha=0.3, linestyle='--')
        
        # Add legend
        self.ax.plot([], [], 'go', markersize=8, label='Start Point')
        self.ax.plot([], [], 'ro', markersize=8, label='End Point')
        self.ax.plot([], [], 'b-', linewidth=2, label='Wire Path')
        self.ax.legend(loc='upper right', fontsize=10)
        
        # Add statistics
        total_length = sum(Geometry.distance_2d(s.start, s.end) for s in segments)
        stats_text = f"Segments: {len(segments)}\nTotal Length: {total_length:.2f}mm"
        self.ax.text(0.02, 0.98, stats_text, transform=self.ax.transAxes,
                    fontsize=10, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Visualization saved to {save_path}")
        
        plt.show()
    
    def plot_entities(self, entities: List, title: str = "DXF Entities",
                     show_grid: bool = True, save_path: Optional[str] = None) -> None:
        """
        Plot original DXF entities
        
        Args:
            entities: List of entities
            title: Plot title
            show_grid: Show grid
            save_path: Optional path to save figure
        """
        self.fig, self.ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        colors = {'line': 'blue', 'circle': 'red', 'arc': 'green', 'polyline': 'purple'}
        
        for entity in entities:
            if isinstance(entity, LineSegment):
                x = [entity.start.x, entity.end.x]
                y = [entity.start.y, entity.end.y]
                self.ax.plot(x, y, color=colors['line'], linewidth=2, alpha=0.7, label='Line')
            
            elif isinstance(entity, CircleEntity):
                circle = patches.Circle(
                    (entity.center.x, entity.center.y),
                    entity.radius,
                    fill=False, edgecolor=colors['circle'], linewidth=2, alpha=0.7
                )
                self.ax.add_patch(circle)
                self.ax.plot(entity.center.x, entity.center.y, 'r+', markersize=10)
            
            elif isinstance(entity, ArcEntity):
                angles = np.linspace(entity.start_angle, entity.end_angle, 100)
                points = [Geometry.point_on_circle(entity.center, entity.radius, a) for a in angles]
                x = [p.x for p in points]
                y = [p.y for p in points]
                self.ax.plot(x, y, color=colors['arc'], linewidth=2, alpha=0.7, label='Arc')
            
            elif isinstance(entity, PolylineEntity):
                x = [p.x for p in entity.points]
                y = [p.y for p in entity.points]
                if entity.is_closed:
                    x.append(entity.points[0].x)
                    y.append(entity.points[0].y)
                self.ax.plot(x, y, color=colors['polyline'], linewidth=2, alpha=0.7, label='Polyline')
        
        # Configure plot
        self.ax.set_aspect('equal')
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.set_xlabel('X (mm)', fontsize=12)
        self.ax.set_ylabel('Y (mm)', fontsize=12)
        
        if show_grid:
            self.ax.grid(True, alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Visualization saved to {save_path}")
        
        plt.show()
    
    def plot_comparison(self, entities: List, segments: List[LineSegment],
                       save_path: Optional[str] = None) -> None:
        """
        Plot comparison between original entities and optimized path
        
        Args:
            entities: Original entities
            segments: Optimized segments
            save_path: Optional path to save figure
        """
        self.fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=self.dpi)
        
        # Plot original entities
        self._plot_on_axis(ax1, entities, "Original DXF Entities")
        
        # Plot optimized segments
        self._plot_segments_on_axis(ax2, segments, "Optimized Path")
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.dpi, bbox_inches='tight')
            logger.info(f"Comparison visualization saved to {save_path}")
        
        plt.show()
    
    def _plot_on_axis(self, ax, entities: List, title: str) -> None:
        """Plot entities on given axis"""
        colors = {'line': 'blue', 'circle': 'red', 'arc': 'green'}
        
        for entity in entities:
            if isinstance(entity, LineSegment):
                ax.plot([entity.start.x, entity.end.x],
                       [entity.start.y, entity.end.y],
                       color=colors['line'], linewidth=1.5, alpha=0.7)
        
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlabel('X (mm)')
        ax.set_ylabel('Y (mm)')
        ax.grid(True, alpha=0.3)
    
    def _plot_segments_on_axis(self, ax, segments: List[LineSegment], title: str) -> None:
        """Plot segments on given axis"""
        for i, segment in enumerate(segments):
            ax.plot([segment.start.x, segment.end.x],
                   [segment.start.y, segment.end.y],
                   'b-', linewidth=1.5, alpha=0.7)
            ax.plot(segment.start.x, segment.start.y, 'go', markersize=4)
            ax.plot(segment.end.x, segment.end.y, 'ro', markersize=4)
        
        ax.set_aspect('equal')
        ax.set_title(title, fontsize=12, fontweight='bold')
        ax.set_xlabel('X (mm)')
        ax.set_ylabel('Y (mm)')
        ax.grid(True, alpha=0.3)
