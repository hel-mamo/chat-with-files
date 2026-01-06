import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ===============================
# Project Paths
# ===============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
VECTOR_DB_PATH = os.path.join(DATA_DIR, "vectordb")

# Create directories automatically
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_PATH, exist_ok=True)


# ===============================
# OpenRouter API Configuration (for DeepSeek R1)
# ===============================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")


# ===============================
# Model Configuration
# ===============================

# LLM Model - DeepSeek R1 (free tier via OpenRouter)
OPENAI_MODEL = "deepseek/deepseek-r1-0528:free"
OPENAI_TEMPERATURE = 0

# Embeddings Model - Using OpenAI embeddings (still requires OpenAI-compatible endpoint)
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"  # or "text-embedding-3-large"


# ===============================
# Retrieval Settings
# ===============================

CHUNK_SIZE = 800
CHUNK_OVERLAP = 150
TOP_K = 4


# ===============================
# Supabase Configuration
# ===============================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("WARNING: Supabase credentials not found. Chat history will use local storage.")
