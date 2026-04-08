from typing import List, Dict
from dataclasses import dataclass
from pathlib import Path
from .metadata import MetadataExtractor, ImageMetadata
from .clustering import ImageClusterer

@dataclass
class Chapter:
    title: str
    images: List[ImageMetadata]

class StoryGenerator:
    def __init__(self):
        self.metadata_extractor = MetadataExtractor()
        self.clusterer = ImageClusterer()

    def create_story(self, image_paths: List[Path]) -> List[Chapter]:
        """
        Organizes a list of images into a chronological story with chapters.
        """
        # 1. Extract Metadata
        print("Extracting metadata...")
        meta_list = []
        for p in image_paths:
            m = self.metadata_extractor.extract(p)
            meta_list.append(m)
            
        print(f"Extracted metadata for {len(meta_list)} images.")

        # 2. Sort by Time
        meta_list.sort(key=lambda x: x.timestamp)

        # 3. Create Time-based Clusters (Events)
        events = self.clusterer.cluster_by_time(meta_list, gap_hours=6.0)
        
        # 4. Convert Events to Chapters
        chapters = []
        for i, event in enumerate(events):
            if not event:
                continue
            
            # Simple titling strategy based on date
            start_time = event[0].timestamp
            title = start_time.strftime("%B %d, %Y")
            
            # Add location info if available (placeholder logic)
            # if event[0].gps_coords:
            #     title += " - Location" 

            chapters.append(Chapter(title=title, images=event))
            
        return chapters
