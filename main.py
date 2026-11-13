import os
import sys
import shutil
from pathlib import Path
import hashlib

def main():
    # Determine output directory
    output_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if output_dir_env:
        output_dir = Path(output_dir_env)
    else:
        output_dir = Path("/output")
        
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Source winner.png path relative to this script
    script_dir = Path(__file__).resolve().parent
    src_path = script_dir / "winner.png"
    dest_path = output_dir / "entry.png"
    
    if not src_path.exists():
        print(f"Error: Source image not found at {src_path}", file=sys.stderr)
        sys.exit(1)
        
    # Read source file and compute sha256
    with open(src_path, "rb") as f:
        src_data = f.read()
    src_sha256 = hashlib.sha256(src_data).hexdigest()
    src_size = len(src_data)
    
    # Gate check: file size must not exceed 1048576 bytes (1 MiB)
    MAX_SIZE = 1048576
    if src_size > MAX_SIZE:
        print(f"Error: Source file size {src_size} exceeds maximum allowed {MAX_SIZE}", file=sys.stderr)
        sys.exit(1)
    
    # Copy file using shutil.copy2
    shutil.copy2(src_path, dest_path)
    
    # Verify destination file
    if not dest_path.exists():
        print(f"Error: Destination file not created at {dest_path}", file=sys.stderr)
        sys.exit(1)
        
    with open(dest_path, "rb") as f:
        dest_data = f.read()
    dest_sha256 = hashlib.sha256(dest_data).hexdigest()
    dest_size = len(dest_data)
    
    if src_sha256 != dest_sha256:
        print(f"Error: SHA256 mismatch! src={src_sha256}, dest={dest_sha256}", file=sys.stderr)
        sys.exit(1)
        
    print(f"Successfully copied entry.png. Size: {dest_size} bytes, SHA256: {dest_sha256}")

if __name__ == "__main__":
    main()
