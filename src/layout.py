from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from pathlib import Path
from typing import List
from .story import Chapter

class PDFGenerator:
    def __init__(self):
        self.width, self.height = A4

    def generate(self, chapters: List[Chapter], output_path: str):
        """Generates the photo book PDF."""
        c = canvas.Canvas(output_path, pagesize=A4)
        c.setTitle("My Photo Book")

        # Title Page
        self._draw_title_page(c, "My Visual Story")
        
        for chapter in chapters:
            self._draw_chapter_title(c, chapter.title)
            
            # Simple grid layout: 2 images per page
            images = chapter.images
            for i in range(0, len(images), 2):
                batch = images[i:i+2]
                self._draw_photo_page(c, batch)
        
        c.save()
        print(f"PDF saved to {output_path}")

    def _draw_title_page(self, c: canvas.Canvas, title: str):
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(self.width / 2, self.height / 2, title)
        c.showPage()

    def _draw_chapter_title(self, c: canvas.Canvas, title: str):
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(self.width / 2, self.height / 2, title)
        c.showPage()

    def _draw_photo_page(self, c: canvas.Canvas, images):
        # Layout config
        margin = 50
        avail_width = self.width - (2 * margin)
        avail_height = (self.height - (3 * margin)) / 2  # 2 slots
        
        y_positions = [self.height - margin - avail_height, margin]
        
        for idx, img_meta in enumerate(images):
            try:
                img_path = str(img_meta.filename)
                # Load image
                # In real app, we need to resize/preserve aspect ratio
                # Draw simple rectangle frame
                y = y_positions[idx]
                
                # Check aspect ratio to fit in box
                img_obj = ImageReader(img_path)
                iw, ih = img_obj.getSize()
                aspect = iw / ih
                
                # Fit to width
                w = avail_width
                h = w / aspect
                
                # If too tall, fit to height
                if h > avail_height:
                    h = avail_height
                    w = h * aspect
                
                # Center
                x_offset = margin + (avail_width - w) / 2
                y_offset = y + (avail_height - h) / 2
                
                c.drawImage(img_obj, x_offset, y_offset, width=w, height=h)
                
            except Exception as e:
                print(f"Failed to draw image {img_meta.filename}: {e}")
                
        c.showPage()
