"""
Main Entry Point
CNC Wire Bending Pro 2026
"""

import logging
import sys
import argparse
from pathlib import Path

from src.dxf_parser import DXFParser
from src.path_optimizer import PathOptimizer
from src.gcode_generator import GCodeGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='CNC Wire Bending Pro 2026 - DXF to G-code Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main input.dxf -o output.gcode
  python -m src.main input.dxf -o output.gcode -c config.yaml
  python -m src.main input.dxf -o output.gcode --format siemens
        """
    )
    
    parser.add_argument('input', help='Input DXF file')
    parser.add_argument('-o', '--output', default='output.gcode', help='Output G-code file')
    parser.add_argument('-c', '--config', default='config.yaml', help='Configuration file')
    parser.add_argument('-f', '--format', default='fanuc', 
                       choices=['fanuc', 'siemens', 'heidenhain'],
                       help='G-code format')
    parser.add_argument('-t', '--tolerance', type=float, default=0.1,
                       help='Path simplification tolerance (mm)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        logger.info("=" * 60)
        logger.info("CNC Wire Bending Pro 2026")
        logger.info("=" * 60)
        logger.info(f"Input file: {args.input}")
        logger.info(f"Output file: {args.output}")
        logger.info(f"Format: {args.format}")
        logger.info(f"Tolerance: {args.tolerance}mm")
        logger.info("=" * 60)
        
        # Check input file exists
        if not Path(args.input).exists():
            logger.error(f"Input file not found: {args.input}")
            return 1
        
        # Parse DXF
        logger.info("Step 1: Parsing DXF file...")
        dxf_parser = DXFParser(args.input)
        entities = dxf_parser.parse()
        
        if not entities:
            logger.warning("No entities found in DXF file")
            return 1
        
        logger.info(f"Found {len(entities)} entities")
        bounds = dxf_parser.get_bounds()
        if bounds:
            logger.info(f"Bounds: X[{bounds['min_x']:.2f}, {bounds['max_x']:.2f}] "
                       f"Y[{bounds['min_y']:.2f}, {bounds['max_y']:.2f}]")
        
        # Optimize path
        logger.info("Step 2: Optimizing path...")
        optimizer = PathOptimizer(tolerance=args.tolerance)
        segments = optimizer.optimize(entities)
        
        stats = optimizer.get_statistics()
        logger.info(f"Optimized path: {stats.get('num_segments', 0)} segments")
        logger.info(f"Total wire length: {stats.get('total_length', 0):.2f}mm")
        
        # Generate G-code
        logger.info("Step 3: Generating G-code...")
        gcode_gen = GCodeGenerator(config_file=args.config)
        gcode = gcode_gen.generate(segments)
        
        # Save G-code
        logger.info("Step 4: Saving G-code...")
        gcode_gen.save_gcode(gcode, args.output)
        
        logger.info("=" * 60)
        logger.info("✓ Conversion completed successfully!")
        logger.info(f"G-code saved to: {args.output}")
        logger.info("=" * 60)
        
        return 0
        
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=args.verbose)
        return 1


if __name__ == '__main__':
    sys.exit(main())