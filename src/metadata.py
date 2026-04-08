from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import exifread
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

@dataclass
class ImageMetadata:
    filename: Path
    timestamp: datetime
    gps_coords: Optional[Tuple[float, float]] = None
    camera_model: Optional[str] = None
    width: int = 0
    height: int = 0

class MetadataExtractor:
    def __init__(self):
        pass

    def extract(self, image_path: Path) -> ImageMetadata:
        """Extracts metadata from an image file."""
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f, details=False)
            
            # Extract timestamp
            timestamp = self._get_timestamp(tags)
            
            # Extract GPS
            gps_coords = self._get_gps_coords(tags)
            
            # Extract Camera Model
            camera_model = str(tags.get('Image Model', 'Unknown'))
            
            # Get dimensions
            with Image.open(image_path) as img:
                width, height = img.size

            if not timestamp:
                # Fallback to file modification time if EXIF is missing
                timestamp = datetime.fromtimestamp(image_path.stat().st_mtime)

            return ImageMetadata(
                filename=image_path,
                timestamp=timestamp,
                gps_coords=gps_coords,
                camera_model=camera_model,
                width=width,
                height=height
            )

        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            # Minimal fallback
            return ImageMetadata(
                filename=image_path,
                timestamp=datetime.fromtimestamp(image_path.stat().st_mtime),
                width=0,
                height=0
            )

    def _get_timestamp(self, tags: Dict) -> Optional[datetime]:
        """Parses EXIF timestamp."""
        date_str = str(tags.get('EXIF DateTimeOriginal') or tags.get('Image DateTime'))
        if date_str and date_str != 'None':
            try:
                return datetime.strptime(str(date_str), '%Y:%m:%d %H:%M:%S')
            except ValueError:
                pass
        return None

    def _get_gps_coords(self, tags: Dict) -> Optional[Tuple[float, float]]:
        """Extracts latitude and longitude if available."""
        # This is a simplified implementation. 
        # A robust one needs to handle degrees/minutes/seconds conversion.
        # For prototype, we will return None or a placeholder if complex parsing needed
        # But let's try a basic conversion if tags exist
        
        if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
            try:
                lat = self._convert_to_degrees(tags['GPS GPSLatitude'])
                lon = self._convert_to_degrees(tags['GPS GPSLongitude'])
                
                if tags.get('GPS GPSLatitudeRef', 'N').values == 'S':
                    lat = -lat
                if tags.get('GPS GPSLongitudeRef', 'E').values == 'W':
                    lon = -lon
                    
                return (lat, lon)
            except:
                return None
        return None

    def _convert_to_degrees(self, value):
        """Helper to convert GPS rational values to degrees."""
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)
        return d + (m / 60.0) + (s / 3600.0)
