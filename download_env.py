import urllib.request
import zipfile
import os
import sys

def download_and_extract(url, extract_to, name):
    print(f"Downloading {name} from {url}...")
    zip_path = f"{name}.zip"
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
            out_file.write(response.read())
            
        print(f"Extracting {name}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            
        print(f"{name} setup complete.")
    except Exception as e:
        print(f"Error setting up {name}: {e}")
    finally:
        if os.path.exists(zip_path):
            os.remove(zip_path)

if __name__ == "__main__":
    env_dir = os.path.join(os.path.dirname(__file__), 'dev_env')
    os.makedirs(env_dir, exist_ok=True)
    
    go_url = "https://golang.google.cn/dl/go1.22.2.windows-amd64.zip"
    
    # Setup Go
    if not os.path.exists(os.path.join(env_dir, "go")):
        download_and_extract(go_url, env_dir, "Go")
    else:
        print("Go already exists.")

    print("Environment update complete!")
