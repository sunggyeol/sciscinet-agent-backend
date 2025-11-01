#!/usr/bin/env python3
"""Test runner for SciSciNet Agent Backend"""
import sys
import subprocess

def main():
    """Run all tests"""
    print("Running SciSciNet Agent Backend Tests...")
    print("=" * 50)
    
    result = subprocess.run(
        ["pytest", "-v"],
        capture_output=False
    )
    
    if result.returncode == 0:
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ Some tests failed")
        print("=" * 50)
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())

