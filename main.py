import typer
from rich.console import Console
from rich.progress import track
from pathlib import Path
from src.story import StoryGenerator
from src.vision import FeatureExtractor
from src.ranking import ImageRanker
from src.layout import PDFGenerator

app = typer.Typer()
console = Console()

@app.command()
def main(
    input_dir: str = typer.Argument(..., help="Directory containing source images"),
    output_pdf: str = typer.Option("photobook.pdf", help="Output PDF filename"),
):
    """
    Automated Visual Storytelling and Photo Book Generation System.
    """
    console.print(f"[bold green]Starting Photobook Generation[/bold green]")
    input_path = Path(input_dir)
    if not input_path.exists():
        console.print(f"[bold red]Error: Input directory {input_dir} does not exist.[/bold red]")
        raise typer.Exit(code=1)

    # Gather images
    image_extensions = {".jpg", ".jpeg", ".png"}
    image_paths = [
        p for p in input_path.iterdir() 
        if p.suffix.lower() in image_extensions
    ]
    
    if not image_paths:
        console.print(f"[bold red]No images found in {input_dir}.[/bold red]")
        raise typer.Exit(code=1)
        
    console.print(f"Found {len(image_paths)} images.")

    # 1. Story Construction (Metadata + Clustering)
    console.print("[bold blue]Step 1: Analyzing Metadata and Storyline...[/bold blue]")
    story_gen = StoryGenerator()
    chapters = story_gen.create_story(image_paths)
    console.print(f"Created {len(chapters)} chapters.")

    # 2. Visual Analysis (Embeddings) - Just demonstrating usage
    console.print("[bold blue]Step 2: Computing Visual Features...[/bold blue]")
    extractor = FeatureExtractor()
    # embeddings = extractor.batch_process(image_paths) # Optional: Use for visual clustering
    console.print("Visual feature extractor initialized.")

    # 3. Visual Scoring (Ranking)
    console.print("[bold blue]Step 3: Scoring Images...[/bold blue]")
    ranker = ImageRanker()
    
    # Analyze images in chapters and maybe sort them?
    for chapter in chapters:
        console.print(f"Processing chapter: {chapter.title}")
        scored_images = []
        for img in chapter.images:
            score = ranker.get_score(img.filename)
            scored_images.append((score, img))
        
        # Sort by score descending? Or Keep chronological?
        # Let's clean up: remove very blurry images (< 10.0 score?)
        # For now, just sort best to worst for the layout to pick top ones?
        # Or keep chronological but maybe highlight best.
        # Let's Just keep chronological for the story, but we computed scores.
        # Maybe we filter out 0.0 scores (errors).
        chapter.images = [img for s, img in scored_images if s > 0.0]

    # 4. Layout Generation
    console.print("[bold blue]Step 4: Generating PDF...[/bold blue]")
    pdf_gen = PDFGenerator()
    pdf_gen.generate(chapters, output_pdf)
    
    console.print(f"[bold green]Success! Photobook saved to {output_pdf}[/bold green]")

if __name__ == "__main__":
    app()
