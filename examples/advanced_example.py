#!/usr/bin/env python
"""
Advanced Example: Custom configuration and arc support
"""

import sys
sys.path.insert(0, '..')

import yaml
from src import DXFParser, PathOptimizer, GCodeGenerator
from src.gcode_arc_support import ArcGCodeGenerator
from src.visualizer import PathVisualizer
import logging

logging.basicConfig(level=logging.INFO)

def create_custom_config():
    """Create a custom machine configuration"""
    config = {
        'machine': {
            'name': 'Advanced CNC Wire Bender',
            'max_speed': 200,
            'acceleration': 100,
            'min_radius': 1.5,
            'max_wire_length': 10000
        },
        'wire': {
            'diameter': 1.5,
            'material': 'stainless_steel'
        },
        'processing': {
            'tolerance': 0.05,
            'feed_rate': 100,
            'cutting_speed': 300
        },
        'optimization': {
            'enable_path_optimization': True,
            'merge_segments': True,
            'min_segment_length': 0.3
        },
        'output': {
            'format': 'siemens',
            'decimal_places': 4,
            'include_comments': True
        }
    }
    
    with open('advanced_config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    return config

def main():
    print("="*70)
    print("CNC Wire Bending Pro 2026 - Advanced Example")
    print("="*70)
    
    try:
        # Create custom config
        print("\n[1] Creating custom configuration...")
        config = create_custom_config()
        print(f"✓ Configuration saved")
        print(f"  Machine: {config['machine']['name']}")
        print(f"  Format: {config['output']['format']}")
        print(f"  Tolerance: {config['processing']['tolerance']}mm")
        
        # Parse DXF
        print("\n[2] Parsing DXF file...")
        dxf_file = 'sample.dxf'
        parser = DXFParser(dxf_file)
        entities = parser.parse()
        print(f"✓ Found {len(entities)} entities")
        
        # Optimize
        print("\n[3] Optimizing path...")
        optimizer = PathOptimizer(tolerance=config['processing']['tolerance'])
        segments = optimizer.optimize(entities)
        stats = optimizer.get_statistics()
        print(f"✓ Optimized: {stats['num_segments']} segments, {stats['total_length']:.2f}mm")
        
        # Visualize original and optimized
        print("\n[4] Creating comparison visualization...")
        visualizer = PathVisualizer(figsize=(16, 8))
        visualizer.plot_comparison(
            entities, segments,
            save_path='comparison.png'
        )
        print("✓ Comparison saved to comparison.png")
        
        # Generate G-code
        print("\n[5] Generating G-code...")
        generator = GCodeGenerator()
        generator.config = config  # Apply custom config
        gcode = generator.generate(segments)
        
        # Save
        output_file = 'advanced_output.gcode'
        generator.save_gcode(gcode, output_file)
        print(f"✓ G-code saved to {output_file}")
        
        # Print statistics
        print("\n" + "="*70)
        print("CONVERSION STATISTICS")
        print("="*70)
        print(f"Input entities:        {len(entities)}")
        print(f"Output segments:       {stats['num_segments']}")
        print(f"Total wire length:     {stats['total_length']:.2f}mm")
        print(f"Average segment:       {stats['avg_segment_length']:.2f}mm")
        print(f"Output format:         {config['output']['format']}")
        print(f"Wire diameter:         {config['wire']['diameter']}mm")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
