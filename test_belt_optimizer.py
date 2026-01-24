#!/usr/bin/env python3
"""
Test script for the Belt Cutting Optimizer
"""

from belt_cutting_optimizer import BeltCuttingOptimizer

def test_normal_case():
    """Test normal case with the example from the requirements"""
    print("Testing normal case...")
    optimizer = BeltCuttingOptimizer(roll_width=640, left_waste=30, right_waste=30)
    
    orders = [
        {'width': 50, 'length': 1200, 'quantity': 300},
        {'width': 80, 'length': 900, 'quantity': 150},
        {'width': 120, 'length': 1500, 'quantity': 100}
    ]
    
    report = optimizer.generate_report(orders)
    print(report)
    print("\n" + "="*60 + "\n")


def test_error_cases():
    """Test various error conditions"""
    print("Testing error cases...")
    optimizer = BeltCuttingOptimizer(roll_width=640, left_waste=30, right_waste=30)
    
    # Test 1: Empty order
    print("Test 1: Empty order")
    report = optimizer.generate_report([])
    if report.startswith("Error:"):
        print(f"✓ Correctly caught error: {report}")
    else:
        print("ERROR: Should have returned an error!")
    
    # Test 2: Width exceeds useful width
    print("\nTest 2: Width exceeds useful width")
    orders = [{'width': 700, 'length': 1000, 'quantity': 10}]  # 700 > 580
    report = optimizer.generate_report(orders)
    if report.startswith("Error:"):
        print(f"✓ Correctly caught error: {report}")
    else:
        print("ERROR: Should have returned an error!")
    
    # Test 3: Zero or negative values
    print("\nTest 3: Zero width")
    orders = [{'width': 0, 'length': 1000, 'quantity': 10}]
    report = optimizer.generate_report(orders)
    if report.startswith("Error:"):
        print(f"✓ Correctly caught error: {report}")
    else:
        print("ERROR: Should have returned an error!")
    
    print("\nTest 3b: Negative length")
    orders = [{'width': 50, 'length': -100, 'quantity': 10}]
    report = optimizer.generate_report(orders)
    if report.startswith("Error:"):
        print(f"✓ Correctly caught error: {report}")
    else:
        print("ERROR: Should have returned an error!")
    
    print("\nTest 3c: Zero quantity")
    orders = [{'width': 50, 'length': 1000, 'quantity': 0}]
    report = optimizer.generate_report(orders)
    if report.startswith("Error:"):
        print(f"✓ Correctly caught error: {report}")
    else:
        print("ERROR: Should have returned an error!")


def test_simple_case():
    """Test a simple case that should work well"""
    print("\nTesting simple case...")
    optimizer = BeltCuttingOptimizer(roll_width=640, left_waste=30, right_waste=30)
    
    # Simple case: only one type of belt
    orders = [
        {'width': 100, 'length': 1000, 'quantity': 50}
    ]
    
    report = optimizer.generate_report(orders)
    print(report)


if __name__ == "__main__":
    test_normal_case()
    test_error_cases()
    test_simple_case()
    print("\nAll tests completed!")