#!/usr/bin/env python3
"""
Test runner for WCC Certificate Automation

This script runs all unit and integration tests for the certificate automation system.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py -v           # Run with verbose output
    python run_tests.py --coverage   # Run with coverage report
"""

import sys
import os
import unittest
import argparse


def run_tests(verbosity=1, with_coverage=False):
    """Run all tests in the tests directory."""

    # Add src to path
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.insert(0, src_path)

    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')

    if with_coverage:
        try:
            import coverage
            cov = coverage.Coverage()
            cov.start()

            runner = unittest.TextTestRunner(verbosity=verbosity)
            result = runner.run(suite)

            cov.stop()
            cov.save()

            print("\n" + "="*70)
            print("Coverage Report:")
            print("="*70)
            cov.report()

            # Generate HTML coverage report
            html_dir = os.path.join(os.path.dirname(__file__), 'htmlcov')
            cov.html_report(directory=html_dir)
            print(f"\nHTML coverage report generated in: {html_dir}")

            return 0 if result.wasSuccessful() else 1

        except ImportError:
            print("Coverage package not installed. Install with: pip install coverage")
            print("Running tests without coverage...\n")

    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Run WCC Certificate Automation tests')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')
    parser.add_argument('-c', '--coverage', action='store_true',
                        help='Run with coverage report')

    args = parser.parse_args()

    verbosity = 2 if args.verbose else 1

    print("Running WCC Certificate Automation Tests")
    print("="*70)

    sys.exit(run_tests(verbosity=verbosity, with_coverage=args.coverage))


if __name__ == '__main__':
    main()
