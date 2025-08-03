#!/usr/bin/env python3
"""
Test script for Plotext-Prometheus
This script demonstrates various usage examples and can be used to test the tool
"""

import subprocess
import sys
import time
from typing import List

def run_command(cmd: List[str], description: str) -> bool:
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Command executed successfully")
            return True
        else:
            print(f"❌ Command failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def test_help():
    """Test help functionality"""
    return run_command(['python', 'plotext_prom.py', '--help'], "Help command")

def test_basic_queries(prometheus_url: str = "http://localhost:9090"):
    """Test basic Prometheus queries"""
    
    # Test queries that should work on most Prometheus setups
    test_cases = [
        {
            'cmd': ['python', 'plotext_prom.py', '-q', 'up', '-u', prometheus_url],
            'desc': 'Basic up metric (instant query)'
        },
        {
            'cmd': ['python', 'plotext_prom.py', '-q', 'up', '-r', '5m', '-u', prometheus_url],
            'desc': 'Up metric over 5 minutes (range query)'
        },
        {
            'cmd': ['python', 'plotext_prom.py', '-q', 'prometheus_build_info', '-u', prometheus_url],
            'desc': 'Prometheus build info'
        }
    ]
    
    results = []
    for test_case in test_cases:
        success = run_command(test_case['cmd'], test_case['desc'])
        results.append(success)
        time.sleep(1)  # Brief pause between tests
    
    return results

def test_with_config():
    """Test using configuration file"""
    return run_command(
        ['python', 'plotext_prom.py', '-q', 'up', '-c', 'config.yaml'],
        "Query using configuration file"
    )

def main():
    """Run all tests"""
    print("Plotext-Prometheus Test Suite")
    print("="*60)
    
    # Test help first
    help_success = test_help()
    
    # Get Prometheus URL from user
    prometheus_url = input("\nEnter your Prometheus URL (default: http://localhost:9090): ").strip()
    if not prometheus_url:
        prometheus_url = "http://localhost:9090"
    
    print(f"Testing with Prometheus URL: {prometheus_url}")
    
    # Test basic queries
    query_results = test_basic_queries(prometheus_url)
    
    # Test with config
    config_success = test_with_config()
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print('='*60)
    print(f"Help command: {'✅' if help_success else '❌'}")
    print(f"Basic queries: {sum(query_results)}/{len(query_results)} passed")
    print(f"Config file test: {'✅' if config_success else '❌'}")
    
    total_tests = 1 + len(query_results) + 1
    passed_tests = int(help_success) + sum(query_results) + int(config_success)
    
    print(f"Overall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! The tool is working correctly.")
    else:
        print(f"\n⚠️  Some tests failed. Check your Prometheus setup and network connectivity.")
        print("Common issues:")
        print("- Prometheus server not running or not accessible")
        print("- Wrong URL or port")
        print("- Network connectivity issues")
        print("- Missing dependencies")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)