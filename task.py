import os
import sys
from src.cli import main

if __name__ == "__main__":
    # Default storage path
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    storage_path = os.path.join(data_dir, "tasks.json")
    
    main(storage_path)
