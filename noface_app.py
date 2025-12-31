"""
Main desktop application for NoFace - AI Motivational Video Generator.
"""
import os
import sys
import shutil
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import configparser
import random
import threading
from pathlib import Path

from video_generator import VideoGenerator
from youtube_uploader import YouTubeUploader
from tiktok_uploader import TikTokUploader


class NoFaceApp:
    """Main desktop application for generating and publishing motivational videos."""
    
    def __init__(self, root):
        """Initialize the application."""
        self.root = root
        self.root.title("NoFace - AI Motivational Video Generator")
        self.root.geometry("900x700")
        
        # Load configuration
        self.config = configparser.ConfigParser()
        self.load_config()
        
        # Initialize components
        self.video_generator = None
        self.youtube_uploader = None
        self.tiktok_uploader = None
        
        # Setup UI
        self.setup_ui()
        
    def load_config(self):
        """Load configuration from file."""
        config_file = 'config.ini'
        if not os.path.exists(config_file):
            # Try example config
            config_file = 'config.example.ini'
        
        if os.path.exists(config_file):
            self.config.read(config_file)
        else:
            # Set defaults
            self.config['VIDEO'] = {
                'width': '1080',
                'height': '1920',
                'fps': '30',
                'duration': '15',
                'output_dir': 'output'
            }
            self.config['CONTENT'] = {
                'quotes_file': 'quotes.txt',
                'background_type': 'gradient',
                'background_color1': '#1a1a2e',
                'background_color2': '#16213e'
            }
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_generate_tab(notebook)
        self.create_publish_tab(notebook)
        self.create_settings_tab(notebook)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_generate_tab(self, notebook):
        """Create the video generation tab."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Generate Videos")
        
        # Quotes section
        quotes_frame = ttk.LabelFrame(frame, text="Motivational Quotes", padding=10)
        quotes_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(quotes_frame, text="Enter quotes (one per line):").pack(anchor=tk.W)
        
        self.quotes_text = scrolledtext.ScrolledText(quotes_frame, height=10, width=70)
        self.quotes_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Load default quotes
        self.load_quotes()
        
        button_frame = ttk.Frame(quotes_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Load from File", command=self.load_quotes_from_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=lambda: self.quotes_text.delete('1.0', tk.END)).pack(side=tk.LEFT, padx=5)
        
        # Video settings
        settings_frame = ttk.LabelFrame(frame, text="Video Settings", padding=10)
        settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(settings_frame, text="Number of videos to generate:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.num_videos_var = tk.IntVar(value=1)
        ttk.Spinbox(settings_frame, from_=1, to=100, textvariable=self.num_videos_var, width=10).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(settings_frame, text="Output directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_dir_var = tk.StringVar(value=self.config.get('VIDEO', 'output_dir', fallback='output'))
        ttk.Entry(settings_frame, textvariable=self.output_dir_var, width=40).grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Button(settings_frame, text="Browse", command=self.browse_output_dir).grid(row=1, column=2, padx=5)
        
        # Generate button
        generate_frame = ttk.Frame(frame)
        generate_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.generate_btn = ttk.Button(generate_frame, text="Generate Videos", command=self.generate_videos)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(generate_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Log
        log_frame = ttk.LabelFrame(frame, text="Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=70)
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def create_publish_tab(self, notebook):
        """Create the publishing tab."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Publish Videos")
        
        # Video selection
        video_frame = ttk.LabelFrame(frame, text="Videos to Publish", padding=10)
        video_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(video_frame, text="Select directory containing videos:").pack(anchor=tk.W)
        
        dir_frame = ttk.Frame(video_frame)
        dir_frame.pack(fill=tk.X, pady=5)
        
        self.publish_dir_var = tk.StringVar(value=self.config.get('VIDEO', 'output_dir', fallback='output'))
        ttk.Entry(dir_frame, textvariable=self.publish_dir_var, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(dir_frame, text="Browse", command=self.browse_publish_dir).pack(side=tk.LEFT, padx=5)
        ttk.Button(dir_frame, text="Refresh", command=self.refresh_video_list).pack(side=tk.LEFT, padx=5)
        
        # Video list
        self.video_listbox = tk.Listbox(video_frame, height=8, selectmode=tk.MULTIPLE)
        self.video_listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(video_frame, orient=tk.VERTICAL, command=self.video_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.video_listbox.config(yscrollcommand=scrollbar.set)
        
        # Publishing options
        options_frame = ttk.LabelFrame(frame, text="Publishing Options", padding=10)
        options_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.publish_youtube_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Publish to YouTube", variable=self.publish_youtube_var).pack(anchor=tk.W)
        
        self.publish_tiktok_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="Prepare for TikTok", variable=self.publish_tiktok_var).pack(anchor=tk.W)
        
        ttk.Label(options_frame, text="Privacy:").pack(anchor=tk.W, pady=(10, 0))
        self.privacy_var = tk.StringVar(value='private')
        privacy_frame = ttk.Frame(options_frame)
        privacy_frame.pack(anchor=tk.W)
        ttk.Radiobutton(privacy_frame, text="Private", variable=self.privacy_var, value='private').pack(side=tk.LEFT)
        ttk.Radiobutton(privacy_frame, text="Unlisted", variable=self.privacy_var, value='unlisted').pack(side=tk.LEFT)
        ttk.Radiobutton(privacy_frame, text="Public", variable=self.privacy_var, value='public').pack(side=tk.LEFT)
        
        # Publish button
        publish_btn_frame = ttk.Frame(frame)
        publish_btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.publish_btn = ttk.Button(publish_btn_frame, text="Publish Selected Videos", command=self.publish_videos)
        self.publish_btn.pack(side=tk.LEFT, padx=5)
        
        # Publish log
        publish_log_frame = ttk.LabelFrame(frame, text="Publishing Log", padding=10)
        publish_log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.publish_log_text = scrolledtext.ScrolledText(publish_log_frame, height=6, width=70)
        self.publish_log_text.pack(fill=tk.BOTH, expand=True)
    
    def create_settings_tab(self, notebook):
        """Create the settings tab."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Settings")
        
        # Video settings
        video_settings_frame = ttk.LabelFrame(frame, text="Video Settings", padding=10)
        video_settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(video_settings_frame, text="Width:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.width_var = tk.IntVar(value=int(self.config.get('VIDEO', 'width', fallback='1080')))
        ttk.Entry(video_settings_frame, textvariable=self.width_var, width=15).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(video_settings_frame, text="Height:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.height_var = tk.IntVar(value=int(self.config.get('VIDEO', 'height', fallback='1920')))
        ttk.Entry(video_settings_frame, textvariable=self.height_var, width=15).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(video_settings_frame, text="FPS:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.fps_var = tk.IntVar(value=int(self.config.get('VIDEO', 'fps', fallback='30')))
        ttk.Entry(video_settings_frame, textvariable=self.fps_var, width=15).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(video_settings_frame, text="Max Duration (seconds):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.duration_var = tk.IntVar(value=int(self.config.get('VIDEO', 'duration', fallback='15')))
        ttk.Entry(video_settings_frame, textvariable=self.duration_var, width=15).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Background settings
        bg_settings_frame = ttk.LabelFrame(frame, text="Background Settings", padding=10)
        bg_settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(bg_settings_frame, text="Color 1 (hex):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.color1_var = tk.StringVar(value=self.config.get('CONTENT', 'background_color1', fallback='#1a1a2e'))
        ttk.Entry(bg_settings_frame, textvariable=self.color1_var, width=15).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(bg_settings_frame, text="Color 2 (hex):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.color2_var = tk.StringVar(value=self.config.get('CONTENT', 'background_color2', fallback='#16213e'))
        ttk.Entry(bg_settings_frame, textvariable=self.color2_var, width=15).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # API settings
        api_settings_frame = ttk.LabelFrame(frame, text="API Configuration", padding=10)
        api_settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(api_settings_frame, text="YouTube OAuth2 JSON file:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Button(api_settings_frame, text="Select File", command=self.select_youtube_credentials).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(api_settings_frame, text="For TikTok API access, visit:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Label(api_settings_frame, text="https://developers.tiktok.com/", foreground="blue").grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Save settings button
        ttk.Button(frame, text="Save Settings", command=self.save_settings).pack(pady=10)
    
    def load_quotes(self):
        """Load quotes from file."""
        quotes_file = self.config.get('CONTENT', 'quotes_file', fallback='quotes.txt')
        if os.path.exists(quotes_file):
            with open(quotes_file, 'r', encoding='utf-8') as f:
                quotes = f.read()
                self.quotes_text.delete('1.0', tk.END)
                self.quotes_text.insert('1.0', quotes)
    
    def load_quotes_from_file(self):
        """Load quotes from a user-selected file."""
        filename = filedialog.askopenfilename(
            title="Select Quotes File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                quotes = f.read()
                self.quotes_text.delete('1.0', tk.END)
                self.quotes_text.insert('1.0', quotes)
    
    def browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
    
    def browse_publish_dir(self):
        """Browse for publishing directory."""
        directory = filedialog.askdirectory(title="Select Video Directory")
        if directory:
            self.publish_dir_var.set(directory)
            self.refresh_video_list()
    
    def refresh_video_list(self):
        """Refresh the list of videos available for publishing."""
        self.video_listbox.delete(0, tk.END)
        directory = self.publish_dir_var.get()
        
        if os.path.exists(directory):
            files = [f for f in os.listdir(directory) if f.endswith('.mp4')]
            for file in sorted(files):
                self.video_listbox.insert(tk.END, file)
    
    def select_youtube_credentials(self):
        """Select YouTube OAuth2 credentials file."""
        filename = filedialog.askopenfilename(
            title="Select YouTube Client Secrets JSON",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            # Copy to expected location
            shutil.copy(filename, 'client_secrets.json')
            messagebox.showinfo("Success", "YouTube credentials file configured!")
    
    def save_settings(self):
        """Save current settings to config file."""
        if 'VIDEO' not in self.config:
            self.config['VIDEO'] = {}
        if 'CONTENT' not in self.config:
            self.config['CONTENT'] = {}
        
        self.config['VIDEO']['width'] = str(self.width_var.get())
        self.config['VIDEO']['height'] = str(self.height_var.get())
        self.config['VIDEO']['fps'] = str(self.fps_var.get())
        self.config['VIDEO']['duration'] = str(self.duration_var.get())
        self.config['VIDEO']['output_dir'] = self.output_dir_var.get()
        
        self.config['CONTENT']['background_color1'] = self.color1_var.get()
        self.config['CONTENT']['background_color2'] = self.color2_var.get()
        
        with open('config.ini', 'w') as f:
            self.config.write(f)
        
        messagebox.showinfo("Success", "Settings saved!")
    
    def log(self, message, log_widget=None):
        """Add message to log."""
        if log_widget is None:
            log_widget = self.log_text
        
        log_widget.insert(tk.END, f"{message}\n")
        log_widget.see(tk.END)
        self.root.update()
    
    def generate_videos(self):
        """Generate motivational videos."""
        # Get quotes
        quotes_text = self.quotes_text.get('1.0', tk.END).strip()
        if not quotes_text:
            messagebox.showerror("Error", "Please enter at least one quote!")
            return
        
        quotes = [q.strip() for q in quotes_text.split('\n') if q.strip()]
        
        # Get number of videos to generate
        num_videos = self.num_videos_var.get()
        
        if num_videos > len(quotes):
            # Select random quotes with repetition if needed
            selected_quotes = [random.choice(quotes) for _ in range(num_videos)]
        else:
            # Select random subset
            selected_quotes = random.sample(quotes, num_videos)
        
        # Clear log
        self.log_text.delete('1.0', tk.END)
        
        # Run generation in separate thread
        thread = threading.Thread(target=self._generate_videos_thread, args=(selected_quotes,))
        thread.daemon = True
        thread.start()
    
    def _generate_videos_thread(self, quotes):
        """Thread function for generating videos."""
        try:
            self.generate_btn.config(state=tk.DISABLED)
            self.status_var.set("Generating videos...")
            
            # Initialize video generator
            self.video_generator = VideoGenerator(
                width=self.width_var.get(),
                height=self.height_var.get(),
                fps=self.fps_var.get(),
                duration=self.duration_var.get()
            )
            
            output_dir = self.output_dir_var.get()
            self.log(f"Output directory: {output_dir}")
            self.log(f"Generating {len(quotes)} videos...")
            
            # Generate videos
            video_paths = self.video_generator.create_batch_videos(
                quotes,
                output_dir,
                self.color1_var.get(),
                self.color2_var.get()
            )
            
            self.progress_var.set(100)
            self.log(f"\n✓ Successfully generated {len(video_paths)} videos!")
            self.log(f"Videos saved to: {output_dir}")
            self.status_var.set("Generation complete!")
            
            messagebox.showinfo("Success", f"Generated {len(video_paths)} videos!")
            
        except Exception as e:
            self.log(f"\n✗ Error: {str(e)}")
            self.status_var.set("Error during generation")
            messagebox.showerror("Error", f"Failed to generate videos: {str(e)}")
        
        finally:
            self.generate_btn.config(state=tk.NORMAL)
            self.progress_var.set(0)
    
    def publish_videos(self):
        """Publish selected videos to platforms."""
        # Get selected videos
        selected_indices = self.video_listbox.curselection()
        if not selected_indices:
            messagebox.showerror("Error", "Please select at least one video!")
            return
        
        directory = self.publish_dir_var.get()
        video_files = [self.video_listbox.get(i) for i in selected_indices]
        video_paths = [os.path.join(directory, f) for f in video_files]
        
        # Clear log
        self.publish_log_text.delete('1.0', tk.END)
        
        # Run publishing in separate thread
        thread = threading.Thread(target=self._publish_videos_thread, args=(video_paths,))
        thread.daemon = True
        thread.start()
    
    def _publish_videos_thread(self, video_paths):
        """Thread function for publishing videos."""
        try:
            self.publish_btn.config(state=tk.DISABLED)
            self.status_var.set("Publishing videos...")
            
            # YouTube
            if self.publish_youtube_var.get():
                self.log("Publishing to YouTube...", self.publish_log_text)
                
                try:
                    if not os.path.exists('client_secrets.json'):
                        raise FileNotFoundError("YouTube credentials not configured. Please add client_secrets.json file.")
                    
                    self.youtube_uploader = YouTubeUploader('client_secrets.json')
                    video_ids = self.youtube_uploader.upload_batch(
                        video_paths,
                        title_prefix="Motivational Video",
                        description="Daily motivation to inspire your day. #motivation #inspiration",
                        tags=['motivation', 'inspiration', 'quotes', 'success'],
                        privacy_status=self.privacy_var.get()
                    )
                    
                    self.log(f"✓ Uploaded {len(video_ids)} videos to YouTube", self.publish_log_text)
                    
                except FileNotFoundError as e:
                    self.log(f"⚠ YouTube: {str(e)}", self.publish_log_text)
                    self.log("  Configure YouTube credentials in Settings tab", self.publish_log_text)
                except Exception as e:
                    self.log(f"✗ YouTube error: {str(e)}", self.publish_log_text)
            
            # TikTok
            if self.publish_tiktok_var.get():
                self.log("\nPreparing for TikTok...", self.publish_log_text)
                
                self.tiktok_uploader = TikTokUploader()
                self.tiktok_uploader.authenticate()
                
                for video_path in video_paths:
                    self.log(f"  Video ready: {video_path}", self.publish_log_text)
                
                self.log("\nTikTok Manual Upload Instructions:", self.publish_log_text)
                self.log(self.tiktok_uploader.get_upload_instructions(), self.publish_log_text)
            
            self.status_var.set("Publishing complete!")
            
        except Exception as e:
            self.log(f"\n✗ Error: {str(e)}", self.publish_log_text)
            self.status_var.set("Error during publishing")
            messagebox.showerror("Error", f"Failed to publish videos: {str(e)}")
        
        finally:
            self.publish_btn.config(state=tk.NORMAL)


def main():
    """Main entry point."""
    root = tk.Tk()
    app = NoFaceApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
