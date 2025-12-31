#!/bin/bash
# Setup script for NoFace - AI Motivational Video Generator

echo "=========================================="
echo "NoFace - Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

python_version=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $python_version found"
echo ""

# Check FFmpeg
echo "Checking FFmpeg installation..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠ FFmpeg is not installed"
    echo "FFmpeg is required for video generation"
    echo ""
    echo "Install FFmpeg:"
    echo "  macOS:   brew install ffmpeg"
    echo "  Linux:   sudo apt-get install ffmpeg"
    echo "  Windows: Download from https://ffmpeg.org/download.html"
    echo ""
else
    ffmpeg_version=$(ffmpeg -version | head -n1)
    echo "✓ $ffmpeg_version"
    echo ""
fi

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠ Virtual environment already exists"
    read -p "Do you want to recreate it? (y/N): " recreate
    if [ "$recreate" = "y" ] || [ "$recreate" = "Y" ]; then
        rm -rf venv
        python3 -m venv venv
        echo "✓ Virtual environment recreated"
    fi
else
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Create config file
echo "Setting up configuration..."
if [ ! -f "config.ini" ]; then
    cp config.example.ini config.ini
    echo "✓ Created config.ini from example"
else
    echo "⚠ config.ini already exists"
fi
echo ""

# Run verification
echo "Running setup verification..."
python3 test_setup.py
echo ""

echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To use NoFace:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the desktop application:"
echo "     python noface_app.py"
echo ""
echo "  3. Or use the command-line interface:"
echo "     python cli.py --help"
echo ""
echo "For YouTube integration:"
echo "  - Get OAuth2 credentials from Google Cloud Console"
echo "  - Save as client_secrets.json"
echo ""
echo "See README.md for detailed instructions."
