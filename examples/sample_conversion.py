#!/usr/bin/env python
"""
Example: Convert sample DXF to G-code
"""

import sys
sys.path.insert(0, '..')

from src import DXFParser, PathOptimizer, GCodeGenerator
from src.visualizer import PathVisualizer
import logging

# Enable logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    print("="*60)
    print("CNC Wire Bending Pro 2026 - Conversion Example")
    print("="*60)
    
    # Note: You need to create a sample.dxf file first
    dxf_file = 'sample.dxf'
    output_file = 'sample_output.gcode'
    
    try:
        # Step 1: Parse DXF
        print("\n[Step 1] Parsing DXF file...")
        parser = DXFParser(dxf_file)
        entities = parser.parse()
        
        if not entities:
            print("✗ No entities found in DXF file")
            return 1
        
        print(f"✓ Found {len(entities)} entities")
        bounds = parser.get_bounds()
        if bounds:
            print(f"  - Bounds: {bounds['width']:.2f}mm x {bounds['height']:.2f}mm")
        
        # Step 2: Optimize path
        print("\n[Step 2] Optimizing path...")
        optimizer = PathOptimizer(tolerance=0.1)
        segments = optimizer.optimize(entities)
        stats = optimizer.get_statistics()
        
        print(f"✓ Optimized to {stats['num_segments']} segments")
        print(f"  - Total wire length: {stats['total_length']:.2f}mm")
        print(f"  - Average segment: {stats['avg_segment_length']:.2f}mm")
        
        # Step 3: Visualize (optional)
        print("\n[Step 3] Creating visualization...")
        visualizer = PathVisualizer()
        visualizer.plot_path(
            segments,
            title="Optimized Wire Bending Path",
            save_path='path_visualization.png'
        )
        
        # Step 4: Generate G-code
        print("\n[Step 4] Generating G-code...")
        generator = GCodeGenerator(config_file='../config.yaml')
        gcode = generator.generate(segments)
        
        # Step 5: Save G-code
        print("\n[Step 5] Saving G-code...")
        generator.save_gcode(gcode, output_file)
        print(f"✓ G-code saved to {output_file}")
        
        # Print first few lines
        lines = gcode.split('\n')[:10]
        print("\nFirst 10 lines of G-code:")
        for line in lines:
            print(f"  {line}")
        
        print("\n" + "="*60)
        print("✓ Conversion completed successfully!")
        print("="*60)
        
        return 0
        
    except FileNotFoundError:
        print(f"✗ Error: File '{dxf_file}' not found")
        print("Please create a sample DXF file first")
        return 1
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
