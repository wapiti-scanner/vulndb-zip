import requests
import zipfile
import os
import shutil

# GitHub repository details
owner = "bitnami"
repo = "vulndb"
branch = "main"
directories = ["data/apache", "data/php"]

# Local paths
local_dir = "vulndb_files"

# GitHub API endpoint to get the repository contents
api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/"

def download_file(url, local_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(local_path, 'wb') as file:
        file.write(response.content)

def download_directory(directory):
    url = f"{api_url}{directory}?ref={branch}"
    response = requests.get(url, headers={"Accept": "application/vnd.github+json"})
    response.raise_for_status()
    items = response.json()
    
    for item in items:
        if item['type'] == 'file':
            file_url = item['download_url']
            file_path = os.path.join(local_dir, directory, item['name'])
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            download_file(file_url, file_path)
        elif item['type'] == 'dir':
            download_directory(os.path.join(directory, item['name']))

def create_zip(directory, zip_filename):
    shutil.make_archive(zip_filename.replace('.zip', ''), 'zip', directory)

if __name__ == "__main__":
    if os.path.exists(local_dir):
        shutil.rmtree(local_dir)
    
    os.makedirs(local_dir, exist_ok=True)

    for directory in directories:
        download_directory(directory)
        zip_filename = os.path.join(local_dir, f"{os.path.basename(directory)}.zip")
        create_zip(os.path.join(local_dir, directory), zip_filename)
        print(f"Created {zip_filename}")

