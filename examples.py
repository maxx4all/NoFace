#!/usr/bin/env python3
"""
Example script demonstrating programmatic usage of NoFace modules.
This shows how to use the video generator and uploaders in your own scripts.
"""

from video_generator import VideoGenerator
from youtube_uploader import YouTubeUploader
from tiktok_uploader import TikTokUploader


def example_generate_single_video():
    """Example: Generate a single motivational video."""
    print("Example 1: Generate a single video")
    print("-" * 50)
    
    # Create video generator
    generator = VideoGenerator(
        width=1080,
        height=1920,
        fps=30,
        duration=15
    )
    
    # Generate video
    quote = "The only way to do great work is to love what you do."
    output_path = "output/example_video.mp4"
    
    print(f"Generating video: {quote}")
    video_path = generator.create_video(
        quote=quote,
        output_path=output_path,
        bg_color1='#1a1a2e',
        bg_color2='#16213e'
    )
    
    print(f"✓ Video created: {video_path}")
    print()


def example_generate_batch():
    """Example: Generate multiple videos from a list of quotes."""
    print("Example 2: Generate batch of videos")
    print("-" * 50)
    
    # Create video generator
    generator = VideoGenerator(width=1080, height=1920, fps=30)
    
    # List of quotes
    quotes = [
        "Success is not final, failure is not fatal.",
        "Believe you can and you're halfway there.",
        "The future belongs to those who believe in their dreams."
    ]
    
    # Generate videos
    print(f"Generating {len(quotes)} videos...")
    video_paths = generator.create_batch_videos(
        quotes=quotes,
        output_dir="output/batch",
        bg_color1='#2d3436',
        bg_color2='#0984e3'
    )
    
    print(f"✓ Created {len(video_paths)} videos")
    for path in video_paths:
        print(f"  - {path}")
    print()


def example_youtube_upload():
    """Example: Upload a video to YouTube (requires OAuth2 credentials)."""
    print("Example 3: Upload to YouTube")
    print("-" * 50)
    
    # Note: This requires client_secrets.json file
    try:
        uploader = YouTubeUploader('client_secrets.json')
        
        # Upload a video
        video_id = uploader.upload_video(
            video_path='output/example_video.mp4',
            title='Daily Motivation #1',
            description='Motivational quote to inspire your day. #motivation #inspiration',
            tags=['motivation', 'inspiration', 'success'],
            privacy_status='private'  # Start with private
        )
        
        if video_id:
            print(f"✓ Uploaded to YouTube: https://www.youtube.com/watch?v={video_id}")
    
    except FileNotFoundError:
        print("⚠ client_secrets.json not found")
        print("  Get OAuth2 credentials from Google Cloud Console")
        print("  See README.md for instructions")
    
    print()


def example_custom_colors():
    """Example: Generate video with custom gradient colors."""
    print("Example 4: Custom gradient colors")
    print("-" * 50)
    
    generator = VideoGenerator()
    
    # Try different color combinations
    color_schemes = [
        ('#FF6B6B', '#4ECDC4'),  # Coral to Teal
        ('#A8E6CF', '#3D84A8'),  # Mint to Blue
        ('#FFA07A', '#FFD700'),  # Light Salmon to Gold
    ]
    
    quote = "Every day is a new beginning."
    
    for i, (color1, color2) in enumerate(color_schemes, 1):
        output_path = f"output/custom_colors_{i}.mp4"
        print(f"Creating video with colors {color1} → {color2}")
        
        generator.create_video(
            quote=quote,
            output_path=output_path,
            bg_color1=color1,
            bg_color2=color2
        )
        
        print(f"✓ Created: {output_path}")
    
    print()


def example_tiktok_preparation():
    """Example: Prepare videos for TikTok upload."""
    print("Example 5: Prepare for TikTok")
    print("-" * 50)
    
    uploader = TikTokUploader()
    uploader.authenticate()
    
    # Show upload instructions
    print(uploader.get_upload_instructions())


def main():
    """Run all examples."""
    print("=" * 60)
    print("NoFace - Programmatic Usage Examples")
    print("=" * 60)
    print()
    
    print("This script demonstrates how to use NoFace modules")
    print("programmatically in your own Python scripts.")
    print()
    
    # Note: Uncomment examples you want to run
    
    print("To run examples, uncomment them in the main() function:")
    print()
    print("# example_generate_single_video()")
    print("# example_generate_batch()")
    print("# example_youtube_upload()")
    print("# example_custom_colors()")
    print("# example_tiktok_preparation()")
    print()
    
    print("Note: Examples require FFmpeg and Python dependencies to be installed.")
    print("Run: pip install -r requirements.txt")
    print()
    
    # Uncomment to run examples:
    # example_generate_single_video()
    # example_generate_batch()
    # example_youtube_upload()
    # example_custom_colors()
    # example_tiktok_preparation()


if __name__ == '__main__':
    main()
