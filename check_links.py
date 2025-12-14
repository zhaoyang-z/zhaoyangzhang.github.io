import yaml
import requests
import os
from pathlib import Path
from urllib.parse import urlparse, quote

def is_url(string):
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except:
        return False

def is_academic_publisher_url(url):
    academic_domains = [
        'onlinelibrary.wiley.com',
        'sciencedirect.com',
        'springer.com',
        'jstor.org',
        'academic.oup.com'
    ]
    return any(domain in url.lower() for domain in academic_domains)

def check_local_file(filepath, base_path):
    full_path = Path(base_path) / filepath
    return full_path.exists()

def check_url(url):
    try:
        if is_academic_publisher_url(url):
            print(f"ℹ️ Academic publisher URL (requires authentication): {url}")
            return True
        
        encoded_url = quote(url, safe=':/?=&')
        response = requests.get(encoded_url, timeout=5, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def check_yaml_file(yaml_path, base_path):
    print(f"\nChecking {yaml_path}...")
    
    if not os.path.exists(yaml_path):
        print(f"❌ YAML file not found: {yaml_path}")
        return
    
    with open(yaml_path, 'r', encoding='utf-8') as file:
        try:
            data = yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"❌ Error parsing YAML file: {e}")
            return

    # Handle different YAML structures
    if isinstance(data, dict):
        if 'datasets' in data:
            items = data['datasets']
        elif 'other_writings' in data:
            items = data['other_writings']
        elif 'summaries' in data:
            items = data['summaries']
        else:
            items = data
    else:
        items = data

    for item in items:
        title = item.get('title', 'Untitled')
        
        # Check PDF
        if 'pdf' in item:
            path = item['pdf']
            if is_url(path):
                if not check_url(path):
                    print(f"❌ External PDF link broken: {path} (Paper: {title})")
            else:
                if not check_local_file(path, base_path):
                    print(f"❌ Local PDF missing: {path} (Paper: {title})")
        
        # Check appendix
        if 'appendix' in item:
            path = item['appendix']
            if is_url(path):
                if not check_url(path):
                    print(f"❌ External appendix link broken: {path} (Paper: {title})")
            else:
                if not check_local_file(path, base_path):
                    print(f"❌ Local appendix missing: {path} (Paper: {title})")
        
        # Check link
        if 'link' in item:
            path = item['link']
            if is_url(path):
                if not check_url(path):
                    print(f"❌ External link broken: {path} (Paper: {title})")
            else:
                if not check_local_file(path, base_path):
                    print(f"❌ Local link file missing: {path} (Paper: {title})")

def main():
    # Set base path for local file checks
    base_path = Path('.')  # Adjust this to your repository root path
    
    # List of YAML files to check
    yaml_files = [
        '_data/papers.yml',
        '_data/datasets.yml',
        '_data/other_writings.yml',
        '_data/summaries.yml'  # Added summaries.yml
    ]
    
    for yaml_file in yaml_files:
        check_yaml_file(yaml_file, base_path)

if __name__ == "__main__":
    main()