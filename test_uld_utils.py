"""Test script for ULD utility functions.

This script tests all the local Python utility functions in uld_utils.py
to ensure they work correctly before deployment.
"""

import sys
import os
import json

# Add src/agents to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'agents'))

from uld_utils import (
    calculate_total_weight,
    calculate_total_volume,
    validate_weight_constraints,
    calculate_uld_requirements,
    check_dimensional_fit,
    compare_uld_options
)


def test_calculate_total_weight():
    """Test calculate_total_weight function."""
    print("\n" + "="*70)
    print("TEST 1: calculate_total_weight")
    print("="*70)
    
    cargo_items = json.dumps([
        {"weight": 500, "quantity": 5},
        {"weight": 300, "quantity": 3}
    ])
    
    result = calculate_total_weight(cargo_items)
    print(result)
    assert "3400 kg" in result, "Total weight calculation failed"
    print("✅ PASSED")


def test_calculate_total_volume():
    """Test calculate_total_volume function."""
    print("\n" + "="*70)
    print("TEST 2: calculate_total_volume")
    print("="*70)
    
    cargo_items = json.dumps([
        {"length": 120, "width": 100, "height": 80, "quantity": 5}
    ])
    
    result = calculate_total_volume(cargo_items)
    print(result)
    assert "4.80 cubic meters" in result or "4.8 cubic meters" in result, "Volume calculation failed"
    print("✅ PASSED")


def test_validate_weight_constraints_valid():
    """Test validate_weight_constraints with valid weight."""
    print("\n" + "="*70)
    print("TEST 3: validate_weight_constraints (VALID)")
    print("="*70)
    
    result = validate_weight_constraints("AKE", 1400, True)
    print(result)
    assert "✅ VALID" in result, "Weight validation should pass"
    print("✅ PASSED")


def test_validate_weight_constraints_invalid():
    """Test validate_weight_constraints with invalid weight."""
    print("\n" + "="*70)
    print("TEST 4: validate_weight_constraints (INVALID)")
    print("="*70)
    
    result = validate_weight_constraints("AKE", 2000, True)
    print(result)
    assert "❌ INVALID" in result or "EXCEEDS" in result, "Weight validation should fail"
    print("✅ PASSED")


def test_calculate_uld_requirements():
    """Test calculate_uld_requirements function."""
    print("\n" + "="*70)
    print("TEST 5: calculate_uld_requirements")
    print("="*70)
    
    result = calculate_uld_requirements(2500, 9.0, "AKE")
    print(result)
    assert "ULDs Required:" in result, "ULD requirements calculation failed"
    print("✅ PASSED")


def test_check_dimensional_fit_valid():
    """Test check_dimensional_fit with valid dimensions."""
    print("\n" + "="*70)
    print("TEST 6: check_dimensional_fit (FITS)")
    print("="*70)
    
    result = check_dimensional_fit(120, 100, 150, "AKE")
    print(result)
    assert "✅ FITS" in result, "Dimensional fit should pass"
    print("✅ PASSED")


def test_check_dimensional_fit_invalid():
    """Test check_dimensional_fit with invalid dimensions."""
    print("\n" + "="*70)
    print("TEST 7: check_dimensional_fit (DOES NOT FIT)")
    print("="*70)
    
    result = check_dimensional_fit(200, 200, 200, "AKE")
    print(result)
    assert "❌ DOES NOT FIT" in result or "EXCEEDS" in result, "Dimensional fit should fail"
    print("✅ PASSED")


def test_compare_uld_options():
    """Test compare_uld_options function."""
    print("\n" + "="*70)
    print("TEST 8: compare_uld_options")
    print("="*70)
    
    result = compare_uld_options(2500, 9.0)
    print(result)
    assert "RECOMMENDED" in result or "Recommendation:" in result, "ULD comparison failed"
    print("✅ PASSED")


def test_error_handling():
    """Test error handling with invalid inputs."""
    print("\n" + "="*70)
    print("TEST 9: Error Handling")
    print("="*70)
    
    # Test with invalid JSON
    result = calculate_total_weight("invalid json")
    print("Invalid JSON test:")
    print(result)
    assert "Error" in result, "Should handle invalid JSON"
    
    # Test with unknown ULD type
    result = validate_weight_constraints("INVALID", 1000, True)
    print("\nUnknown ULD type test:")
    print(result)
    assert "ERROR" in result or "Unknown" in result, "Should handle unknown ULD type"
    
    print("✅ PASSED")


def run_all_tests():
    """Run all utility function tests."""
    print("\n" + "="*70)
    print("ULD UTILITY FUNCTIONS TEST SUITE")
    print("="*70)
    
    tests = [
        test_calculate_total_weight,
        test_calculate_total_volume,
        test_validate_weight_constraints_valid,
        test_validate_weight_constraints_invalid,
        test_calculate_uld_requirements,
        test_check_dimensional_fit_valid,
        test_check_dimensional_fit_invalid,
        test_compare_uld_options,
        test_error_handling
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n❌ FAILED: {test.__name__}")
            print(f"Error: {str(e)}")
            failed += 1
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total Tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠️  {failed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
