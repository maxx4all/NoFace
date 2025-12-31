"""
Video generator module for creating motivational videos.
"""
import os
import random
import shutil
import tempfile
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    AudioFileClip,
    ImageClip,
    CompositeVideoClip,
    TextClip,
    concatenate_videoclips
)
from gtts import gTTS


class VideoGenerator:
    """Generates motivational videos with AI-powered content."""
    
    def __init__(self, width: int = 1080, height: int = 1920, fps: int = 30, duration: int = 15):
        """
        Initialize the video generator.
        
        Args:
            width: Video width in pixels
            height: Video height in pixels
            fps: Frames per second
            duration: Video duration in seconds
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.duration = duration
        
    def create_gradient_background(self, color1: str, color2: str) -> Image.Image:
        """
        Create a gradient background image.
        
        Args:
            color1: Start color in hex format (e.g., '#1a1a2e')
            color2: End color in hex format (e.g., '#16213e')
            
        Returns:
            PIL Image with gradient background
        """
        base = Image.new('RGB', (self.width, self.height), color1)
        top = Image.new('RGB', (self.width, self.height), color2)
        mask = Image.new('L', (self.width, self.height))
        mask_data = []
        
        for y in range(self.height):
            alpha = int(255 * (y / self.height))
            mask_data.extend([alpha] * self.width)
        
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return base
    
    def generate_speech(self, text: str, output_path: str) -> str:
        """
        Generate speech audio from text using gTTS.
        
        Args:
            text: Text to convert to speech
            output_path: Path to save the audio file
            
        Returns:
            Path to the generated audio file
        """
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_path)
        return output_path
    
    def wrap_text(self, text: str, max_width: int = 30) -> str:
        """
        Wrap text to fit within specified width.
        
        Args:
            text: Text to wrap
            max_width: Maximum characters per line
            
        Returns:
            Wrapped text with newlines
        """
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_width:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    def create_video(
        self,
        quote: str,
        output_path: str,
        bg_color1: str = '#1a1a2e',
        bg_color2: str = '#16213e'
    ) -> str:
        """
        Create a complete motivational video.
        
        Args:
            quote: Motivational quote text
            output_path: Path to save the video
            bg_color1: First gradient color
            bg_color2: Second gradient color
            
        Returns:
            Path to the generated video file
        """
        # Create temporary directory for intermediate files
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Generate background image
            bg_image = self.create_gradient_background(bg_color1, bg_color2)
            bg_path = os.path.join(temp_dir, 'background.png')
            bg_image.save(bg_path)
            
            # Generate speech
            audio_path = os.path.join(temp_dir, 'speech.mp3')
            self.generate_speech(quote, audio_path)
            
            # Load audio to get duration
            audio_clip = AudioFileClip(audio_path)
            video_duration = min(audio_clip.duration + 1, self.duration)  # Add 1 second padding
            
            # Create background video clip
            bg_clip = ImageClip(bg_path).set_duration(video_duration)
            
            # Wrap text for better display
            wrapped_quote = self.wrap_text(quote, max_width=35)
            
            # Create text clip
            txt_clip = TextClip(
                wrapped_quote,
                fontsize=70,
                color='white',
                font='Arial-Bold',
                method='caption',
                size=(self.width - 200, None),
                align='center'
            ).set_duration(video_duration).set_position('center')
            
            # Composite video
            video = CompositeVideoClip([bg_clip, txt_clip])
            video = video.set_audio(audio_clip)
            
            # Write video file
            video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=os.path.join(temp_dir, 'temp-audio.m4a'),
                remove_temp=True
            )
            
            # Clean up
            audio_clip.close()
            video.close()
            
            return output_path
            
        finally:
            # Clean up temporary files
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    def create_batch_videos(
        self,
        quotes: list,
        output_dir: str,
        bg_color1: str = '#1a1a2e',
        bg_color2: str = '#16213e'
    ) -> list:
        """
        Create multiple videos from a list of quotes.
        
        Args:
            quotes: List of motivational quotes
            output_dir: Directory to save videos
            bg_color1: First gradient color
            bg_color2: Second gradient color
            
        Returns:
            List of paths to generated videos
        """
        os.makedirs(output_dir, exist_ok=True)
        video_paths = []
        
        for i, quote in enumerate(quotes):
            output_path = os.path.join(output_dir, f'motivational_video_{i+1}.mp4')
            print(f"Generating video {i+1}/{len(quotes)}: {output_path}")
            
            try:
                self.create_video(quote, output_path, bg_color1, bg_color2)
                video_paths.append(output_path)
                print(f"✓ Video {i+1} completed")
            except Exception as e:
                print(f"✗ Error generating video {i+1}: {e}")
        
        return video_paths
