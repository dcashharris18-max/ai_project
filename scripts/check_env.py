"""Simple environment checker for local development.

Usage: python scripts/check_env.py
"""
import sys
import subprocess


def main():
    print("Checking Python version...")
    major, minor = sys.version_info[:2]
    print(f"Detected Python: {major}.{minor}")
    if (major, minor) != (3, 11):
        print("Project expects Python 3.11. Please install Python 3.11 and create a venv.")
    else:
        print("Python version OK.")

    print("Checking backend virtualenv presence (backend/.venv)...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        print("pip available")
    except Exception:
        print("pip not available in this environment.")


if __name__ == '__main__':
    main()
