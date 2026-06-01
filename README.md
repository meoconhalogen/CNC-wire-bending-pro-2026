# CNC Wire Bending Pro 2026

Chương trình chuyên nghiệp chuyển đổi file DXF thành G-code cho máy uốn dây CNC.

## Tính năng

- 📖 **Đọc file DXF**: Hỗ trợ các entities chính (lines, circles, arcs, polylines)
- 🔄 **Tối ưu hóa đường đi**: Giảm thời gian uốn và lượng dây thừa
- 🎯 **Sinh G-code**: Tạo lệnh điều khiển cho máy wire bending CNC
- ⚙️ **Cấu hình linh hoạt**: Tùy chỉnh tham số máy, tốc độ, độ chính xác
- 📊 **Visualization**: Hiển thị đường đi trước khi thực thi
- 📝 **Logging & Debug**: Theo dõi quá trình xử lý chi tiết

## Cấu trúc dự án

```
CNC-wire-bending-pro-2026/
├── src/
│   ├── dxf_parser.py          # Module đọc DXF
│   ├── geometry.py            # Các hàm hình học
│   ├── path_optimizer.py      # Tối ưu đường đi
│   ├── gcode_generator.py     # Tạo G-code
│   ├── __init__.py            # Package init
│   └── main.py                # Entry point
├── tests/
│   ├── test_dxf_parser.py
│   ├── test_geometry.py
│   └── test_gcode_generator.py
├── examples/
│   └── sample.dxf             # File DXF mẫu
├── docs/
│   ├── USAGE.md               # Hướng dẫn sử dụng
│   └── API.md                 # Tài liệu API
├── requirements.txt
├── config.yaml                # Cấu hình mặc định
├── setup.py
└── .gitignore
```

## Yêu cầu

- Python 3.8+
- Libraries: ezdxf, numpy, matplotlib, pyyaml

## Cài đặt

```bash
git clone https://github.com/meoconhalogen/CNC-wire-bending-pro-2026.git
cd CNC-wire-bending-pro-2026
pip install -r requirements.txt
```

## Sử dụng nhanh

### Từ command line:

```bash
python -m src.main input.dxf -o output.gcode
```

Tùy chọn:
- `-c, --config`: Tệp cấu hình YAML
- `-f, --format`: Định dạng G-code (fanuc, siemens, heidenhain)
- `-t, --tolerance`: Độ chính xác đơn giản hóa đường đi (mm)
- `-v, --verbose`: Xuất chi tiết

### Từ Python code:

```python
from src.dxf_parser import DXFParser
from src.path_optimizer import PathOptimizer
from src.gcode_generator import GCodeGenerator

# Đọc file DXF
parser = DXFParser('sample.dxf')
entities = parser.parse()
print(f"Tìm thấy {len(entities)} entities")

# Tối ưu hóa đường đi
optimizer = PathOptimizer(tolerance=0.1)
segments = optimizer.optimize(entities)
stats = optimizer.get_statistics()
print(f"Tổng độ dài dây: {stats['total_length']:.2f}mm")

# Tạo G-code
generator = GCodeGenerator(config_file='config.yaml')
gcode = generator.generate(segments)

# Lưu G-code
generator.save_gcode(gcode, 'output.gcode')
```

## Module chính

### 1. DXFParser
Đọc và phân tích file DXF, trích xuất các entities hình học:
- Lines (đoạn thẳng)
- Circles (hình tròn)
- Arcs (cung tròn)
- Polylines (đa tuyến)
- Splines (đường cong)

### 2. Geometry
Các hàm hình học và toán học:
- Tính khoảng cách, góc
- Kiểm tra giao điểm
- Làm mịn đường đi (Douglas-Peucker)
- Xoay, dịch chuyển điểm

### 3. PathOptimizer
Tối ưu hóa đường đi để uốn dây hiệu quả:
- Chuyển đổi các entities phức tạp thành đoạn thẳng
- Hợp nhất các đoạn gần nhau
- Sắp xếp lại để giảm khoảng cách di chuyển (TSP approximation)

### 4. GCodeGenerator
Sinh G-code cho máy CNC:
- Hỗ trợ định dạng: Fanuc, Siemens Sinumerik, Heidenhain
- Xuất lệnh rapid move (G00) và linear move (G01)
- Nhận xét chi tiết và thống kê

## Ví dụ

```bash
# Chuyển đổi DXF mặc định (Fanuc format)
python -m src.main examples/sample.dxf -o output.gcode

# Định dạng Siemens với độ chính xác 0.05mm
python -m src.main examples/sample.dxf -o output.gcode -f siemens -t 0.05

# Với cấu hình tùy chỉnh
python -m src.main examples/sample.dxf -o output.gcode -c my_config.yaml -v
```

## Cấu hình

Sửa `config.yaml` để tùy chỉnh:

```yaml
machine:
  name: "CNC Wire Bending Pro 2026"
  max_speed: 100        # mm/s
  feed_rate: 50         # mm/min
  min_radius: 2.0       # mm
  
wire:
  diameter: 2.0         # mm
  material: "steel"     # steel, aluminum, copper, titanium
  
output:
  format: "fanuc"       # fanuc, siemens, heidenhain, generic
  decimal_places: 3
  include_comments: true
```

## Kiểm thử

```bash
pytest tests/ -v
pytest tests/ --cov=src  # Với coverage report
```

## Liên hệ & Hỗ trợ

- Author: meoconhalogen
- GitHub: [CNC-wire-bending-pro-2026](https://github.com/meoconhalogen/CNC-wire-bending-pro-2026)
- License: MIT

---

**Status**: 🚀 Phát triển đang tiến hành - v2026.1.0