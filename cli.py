#!/usr/bin/env python3
"""
Command-line interface for NoFace - AI Motivational Video Generator.
"""
import argparse
import os
import sys
import random
from pathlib import Path

from video_generator import VideoGenerator
from youtube_uploader import YouTubeUploader
from tiktok_uploader import TikTokUploader


def load_quotes(quotes_file):
    """Load quotes from file."""
    if not os.path.exists(quotes_file):
        print(f"Error: Quotes file not found: {quotes_file}")
        sys.exit(1)
    
    with open(quotes_file, 'r', encoding='utf-8') as f:
        quotes = [line.strip() for line in f if line.strip()]
    
    return quotes


def generate_command(args):
    """Generate videos from quotes."""
    print("NoFace - Video Generation")
    print("=" * 50)
    
    # Load quotes
    quotes = load_quotes(args.quotes_file)
    print(f"Loaded {len(quotes)} quotes from {args.quotes_file}")
    
    # Select quotes to use
    if args.num_videos > len(quotes):
        selected_quotes = [random.choice(quotes) for _ in range(args.num_videos)]
    else:
        selected_quotes = random.sample(quotes, args.num_videos)
    
    print(f"Generating {len(selected_quotes)} videos...")
    
    # Initialize generator
    generator = VideoGenerator(
        width=args.width,
        height=args.height,
        fps=args.fps,
        duration=args.duration
    )
    
    # Generate videos
    video_paths = generator.create_batch_videos(
        selected_quotes,
        args.output_dir,
        args.color1,
        args.color2
    )
    
    print(f"\n✓ Successfully generated {len(video_paths)} videos!")
    print(f"Videos saved to: {args.output_dir}")
    
    for path in video_paths:
        print(f"  - {path}")


def publish_command(args):
    """Publish videos to platforms."""
    print("NoFace - Video Publishing")
    print("=" * 50)
    
    # Get video files
    if not os.path.exists(args.video_dir):
        print(f"Error: Video directory not found: {args.video_dir}")
        sys.exit(1)
    
    video_files = [f for f in os.listdir(args.video_dir) if f.endswith('.mp4')]
    
    if not video_files:
        print(f"No MP4 videos found in {args.video_dir}")
        sys.exit(1)
    
    video_paths = [os.path.join(args.video_dir, f) for f in video_files]
    print(f"Found {len(video_paths)} videos to publish")
    
    # Publish to YouTube
    if args.youtube:
        print("\nPublishing to YouTube...")
        
        if not os.path.exists(args.youtube_secrets):
            print(f"Error: YouTube credentials not found: {args.youtube_secrets}")
            print("Please provide OAuth2 credentials JSON file")
            sys.exit(1)
        
        uploader = YouTubeUploader(args.youtube_secrets)
        video_ids = uploader.upload_batch(
            video_paths,
            title_prefix=args.title_prefix,
            description=args.description,
            tags=args.tags.split(',') if args.tags else None,
            privacy_status=args.privacy
        )
        
        print(f"\n✓ Uploaded {len(video_ids)} videos to YouTube")
    
    # Prepare for TikTok
    if args.tiktok:
        print("\nPreparing videos for TikTok...")
        uploader = TikTokUploader()
        uploader.authenticate()
        
        print("\nVideos ready for TikTok upload:")
        for path in video_paths:
            print(f"  - {path}")
        
        print("\n" + uploader.get_upload_instructions())


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description='NoFace - AI Motivational Video Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 3 videos
  python cli.py generate -n 3
  
  # Generate videos with custom settings
  python cli.py generate -n 5 --width 1080 --height 1920 --fps 30
  
  # Publish videos to YouTube
  python cli.py publish --youtube --privacy public
  
  # Prepare videos for TikTok
  python cli.py publish --tiktok
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate motivational videos')
    gen_parser.add_argument('-n', '--num-videos', type=int, default=1,
                           help='Number of videos to generate (default: 1)')
    gen_parser.add_argument('-q', '--quotes-file', default='quotes.txt',
                           help='File containing motivational quotes (default: quotes.txt)')
    gen_parser.add_argument('-o', '--output-dir', default='output',
                           help='Output directory for videos (default: output)')
    gen_parser.add_argument('--width', type=int, default=1080,
                           help='Video width in pixels (default: 1080)')
    gen_parser.add_argument('--height', type=int, default=1920,
                           help='Video height in pixels (default: 1920)')
    gen_parser.add_argument('--fps', type=int, default=30,
                           help='Frames per second (default: 30)')
    gen_parser.add_argument('--duration', type=int, default=15,
                           help='Maximum video duration in seconds (default: 15)')
    gen_parser.add_argument('--color1', default='#1a1a2e',
                           help='First gradient color (default: #1a1a2e)')
    gen_parser.add_argument('--color2', default='#16213e',
                           help='Second gradient color (default: #16213e)')
    
    # Publish command
    pub_parser = subparsers.add_parser('publish', help='Publish videos to platforms')
    pub_parser.add_argument('-d', '--video-dir', default='output',
                           help='Directory containing videos to publish (default: output)')
    pub_parser.add_argument('--youtube', action='store_true',
                           help='Publish to YouTube')
    pub_parser.add_argument('--tiktok', action='store_true',
                           help='Prepare for TikTok upload')
    pub_parser.add_argument('--youtube-secrets', default='client_secrets.json',
                           help='YouTube OAuth2 secrets file (default: client_secrets.json)')
    pub_parser.add_argument('--privacy', choices=['public', 'private', 'unlisted'],
                           default='private',
                           help='YouTube privacy setting (default: private)')
    pub_parser.add_argument('--title-prefix', default='Motivational Video',
                           help='Prefix for video titles (default: Motivational Video)')
    pub_parser.add_argument('--description', default='Daily motivation to inspire your day.',
                           help='Video description')
    pub_parser.add_argument('--tags', default='motivation,inspiration,quotes',
                           help='Comma-separated tags')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'generate':
        generate_command(args)
    elif args.command == 'publish':
        if not args.youtube and not args.tiktok:
            print("Error: Please specify at least one platform (--youtube or --tiktok)")
            sys.exit(1)
        publish_command(args)


if __name__ == '__main__':
    main()
