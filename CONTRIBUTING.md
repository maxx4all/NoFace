# Contributing to NoFace

Thank you for your interest in contributing to NoFace! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### Suggesting Features

Feature suggestions are welcome! Please open an issue with:
- A clear description of the feature
- Use cases and benefits
- Any implementation ideas you have

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature-name`)
7. Open a Pull Request

### Code Style

- Follow PEP 8 style guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise

### Testing

- Test your changes before submitting a PR
- Ensure existing functionality still works
- Add tests for new features if applicable

## Development Setup

1. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/NoFace.git
cd NoFace
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install FFmpeg (see README.md for instructions)

## Project Structure

- `noface_app.py` - Main desktop GUI application
- `cli.py` - Command-line interface
- `video_generator.py` - Video generation logic
- `youtube_uploader.py` - YouTube API integration
- `tiktok_uploader.py` - TikTok integration
- `quotes.txt` - Sample motivational quotes
- `config.example.ini` - Example configuration

## Questions?

Feel free to open an issue for any questions or concerns!
