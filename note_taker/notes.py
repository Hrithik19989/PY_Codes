from pathlib import Path
from datetime import datetime
import os

NOTES_DIR = Path("notes")

def setup():
    """Create the notes folder if it doesn't exist."""
    NOTES_DIR.mkdir(exist_ok=True)