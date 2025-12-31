#!/usr/bin/env python3
"""
Test script to verify NoFace application structure and dependencies.
Run this to check if the application is properly set up.
"""
import sys
import os


def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"  ✗ Python {version.major}.{version.minor} detected")
        print("  ! Python 3.8 or higher is required")
        return False
    print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_module(module_name, package_name=None):
    """Check if a Python module is installed."""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"  ✓ {package_name}")
        return True
    except ImportError:
        print(f"  ✗ {package_name} not installed")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    print("\nChecking Python dependencies...")
    
    dependencies = [
        ('PIL', 'Pillow'),
        ('moviepy', 'moviepy'),
        ('gtts', 'gTTS'),
        ('googleapiclient', 'google-api-python-client'),
        ('google.auth', 'google-auth'),
        ('requests', 'requests'),
        ('tkinter', 'tkinter'),
    ]
    
    all_installed = True
    for module, package in dependencies:
        if not check_module(module, package):
            all_installed = False
    
    return all_installed


def check_ffmpeg():
    """Check if FFmpeg is installed."""
    print("\nChecking FFmpeg...")
    import subprocess
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✓ {version_line}")
            return True
        else:
            print("  ✗ FFmpeg not working properly")
            return False
    except FileNotFoundError:
        print("  ✗ FFmpeg not found in PATH")
        print("  ! Install FFmpeg: https://ffmpeg.org/download.html")
        return False
    except Exception as e:
        print(f"  ✗ Error checking FFmpeg: {e}")
        return False


def check_files():
    """Check if required files exist."""
    print("\nChecking required files...")
    
    files = [
        'noface_app.py',
        'cli.py',
        'video_generator.py',
        'youtube_uploader.py',
        'tiktok_uploader.py',
        'requirements.txt',
        'quotes.txt',
        'config.example.ini',
        'README.md'
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} not found")
            all_exist = False
    
    return all_exist


def check_syntax():
    """Check syntax of Python files."""
    print("\nChecking Python syntax...")
    
    files = [
        'noface_app.py',
        'cli.py',
        'video_generator.py',
        'youtube_uploader.py',
        'tiktok_uploader.py'
    ]
    
    all_valid = True
    for file in files:
        if os.path.exists(file):
            try:
                import ast
                with open(file, 'r') as f:
                    ast.parse(f.read())
                print(f"  ✓ {file}")
            except SyntaxError as e:
                print(f"  ✗ {file}: {e}")
                all_valid = False
    
    return all_valid


def main():
    """Main test function."""
    print("=" * 60)
    print("NoFace - Application Setup Verification")
    print("=" * 60)
    
    results = {
        'Python Version': check_python_version(),
        'Required Files': check_files(),
        'Python Syntax': check_syntax(),
        'Dependencies': check_dependencies(),
        'FFmpeg': check_ffmpeg()
    }
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = True
    for check, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{check:20s}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All checks passed! The application is ready to use.")
        print("\nRun the application:")
        print("  python noface_app.py    # Desktop GUI")
        print("  python cli.py --help    # Command-line interface")
    else:
        print("\n✗ Some checks failed. Please install missing dependencies.")
        print("\nTo install dependencies:")
        print("  pip install -r requirements.txt")
        print("\nTo install FFmpeg:")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        print("  macOS:   brew install ffmpeg")
        print("  Linux:   sudo apt-get install ffmpeg")
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
