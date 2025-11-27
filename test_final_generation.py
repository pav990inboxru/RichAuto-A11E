# Final test to verify the complete code generation with all parameters
def test_final_code_generation():
    """Test the final code generation logic with all parameters"""
    
    # Parameters
    step = 40.0
    width = 200.0
    start_height = 4.0
    retract_height = 20.0  # New parameter
    cut_depth = 0.0
    plunge_feedrate = 3000.0
    cut_feedrate = 300.0
    start_y = 0.0
    end_y = 120.0  # Reduced for test
    
    # Generate the code following the original pattern logic
    code_lines = []
    code_lines.append("G54")
    
    current_y = start_y
    first = True
    
    while current_y <= end_y:
        if first:
            # First move to initial position
            code_lines.append(f"G00X0.000Y{current_y:03.0f}Z{start_height:0.3f}")
            code_lines.append(f"Z{start_height:0.3f}")  # Original has this duplicate line
            first = False
        else:
            # Subsequent moves to new Y positions
            code_lines.append(f"X0.000Y{current_y:03.0f}")
            code_lines.append(f"Z{start_height:0.3f}")  # Move to start height before cutting
        
        # Plunge to cut depth
        code_lines.append(f"G01Z{cut_depth:0.3f}F{plunge_feedrate:0.0f}")
        
        # Cut along X-axis
        code_lines.append(f"X{width:0.3f}F{cut_feedrate:0.0f}")
        
        # Retract to safe height
        code_lines.append(f"G00Z{retract_height:0.3f}")
        
        # Move to next Y position (but stay at safe height)
        current_y += step
        
        # If we still have more Y positions to cut
        if current_y <= end_y:
            # Original pattern shows move to X0.000Y[next] at safe height
            pass  # The next iteration will handle the Y move
    
    # Add final safe move if needed
    # code_lines.append(f"G00Z{retract_height:0.3f}")
    
    generated_code = "\n".join(code_lines)
    
    print("Generated final test code (matching original pattern):")
    print(generated_code)
    print(f"\nTotal lines: {len(code_lines)}")
    print(f"Number of cuts: {int((end_y-start_y)/step)+1}")
    
    return generated_code

if __name__ == "__main__":
    test_final_code_generation()