
import os
import time
import uuid
import json
import zlib
from pathlib import Path

# Directory setup
LOCAL_FS_PATH = "local_files/"
LOCAL_FS_PATH1 = "local_files1/"
S3_SIM_PATH = "s3_simulated/"
S3_METADATA_DB = "s3_metadata.json"

# Ensure dirs
os.makedirs(LOCAL_FS_PATH, exist_ok=True)
os.makedirs(S3_SIM_PATH, exist_ok=True)

# --------------------------
# Local FileSystem Behavior
# --------------------------

def Localfile(filename,content):
    full_path= os.path.join(LOCAL_FS_PATH1,filename)
    with open(full_path,'w') as f:
        f.write(content)
    return full_path
  

def write_to_local(filename, content):
    start = time.time()
    full_path = os.path.join(LOCAL_FS_PATH, filename)
    with open(full_path, 'w') as f:
        f.write(content)
    end = time.time()
    print(f"[LocalFS] Written in {end - start:.4f}s → {full_path}")
    return full_path

def read_from_local(filename):
    start = time.time()
    full_path = os.path.join(LOCAL_FS_PATH, filename)
    with open(full_path, 'r') as f:
        content = f.read()
    end = time.time()
    print(f"[LocalFS] Read in {end - start:.4f}s → {full_path}")
    return content

# --------------------------
# Simulated S3 Behavior
# --------------------------

def init_metadata():
    if not os.path.exists(S3_METADATA_DB):
        with open(S3_METADATA_DB, 'w') as f:
            json.dump({}, f)

def load_metadata():
    with open(S3_METADATA_DB, 'r') as f:
        return json.load(f)

def save_metadata(metadata):
    with open(S3_METADATA_DB, 'w') as f:
        json.dump(metadata, f, indent=2)

def erasure_code(content):
    # Simulate simple parity block
    parity = zlib.crc32(content.encode())
    return content, parity

'''
def s3simulation(key,content):
    
    object_id = str(uuid.uuid4())
    object_path = os.path.join(S3_SIM_PATH, object_id)
    with open(object_path, 'w') as f:
        f.write(body)
'''   
    

def write_to_s3(key, content):
    start = time.time()
    object_id = str(uuid.uuid4())
    version_id = str(uuid.uuid4())

    body, parity = erasure_code(content)

    # Save object
    object_path = os.path.join(S3_SIM_PATH, object_id)
    with open(object_path, 'w') as f:
        f.write(body)

    # Load & update metadata
    meta = load_metadata()
    meta[key] = {
        "object_id": object_id,
        "version_id": version_id,
        "timestamp": time.time(),
        "parity": parity
    }
    save_metadata(meta)

    end = time.time()
    print(f"[S3] Object stored in {end - start:.4f}s with version {version_id}")
    return version_id

def read_from_s3(key):
    start = time.time()
    meta = load_metadata()
    if key not in meta:
        raise FileNotFoundError(f"{key} not found in S3 metadata")

    object_id = meta[key]["object_id"]
    path = os.path.join(S3_SIM_PATH, object_id)
    with open(path, 'r') as f:
        body = f.read()

    # Optional: Check parity
    parity_check = zlib.crc32(body.encode())
    if parity_check != meta[key]["parity"]:
        raise ValueError("Corrupted S3 object: parity mismatch")

    end = time.time()
    print(f"[S3] Read object in {end - start:.4f}s with version {meta[key]['version_id']}")
    return body




# --------------------------
# Test Demo
# --------------------------

def simulate_demo():
    init_metadata()

    print("\n-- Writing to Local File System --")
    write_to_local("report.txt", "Normal file system write performance test.")

    print("\n-- Reading from Local File System --")
    print(read_from_local("report.txt"))

    print("\n-- Writing to Simulated S3 --")
    write_to_s3("report.txt", "Simulated S3 object store write with versioning and parity.")

    print("\n-- Reading from Simulated S3 --")
    print(read_from_s3("report.txt"))

if __name__ == "__main__":
    simulate_demo()
