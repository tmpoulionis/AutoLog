import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BACKEND = "transformers"  # or "claude"

# TransformersBackend settings
MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
LOAD_IN_4BIT = True
MAX_NEW_TOKENS = 1024
DEVICE_MAP = "auto"

# Storage settings
AUTOLOG_DIR  = Path(os.environ.get("AUTOLOG_DIR", Path.home() / ".autolog"))
PROJECTS_DIR = AUTOLOG_DIR / "projects"
CHROMA_DIR   = AUTOLOG_DIR / "chroma"

# Embedding settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
