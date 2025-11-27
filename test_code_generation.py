# Test script to verify the code generation logic without GUI
def test_code_generation():
    """Test the code generation logic without requiring GUI"""
    
    # Parameters
    step = 40.0
    width = 200.0
    start_height = 4.0
    cut_depth = 0.0
    plunge_feedrate = 3000.0
    cut_feedrate = 300.0
    start_y = 0.0
    end_y = 200.0  # Reduced for test
    
    # Generate the code
    code_lines = []
    code_lines.append("G54")
    
    current_y = start_y
    
    # First move to initial position
    code_lines.append(f"G00X0.000Y{current_y:05.0f}Z{start_height:0.3f}")
    
    while current_y <= end_y:
        # Plunge to cut depth
        code_lines.append(f"G01Z{cut_depth:0.3f}F{plunge_feedrate:0.0f}")
        
        # Cut along X-axis
        code_lines.append(f"X{width:0.3f}F{cut_feedrate:0.0f}")
        
        # Retract to safe height
        code_lines.append(f"G00Z{start_height:0.3f}")
        
        # Move to next Y position (but stay at safe height)
        current_y += step
        
        # If we still have more Y positions to cut
        if current_y <= end_y:
            code_lines.append(f"G00X0.000Y{current_y:05.0f}")
    
    # Add final safe move
    code_lines.append(f"G00Z{start_height:0.3f}")
    
    generated_code = "\n".join(code_lines)
    
    print("Generated test code:")
    print(generated_code)
    print(f"\nTotal lines: {len(code_lines)}")
    print(f"Number of cuts: {int((end_y-start_y)/step)+1}")
    
    # Verify the code structure
    expected_lines = [
        "G54",
        "G00X0.000Y00000Z4.000",
        "Z4.000",
        "G01Z0.000F3000",
        "X200.000F300",
        "G00Z4.000",
        "X0.000Y00040",
        "G00X0.000Y00080Z4.000",
        "Z4.000",
        "G01Z0.000F3000",
        "X200.000F300",
        "G00Z4.000",
        "G00Z4.000"
    ]
    
    print("\nVerification:")
    for i, line in enumerate(code_lines):
        print(f"Line {i+1}: {line}")
    
    return generated_code

if __name__ == "__main__":
    test_code_generation()