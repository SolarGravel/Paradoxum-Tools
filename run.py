import subprocess
import os

path: str = os.path.abspath("Title.py")

subprocess.run(f"streamlit run {path}")
