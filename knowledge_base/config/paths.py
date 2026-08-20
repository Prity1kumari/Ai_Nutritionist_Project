from pathlib import Path

# ===========================
# Dataset Location
# ===========================

OPENFOODFACTS_PATH = Path(
    r"C:\Users\prity\OneDrive\Desktop\Ai_Nutritionist_Project\dataset\raw\en.openfoodfacts.org.products.csv"
)

# ===========================
# Knowledge Base Root
# ===========================

KB_ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = KB_ROOT / "raw"
PROCESSED_DIR = KB_ROOT / "processed"
JSON_DIR = KB_ROOT / "json"
EMBEDDINGS_DIR = KB_ROOT / "embeddings"
VECTOR_STORE_DIR = KB_ROOT / "vector_store"