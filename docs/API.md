# API Documentation - CNC Wire Bending Pro 2026

## Mục lục
- [DXFParser](#dxfparser)
- [Geometry](#geometry)
- [PathOptimizer](#pathoptimizer)
- [GCodeGenerator](#gcodegenerator)

## DXFParser

Module đọc và phân tích file DXF.

### Class: `Point`

Diễn tả một điểm 2D/3D.

```python
@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0
```

**Tính chất:**
- `x`: Tọa độ X (mm)
- `y`: Tọa độ Y (mm)
- `z`: Tọa độ Z (mm, mặc định 0)

**Ví dụ:**
```python
from src.dxf_parser import Point

point = Point(10.5, 20.3, 0)
print(point)  # Point(10.500, 20.300, 0.000)
```

### Class: `LineSegment`

Diễn tả một đoạn thẳng.

```python
@dataclass
class LineSegment:
    start: Point
    end: Point
    entity_type: EntityType = EntityType.LINE
```

**Ví dụ:**
```python
from src.dxf_parser import LineSegment, Point

line = LineSegment(
    start=Point(0, 0),
    end=Point(10, 10)
)
print(line)  # Line(Point(0.000, 0.000, 0.000) -> Point(10.000, 10.000, 0.000))
```

### Class: `CircleEntity`

Diễn tả một đường tròn.

```python
@dataclass
class CircleEntity:
    center: Point
    radius: float
    entity_type: EntityType = EntityType.CIRCLE
```

### Class: `ArcEntity`

Diễn tả một cung tròn.

```python
@dataclass
class ArcEntity:
    center: Point
    radius: float
    start_angle: float  # độ
    end_angle: float    # độ
    entity_type: EntityType = EntityType.ARC
```

### Class: `PolylineEntity`

Diễn tả một đa tuyến.

```python
@dataclass
class PolylineEntity:
    points: List[Point]
    is_closed: bool = False
    entity_type: EntityType = EntityType.POLYLINE
```

### Class: `DXFParser`

Parser chính đọc file DXF.

#### Method: `__init__(filepath: str)`

```python
parser = DXFParser('drawing.dxf')
```

#### Method: `parse() -> List[Any]`

Phân tích file DXF và trả về danh sách entities.

```python
entities = parser.parse()
print(f"Tìm thấy {len(entities)} entities")
```

**Trả về:**
- Danh sách các entities (LineSegment, CircleEntity, ArcEntity, PolylineEntity)

**Ngoại lệ:**
- `FileNotFoundError`: File không tồn tại
- `Exception`: Lỗi đọc DXF

#### Method: `get_bounds() -> Dict[str, float]`

Lấy hộp giới hạn của tất cả entities.

```python
bounds = parser.get_bounds()
print(f"Width: {bounds['width']}mm, Height: {bounds['height']}mm")
```

**Trả về:**
```python
{
    'min_x': float,
    'max_x': float,
    'min_y': float,
    'max_y': float,
    'width': float,
    'height': float
}
```

#### Method: `get_entity_count() -> int`

Lấy số lượng entities.

```python
count = parser.get_entity_count()
print(f"Có {count} entities")
```

---

## Geometry

Module chứa các hàm toán học hình học.

### Class: `Geometry`

#### Static Method: `distance(p1: Point, p2: Point) -> float`

Tính khoảng cách Euclidean 3D.

```python
from src.geometry import Geometry
from src.dxf_parser import Point

dist = Geometry.distance(Point(0, 0, 0), Point(3, 4, 0))
print(dist)  # 5.0
```

#### Static Method: `distance_2d(p1: Point, p2: Point) -> float`

Tính khoảng cách 2D (bỏ qua Z).

```python
dist = Geometry.distance_2d(Point(0, 0), Point(3, 4))
print(dist)  # 5.0
```

#### Static Method: `angle(p1: Point, p2: Point) -> float`

Tính góc từ p1 đến p2 (độ, 0-360).

```python
angle = Geometry.angle(Point(0, 0), Point(1, 1))
print(angle)  # 45.0
```

#### Static Method: `angle_between(p1: Point, p2: Point, p3: Point) -> float`

Tính góc tại p2 giữa p1-p2-p3 (độ, 0-180).

```python
angle = Geometry.angle_between(
    Point(0, 0),
    Point(1, 0),
    Point(1, 1)
)
print(angle)  # 90.0
```

#### Static Method: `point_on_circle(center: Point, radius: float, angle: float) -> Point`

Tính điểm trên đường tròn tại góc cho trước.

```python
p = Geometry.point_on_circle(Point(0, 0), 10, 90)
print(p)  # Point(0.000, 10.000, 0.000)
```

#### Static Method: `point_on_line(p1: Point, p2: Point, t: float) -> Point`

Tính điểm nội suy trên đường thẳng (t: 0-1).

```python
p = Geometry.point_on_line(Point(0, 0), Point(10, 10), 0.5)
print(p)  # Point(5.000, 5.000, 0.000)
```

#### Static Method: `line_intersection(p1, p2, p3, p4) -> Tuple[bool, Point]`

Tính giao điểm của hai đường thẳng.

```python
found, point = Geometry.line_intersection(
    Point(0, 0), Point(10, 0),
    Point(5, -5), Point(5, 5)
)
if found:
    print(f"Giao điểm: {point}")
```

#### Static Method: `point_to_line_distance(point, p1, p2) -> float`

Tính khoảng cách vuông góc từ điểm đến đường thẳng.

```python
dist = Geometry.point_to_line_distance(
    Point(5, 5),
    Point(0, 0),
    Point(10, 0)
)
print(dist)  # 5.0
```

#### Static Method: `rotate_point(point, center, angle) -> Point`

Xoay điểm quanh tâm.

```python
p = Geometry.rotate_point(
    Point(10, 0),
    Point(0, 0),
    90  # degrees
)
print(p)  # Point(0.000, 10.000, 0.000)
```

#### Static Method: `arc_length(radius, start_angle, end_angle) -> float`

Tính độ dài cung tròn.

```python
length = Geometry.arc_length(10, 0, 90)
print(length)  # ~15.7 (π * 10 / 2)
```

---

## PathOptimizer

Module tối ưu hóa đường đi uốn dây.

### Class: `PathOptimizer`

#### Method: `__init__(tolerance: float = 0.1)`

```python
from src.path_optimizer import PathOptimizer

optimizer = PathOptimizer(tolerance=0.1)  # mm
```

#### Method: `optimize(entities: List[Any]) -> List[LineSegment]`

Tối ưu hóa danh sách entities.

```python
entities = parser.parse()
segments = optimizer.optimize(entities)
print(f"Tối ưu hóa thành {len(segments)} segments")
```

**Bước xử lý:**
1. Chuyển đổi entities thành line segments
2. Hợp nhất các segments collinear
3. Sắp xếp để minimize khoảng cách di chuyển

#### Method: `calculate_total_length(segments: List[LineSegment]) -> float`

Tính tổng độ dài đường đi.

```python
total = optimizer.calculate_total_length(segments)
print(f"Tổng độ dài: {total:.2f}mm")
```

#### Method: `get_statistics() -> dict`

Lấy thống kê tối ưu hóa.

```python
stats = optimizer.get_statistics()
print(stats)
# {
#     'num_segments': 42,
#     'total_length': 156.78,
#     'avg_segment_length': 3.73
# }
```

---

## GCodeGenerator

Module tạo G-code cho máy CNC.

### Class: `GCodeGenerator`

#### Method: `__init__(config_file: str = None)`

```python
from src.gcode_generator import GCodeGenerator

# Sử dụng config mặc định
generator = GCodeGenerator()

# Hoặc load config từ file
generator = GCodeGenerator('config.yaml')
```

#### Method: `generate(segments: List[LineSegment]) -> str`

Tạo G-code từ danh sách segments.

```python
gcode = generator.generate(segments)
print(gcode)
```

**Trả về:** Chuỗi G-code đầy đủ

#### Method: `save_gcode(gcode: str, filepath: str)`

Lưu G-code ra file.

```python
generator.save_gcode(gcode, 'output.gcode')
```

### Class: `GCodeFormat`

Các định dạng G-code được hỗ trợ.

```python
from src.gcode_generator import GCodeFormat

print(GCodeFormat.FANUC)
print(GCodeFormat.SIEMENS)
print(GCodeFormat.HEIDENHAIN)
```

**Mỗi format chứa:**
- `name`: Tên máy
- `rapid`: Lệnh rapid move
- `linear`: Lệnh linear move
- `arc_cw`: Lệnh cung tròn thuận chiều
- `arc_ccw`: Lệnh cung tròn ngược chiều
- `start_code`: Mã khởi động
- `end_code`: Mã kết thúc

---

## Ví dụ hoàn chỉnh

```python
from src import DXFParser, PathOptimizer, GCodeGenerator
import logging

logging.basicConfig(level=logging.INFO)

# Bước 1: Đọc DXF
parser = DXFParser('drawing.dxf')
entities = parser.parse()

# Bước 2: Tối ưu hóa
optimizer = PathOptimizer(tolerance=0.05)
segments = optimizer.optimize(entities)
stats = optimizer.get_statistics()

print(f"Segments: {stats['num_segments']}")
print(f"Độ dài dây: {stats['total_length']:.2f}mm")
print(f"Độ dài trung bình: {stats['avg_segment_length']:.2f}mm")

# Bước 3: Sinh G-code
generator = GCodeGenerator('config.yaml')
gcode = generator.generate(segments)

# Bước 4: Lưu
generator.save_gcode(gcode, 'output.gcode')
print("✓ Hoàn tất!")
```

---

**Phiên bản:** 2026.1.0  
**Cập nhật lần cuối:** 2026-06-01
