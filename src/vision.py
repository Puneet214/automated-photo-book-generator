from typing import List, Dict, Any
from pathlib import Path
try:
    import torch
    from PIL import Image
    from transformers import CLIPProcessor, CLIPModel
    _VISION_AVAILABLE = True
except ImportError:
    _VISION_AVAILABLE = False
    print("Warning: Torch/Transformers not found. Vision features will be disabled.")

class FeatureExtractor:
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        """Initializes the CLIP model."""
        if _VISION_AVAILABLE:
            print(f"Loading CLIP model: {model_name}...")
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model = CLIPModel.from_pretrained(model_name).to(self.device)
            self.processor = CLIPProcessor.from_pretrained(model_name)
            print("Model loaded successfully.")
        else:
            self.model = None

    def get_embedding(self, image_path: Path):
        """Computes the visual embedding for a single image."""
        if not _VISION_AVAILABLE:
            return None
            
        try:
            image = Image.open(image_path)
            inputs = self.processor(images=image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                image_features = self.model.get_image_features(**inputs)
            
            # Normalize the features
            image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
            return image_features.cpu().numpy()
            
        except Exception as e:
            print(f"Error computing embedding for {image_path}: {e}")
            return None

    def batch_process(self, image_paths: List[Path]) -> Dict[Path, Any]:
        """Computes embeddings for a batch of images."""
        embeddings = {}
        if not _VISION_AVAILABLE:
            return embeddings
            
        # For prototype simplicity, we loop. Batch processing via processor is possible but requires collating.
        for path in image_paths:
            emb = self.get_embedding(path)
            if emb is not None:
                embeddings[path] = emb
        return embeddings
