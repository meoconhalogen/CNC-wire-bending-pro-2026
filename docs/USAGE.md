# CNC Wire Bending Pro 2026 - Hướng dẫn sử dụng

## Mục lục
1. [Cài đặt](#cài-đặt)
2. [Sử dụng nhanh](#sử-dụng-nhanh)
3. [Ví dụ chi tiết](#ví-dụ-chi-tiết)
4. [Cấu hình](#cấu-hình)
5. [Xử lý sự cố](#xử-lý-sự-cố)

## Cài đặt

### Yêu cầu
- Python 3.8 trở lên
- pip package manager

### Bước 1: Clone repository
```bash
git clone https://github.com/meoconhalogen/CNC-wire-bending-pro-2026.git
cd CNC-wire-bending-pro-2026
```

### Bước 2: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Kiểm tra cài đặt
```bash
python -m pytest tests/ -v
```

## Sử dụng nhanh

### Cách 1: Command line

**Sử dụng mặc định:**
```bash
python -m src.main input.dxf -o output.gcode
```

**Với tùy chọn:**
```bash
python -m src.main input.dxf \
  -o output.gcode \
  -f siemens \
  -t 0.05 \
  -c my_config.yaml \
  -v
```

### Cách 2: Python API

```python
from src.dxf_parser import DXFParser
from src.path_optimizer import PathOptimizer
from src.gcode_generator import GCodeGenerator

# Bước 1: Đọc DXF
parser = DXFParser('input.dxf')
entities = parser.parse()
print(f"Tìm thấy {len(entities)} entities")

# Bước 2: Tối ưu hóa
optimizer = PathOptimizer(tolerance=0.1)
segments = optimizer.optimize(entities)
stats = optimizer.get_statistics()
print(f"Tổng độ dài dây: {stats['total_length']:.2f}mm")

# Bước 3: Sinh G-code
generator = GCodeGenerator(config_file='config.yaml')
gcode = generator.generate(segments)

# Bước 4: Lưu
generator.save_gcode(gcode, 'output.gcode')
```

## Ví dụ chi tiết

### Ví dụ 1: Chuyển đổi đơn giản

```python
from src import DXFParser, PathOptimizer, GCodeGenerator

# Đọc file DXF
parser = DXFParser('drawing.dxf')
entities = parser.parse()

# Lấy thông tin bounds
bounds = parser.get_bounds()
print(f"Kích thước: {bounds['width']}mm x {bounds['height']}mm")

# Tối ưu hóa
optimizer = PathOptimizer(tolerance=0.1)
segments = optimizer.optimize(entities)

# Sinh G-code
generator = GCodeGenerator()
gcode = generator.generate(segments)
generator.save_gcode(gcode, 'output.gcode')
```

### Ví dụ 2: Tùy chỉnh cấu hình

```python
import yaml
from src import DXFParser, GCodeGenerator

# Tạo cấu hình tùy chỉnh
config = {
    'machine': {
        'name': 'My CNC Machine',
        'feed_rate': 60,
        'max_speed': 150
    },
    'wire': {
        'diameter': 2.5,
        'material': 'aluminum'
    },
    'output': {
        'format': 'siemens',
        'decimal_places': 4,
        'include_comments': True
    }
}

# Lưu config
with open('custom_config.yaml', 'w') as f:
    yaml.dump(config, f)

# Sử dụng
parser = DXFParser('input.dxf')
entities = parser.parse()

generator = GCodeGenerator('custom_config.yaml')
gcode = generator.generate(entities)
generator.save_gcode(gcode, 'output.gcode')
```

### Ví dụ 3: Xử lý lỗi

```python
from src import DXFParser, PathOptimizer, GCodeGenerator
import logging

# Bật logging chi tiết
logging.basicConfig(level=logging.INFO)

try:
    # Đọc DXF
    parser = DXFParser('input.dxf')
    entities = parser.parse()
    
    if not entities:
        print("Cảnh báo: File DXF không chứa entities")
        exit(1)
    
    # Tối ưu hóa
    optimizer = PathOptimizer(tolerance=0.05)
    segments = optimizer.optimize(entities)
    
    # Sinh G-code
    generator = GCodeGenerator()
    gcode = generator.generate(segments)
    generator.save_gcode(gcode, 'output.gcode')
    
    print("✓ Chuyển đổi thành công!")
    
except FileNotFoundError:
    print("Lỗi: File DXF không tồn tại")
except Exception as e:
    print(f"Lỗi: {str(e)}")
```

## Cấu hình

### Tệp config.yaml

```yaml
machine:
  name: "CNC Wire Bending Pro 2026"
  max_speed: 100           # mm/s
  acceleration: 50         # mm/s²
  min_radius: 2.0          # mm - bán kính uốn nhỏ nhất
  max_wire_length: 5000    # mm

wire:
  diameter: 2.0            # mm
  material: "steel"        # steel, aluminum, copper, titanium

processing:
  tolerance: 0.1           # mm - sai số cho phép
  feed_rate: 50            # mm/min - tốc độ uốn
  cutting_speed: 200       # rpm - tốc độ cắt (nếu có)

optimization:
  enable_path_optimization: true
  merge_segments: true     # gộp các đoạn thẳng collinear
  min_segment_length: 0.5  # mm - độ dài tối thiểu

output:
  format: "fanuc"          # fanuc, siemens, heidenhain, generic
  decimal_places: 3        # số chữ số thập phân
  include_comments: true   # bao gồm bình luận

visualization:
  enable_preview: true
  show_grid: true
  grid_size: 10            # mm
```

### Các định dạng G-code

#### Fanuc
```
G21                    (Metric)
G90                    (Absolute positioning)
G40                    (Cancel cutter radius)
F50                    (Feed rate)
M3                     (Spindle on)
G00 X10 Y10           (Rapid move)
G01 X20 Y20           (Linear feed)
M5                    (Spindle off)
M30                   (End program)
```

#### Siemens Sinumerik
```
G21                   (Metric)
G90                   (Absolute)
G00 X10 Y10          (Rapid)
G01 X20 Y20          (Feed)
M30                  (End)
```

#### Heidenhain iTNC 530
```
BLK FORM 0.1 Z X 0 Y 0 Z 0
L CYCL DEF 7.0 DATUM
G00 X10 Y10
G01 X20 Y20
M30
```

## Xử lý sự cố

### Vấn đề 1: "File not found" error
**Giải pháp:**
```bash
# Kiểm tra file DXF tồn tại
ls -la input.dxf

# Hoặc sử dụng đường dẫn tuyệt đối
python -m src.main /full/path/to/input.dxf -o output.gcode
```

### Vấn đề 2: "No entities found"
**Giải pháp:**
- File DXF có thể trống hoặc không hỗ trợ
- Cấp nhật lên phiên bản mới nhất của ezdxf
```bash
pip install --upgrade ezdxf
```

### Vấn đề 3: G-code quá dài
**Giải pháp:**
- Giảm tolerance để đơn giản hóa đường đi
```bash
python -m src.main input.dxf -o output.gcode -t 0.2
```

### Vấn đề 4: Độ chính xác không đủ
**Giải pháp:**
- Tăng độ chính xác thập phân trong config
```yaml
output:
  decimal_places: 4  # Từ 3 lên 4
```

## Lệnh hữu ích

```bash
# Chạy tests
pytest tests/ -v
pytest tests/ --cov=src

# Kiểm tra cú pháp
python -m py_compile src/*.py

# Định dạng code
python -m black src/

# Tìm lỗi
python -m pylint src/

# Hiển thị giúp
python -m src.main --help
```

## Tài liệu thêm
- [API Documentation](API.md)
- [README](../README.md)
- [GitHub Issues](https://github.com/meoconhalogen/CNC-wire-bending-pro-2026/issues)
