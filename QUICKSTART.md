# Quick Start Guide

Get started with NoFace in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- FFmpeg (for video processing)

## Installation

### Option 1: Automated Setup (Linux/macOS)

```bash
# Clone the repository
git clone https://github.com/maxx4all/NoFace.git
cd NoFace

# Run setup script
./setup.sh
```

### Option 2: Manual Setup (All Platforms)

```bash
# Clone the repository
git clone https://github.com/maxx4all/NoFace.git
cd NoFace

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create config file
cp config.example.ini config.ini
```

## First Video

### Using Desktop GUI

```bash
python noface_app.py
```

1. In the "Generate Videos" tab, you'll see sample motivational quotes
2. Click "Generate Videos" to create your first video
3. Videos will be saved in the `output` folder

### Using Command-Line

```bash
# Generate a single video
python cli.py generate -n 1

# Generate 5 videos
python cli.py generate -n 5

# Custom output directory
python cli.py generate -n 3 -o my_videos
```

## Publishing Videos

### YouTube Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop application)
5. Download credentials and save as `client_secrets.json`

### Publish to YouTube

```bash
# Using CLI
python cli.py publish --youtube --privacy private

# Using GUI
# 1. Open "Publish Videos" tab
# 2. Select videos
# 3. Check "Publish to YouTube"
# 4. Click "Publish Selected Videos"
```

### TikTok Upload

TikTok requires Content Posting API approval. Until then:

1. Generate videos with NoFace
2. Transfer videos to your mobile device
3. Upload manually to TikTok app

For API access, apply at: https://developers.tiktok.com/

## Customization

Edit `config.ini` to customize:

- Video dimensions (default: 1080x1920 for vertical format)
- Background colors (gradient)
- Output directory
- Video duration and FPS

## Troubleshooting

### FFmpeg Not Found

**Error**: `FFmpeg not found in PATH`

**Solution**:
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'PIL'`

**Solution**:
```bash
pip install -r requirements.txt
```

### YouTube Authentication

**Error**: `Client secrets file not found`

**Solution**: Download OAuth2 credentials from Google Cloud Console and save as `client_secrets.json`

## Next Steps

- Add your own motivational quotes to `quotes.txt`
- Customize background colors in settings
- Generate videos in batch
- Schedule automated publishing
- Experiment with different video styles

## Getting Help

- Read the full [README.md](README.md)
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for development setup
- Open an issue on GitHub for bugs or questions

## Example Workflow

```bash
# 1. Generate 10 videos
python cli.py generate -n 10 -o my_campaign

# 2. Review videos in my_campaign/ folder

# 3. Publish to YouTube (private first)
python cli.py publish -d my_campaign --youtube --privacy private

# 4. Review on YouTube, then make public via YouTube Studio
```

Happy creating! 🎬
