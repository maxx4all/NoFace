# NoFace - AI Motivational Video Generator

A desktop application that automatically generates and publishes motivational videos to TikTok and YouTube using AI-powered content creation.

## Features

- 🎬 **AI-Powered Video Generation**: Automatically creates motivational videos with text-to-speech
- 🎨 **Customizable Visuals**: Gradient backgrounds with configurable colors
- 📢 **Text-to-Speech**: Converts motivational quotes to natural-sounding speech using gTTS
- 📤 **YouTube Integration**: Direct upload to YouTube with OAuth2 authentication
- 📱 **TikTok Support**: Prepares videos for TikTok with upload instructions
- 🖥️ **Desktop GUI**: Easy-to-use interface built with tkinter
- ⚙️ **Configurable Settings**: Customize video dimensions, FPS, colors, and more
- 📊 **Batch Processing**: Generate and upload multiple videos at once

## Requirements

- Python 3.8 or higher
- FFmpeg (required for video processing)
- ImageMagick (optional, for advanced text rendering)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/maxx4all/NoFace.git
cd NoFace
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

#### Windows
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

#### macOS
```bash
brew install ffmpeg
```

#### Linux
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

### 4. Configure API Credentials (Optional)

#### YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials JSON file and save it as `client_secrets.json` in the project directory

#### TikTok API Setup

TikTok's Content Posting API requires special approval:
1. Visit [TikTok for Developers](https://developers.tiktok.com/)
2. Apply for Content Posting API access
3. Once approved, configure your access token in the settings

Note: Without TikTok API access, videos can be uploaded manually to the TikTok app.

## Usage

### Running the Application

```bash
python noface_app.py
```

### Quick Start Guide

1. **Generate Videos**:
   - Open the "Generate Videos" tab
   - Enter motivational quotes (one per line) or load from a file
   - Configure number of videos to generate
   - Click "Generate Videos"
   - Videos will be saved to the output directory

2. **Publish Videos**:
   - Open the "Publish Videos" tab
   - Select the directory containing your videos
   - Choose videos to publish
   - Select publishing platforms (YouTube and/or TikTok)
   - Choose privacy settings
   - Click "Publish Selected Videos"

3. **Configure Settings**:
   - Open the "Settings" tab
   - Adjust video dimensions, FPS, and duration
   - Customize background colors
   - Configure API credentials
   - Save settings

### Configuration File

Copy the example configuration:

```bash
cp config.example.ini config.ini
```

Edit `config.ini` to customize default settings:

```ini
[API]
youtube_client_id = YOUR_YOUTUBE_CLIENT_ID
youtube_client_secret = YOUR_YOUTUBE_CLIENT_SECRET

[VIDEO]
width = 1080
height = 1920
fps = 30
duration = 15
output_dir = output

[CONTENT]
quotes_file = quotes.txt
background_type = gradient
background_color1 = #1a1a2e
background_color2 = #16213e
```

## Project Structure

```
NoFace/
├── noface_app.py           # Main desktop application
├── video_generator.py      # Video generation module
├── youtube_uploader.py     # YouTube API integration
├── tiktok_uploader.py      # TikTok integration
├── requirements.txt        # Python dependencies
├── config.example.ini      # Example configuration
├── quotes.txt             # Sample motivational quotes
├── README.md              # This file
└── .gitignore            # Git ignore rules
```

## Features in Detail

### Video Generation

The application uses MoviePy for video composition and gTTS (Google Text-to-Speech) for audio generation. Each video includes:

- Gradient background with customizable colors
- Centered text with automatic wrapping
- Natural text-to-speech narration
- Optimized for vertical video format (1080x1920)

### YouTube Publishing

- OAuth2 authentication for secure access
- Batch upload support
- Configurable privacy settings (public, private, unlisted)
- Automatic metadata including title, description, and tags
- Upload progress tracking

### TikTok Integration

- Video format optimized for TikTok (1080x1920, 30 FPS)
- Manual upload instructions provided
- Framework ready for TikTok API when available
- Batch preparation support

## Troubleshooting

### FFmpeg Not Found

If you get an FFmpeg error:
1. Ensure FFmpeg is installed
2. Add FFmpeg to your system PATH
3. Restart your terminal/IDE

### YouTube Authentication Issues

1. Ensure `client_secrets.json` is in the project directory
2. Check that YouTube Data API v3 is enabled in your Google Cloud project
3. Verify OAuth2 credentials are configured correctly

### Video Generation Fails

1. Check that all quotes are properly formatted (one per line)
2. Ensure output directory is writable
3. Verify FFmpeg is working: `ffmpeg -version`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- MoviePy for video processing
- gTTS for text-to-speech
- Google YouTube API for video uploads
- TikTok for platform support

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Roadmap

- [ ] Add more background styles (images, videos, animations)
- [ ] Support for multiple voices and languages
- [ ] Advanced text animations
- [ ] Music and sound effects
- [ ] Scheduled posting
- [ ] Analytics dashboard
- [ ] Custom fonts and styling
- [ ] Instagram Reels support
- [ ] Video templates