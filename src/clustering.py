from typing import List, Dict, Any
import numpy as np
from sklearn.cluster import KMeans
from datetime import timedelta
from .metadata import ImageMetadata

class ImageClusterer:
    def __init__(self):
        pass

    def cluster_by_time(self, metadata_list: List[ImageMetadata], gap_hours: float = 4.0) -> List[List[ImageMetadata]]:
        """
        Splits images into events based on time gaps.
        Images must be sorted by time before calling this.
        """
        if not metadata_list:
            return []

        # Ensure sorted
        sorted_meta = sorted(metadata_list, key=lambda x: x.timestamp)
        
        events = []
        current_event = [sorted_meta[0]]
        
        for i in range(1, len(sorted_meta)):
            prev = sorted_meta[i-1]
            curr = sorted_meta[i]
            
            diff = curr.timestamp - prev.timestamp
            if diff > timedelta(hours=gap_hours):
                events.append(current_event)
                current_event = []
            
            current_event.append(curr)
            
        if current_event:
            events.append(current_event)
            
        return events

    def cluster_visually(self, embeddings: Dict[Any, np.ndarray], n_clusters: int = 5) -> Dict[int, List[Any]]:
        """
        Clusters images based on their CLIP embeddings using K-Means.
        Returns a dict mapping cluster_id to list of image paths/IDs.
        """
        if not embeddings:
            return {}
            
        keys = list(embeddings.keys())
        matrix = np.vstack([embeddings[k] for k in keys])
        
        # Determine K if not provided (heuristic or fixed)
        k = min(n_clusters, len(keys))
        if k < 1:
            return {}
            
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(matrix)
        
        clusters = {}
        for i, label in enumerate(labels):
            label = int(label)
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(keys[i])
            
        return clusters
