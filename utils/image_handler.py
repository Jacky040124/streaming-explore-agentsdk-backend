"""
Image handler utility for processing and saving generated images.
Handles image URLs, base64 data, and local file storage.
"""

import base64
import os
from pathlib import Path
from typing import Optional, Tuple
import urllib.request
from datetime import datetime


class ImageHandler:
    """Handles saving and processing of generated images."""
    
    def __init__(self, storage_dir: str = "outputs/images"):
        """
        Initialize image handler with storage directory.
        
        Args:
            storage_dir: Directory to store image files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def save_image_from_response(
        self, 
        image_data: str, 
        workflow_id: str,
        image_format: str = "png"
    ) -> Tuple[str, str]:
        """
        Save image from agent response (URL or base64).
        
        Args:
            image_data: The image data from ImageGenerationTool (URL or base64)
            workflow_id: Workflow ID for naming
            image_format: Image format (png, jpeg, webp)
            
        Returns:
            Tuple of (saved_file_path, reference_path_for_markdown)
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"image_{workflow_id[:8]}_{timestamp}.{image_format}"
        file_path = self.storage_dir / filename
        
        try:
            if image_data.startswith(('http://', 'https://')):
                # Download from URL
                self._download_image(image_data, file_path)
            elif image_data.startswith('data:image'):
                # Handle base64 data URL
                self._save_base64_image(image_data, file_path)
            elif ';base64,' in image_data:
                # Handle base64 without data URL prefix
                self._save_base64_image(f"data:image/{image_format};base64,{image_data}", file_path)
            else:
                # Assume it's raw base64
                self._save_raw_base64(image_data, file_path)
                
            # Return both absolute path and relative path for markdown
            relative_path = f"images/{filename}"
            return str(file_path), relative_path
            
        except Exception as e:
            print(f"Failed to save image: {e}")
            # Return empty paths if save fails
            return "", ""
    
    def _download_image(self, url: str, file_path: Path) -> None:
        """Download image from URL."""
        urllib.request.urlretrieve(url, file_path)
    
    def _save_base64_image(self, data_url: str, file_path: Path) -> None:
        """Save base64 data URL image."""
        # Extract base64 data from data URL
        header, data = data_url.split(',', 1)
        image_data = base64.b64decode(data)
        file_path.write_bytes(image_data)
    
    def _save_raw_base64(self, base64_str: str, file_path: Path) -> None:
        """Save raw base64 string as image."""
        image_data = base64.b64decode(base64_str)
        file_path.write_bytes(image_data)
    
    def get_image_path(self, filename: str) -> Optional[Path]:
        """Get full path for an image filename."""
        path = self.storage_dir / filename
        return path if path.exists() else None