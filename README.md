# Belt Cutting Optimizer

A Python program for optimizing the cutting of roll material into belts to minimize waste.

## Features

- Calculates optimal cutting patterns for roll materials
- Minimizes waste by width and length
- Handles multiple belt sizes simultaneously
- Provides detailed reports on material usage and waste
- Validates input data and provides clear error messages

## Parameters

- **Roll width**: 640 mm (default)
- **Left waste**: 30 mm (default)
- **Right waste**: 30 mm (default)
- **Useful width**: 580 mm (calculated as 640 - 30 - 30)

## Usage

```python
from belt_cutting_optimizer import BeltCuttingOptimizer

# Initialize optimizer with roll parameters
optimizer = BeltCuttingOptimizer(roll_width=640, left_waste=30, right_waste=30)

# Define your orders
orders = [
    {'width': 50, 'length': 1200, 'quantity': 300},
    {'width': 80, 'length': 900, 'quantity': 150},
    {'width': 120, 'length': 1500, 'quantity': 100}
]

# Generate the optimization report
report = optimizer.generate_report(orders)
print(report)
```

## Output Format

The program outputs a comprehensive report with:

1. **Material consumption**: Total roll length used
2. **Cutting plan**: Which blanks to cut and how many times
3. **Detailed layout**: How each blank is arranged by width and length
4. **Production summary**: Required vs produced quantities
5. **Waste analysis**: Width waste, length waste, and efficiency percentage

## Error Handling

The program validates input and returns appropriate error messages for:
- Empty order tables
- Belt widths exceeding useful roll width
- Non-positive dimensions or quantities
- Invalid data types

## Units

All measurements are in millimeters (mm).
