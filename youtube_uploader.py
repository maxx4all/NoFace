"""
YouTube uploader module for publishing videos.
"""
import os
import pickle
from typing import Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class YouTubeUploader:
    """Handles video uploads to YouTube."""
    
    # Scopes required for uploading videos
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self, client_secrets_file: str = 'client_secrets.json'):
        """
        Initialize YouTube uploader.
        
        Args:
            client_secrets_file: Path to OAuth2 client secrets JSON file
        """
        self.client_secrets_file = client_secrets_file
        self.credentials = None
        self.youtube = None
        
    def authenticate(self):
        """
        Authenticate with YouTube API using OAuth2.
        """
        token_file = 'youtube_token.pickle'
        
        # Load credentials from file if available
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                self.credentials = pickle.load(token)
        
        # Refresh or get new credentials
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                if not os.path.exists(self.client_secrets_file):
                    raise FileNotFoundError(
                        f"Client secrets file not found: {self.client_secrets_file}\n"
                        "Please download OAuth2 credentials from Google Cloud Console."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file,
                    self.SCOPES
                )
                self.credentials = flow.run_local_server(port=8080)
            
            # Save credentials for future use
            with open(token_file, 'wb') as token:
                pickle.dump(self.credentials, token)
        
        # Build YouTube API client
        self.youtube = build('youtube', 'v3', credentials=self.credentials)
    
    def upload_video(
        self,
        video_path: str,
        title: str,
        description: str = '',
        tags: list = None,
        category_id: str = '22',  # People & Blogs
        privacy_status: str = 'private'
    ) -> Optional[str]:
        """
        Upload a video to YouTube.
        
        Args:
            video_path: Path to the video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID
            privacy_status: 'public', 'private', or 'unlisted'
            
        Returns:
            Video ID if successful, None otherwise
        """
        if not self.youtube:
            self.authenticate()
        
        if tags is None:
            tags = ['motivation', 'inspirational', 'quotes']
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Create media upload
        media = MediaFileUpload(
            video_path,
            chunksize=-1,
            resumable=True,
            mimetype='video/mp4'
        )
        
        try:
            # Execute upload request
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"Upload progress: {int(status.progress() * 100)}%")
            
            video_id = response['id']
            print(f"✓ Video uploaded successfully. Video ID: {video_id}")
            print(f"  URL: https://www.youtube.com/watch?v={video_id}")
            
            return video_id
            
        except Exception as e:
            print(f"✗ Error uploading video: {e}")
            return None
    
    def upload_batch(
        self,
        video_paths: list,
        title_prefix: str = 'Motivational Video',
        description: str = 'Daily motivation to inspire your day.',
        tags: list = None,
        privacy_status: str = 'private'
    ) -> list:
        """
        Upload multiple videos to YouTube.
        
        Args:
            video_paths: List of video file paths
            title_prefix: Prefix for video titles
            description: Video description
            tags: List of tags
            privacy_status: 'public', 'private', or 'unlisted'
            
        Returns:
            List of video IDs
        """
        if not self.youtube:
            self.authenticate()
        
        video_ids = []
        
        for i, video_path in enumerate(video_paths):
            title = f"{title_prefix} #{i+1}"
            print(f"\nUploading video {i+1}/{len(video_paths)}: {title}")
            
            video_id = self.upload_video(
                video_path,
                title,
                description,
                tags,
                privacy_status=privacy_status
            )
            
            if video_id:
                video_ids.append(video_id)
        
        return video_ids
