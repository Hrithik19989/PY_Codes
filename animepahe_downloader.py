import os
import sys
import time
import requests
import json
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://animepahe.pw"

def get_headless_browser():
    options = Options()
    options.add_argument("--headless=new")  
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    
    driver = webdriver.Chrome(options=options)
    # Anti-bot detection fingerprint evasion bypass setup
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

def search_anime(driver, query):
    """Searches AnimePahe for the query title and extracts matching results."""
    print(f"\n🔍 Searching for '{query}' on AnimePahe...")
    search_url = f"{BASE_URL}/api?m=search&q={requests.utils.quote(query)}"
    
    driver.get(search_url)
    time.sleep(2)
    
    try:
        page_source = driver.find_element(By.TAG_NAME, "pre").text
        data = json.loads(page_source)
        return data.get('data', [])
    except Exception:
        try:
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            data = json.loads(soup.text)
            return data.get('data', [])
        except Exception:
            return []

def filter_audio_preference(anime_list, choice):
    """Filters results by language format based on user criteria."""
    filtered = []
    for anime in anime_list:
        title = anime.get('title', '').lower()
        is_dub = "(dub)" in title or "dubbed" in title
        
        if choice == "dub" and is_dub:
            filtered.append(anime)
        elif choice == "sub" and not is_dub:
            filtered.append(anime)
        elif choice == "all":
            filtered.append(anime)
    return filtered

def fetch_episode_links(driver, anime_session_id):
    """Fetches pagination and index of all episodes belonging to selected anime ID."""
    print("📦 Scraping episode manifest tables...")
    episodes = []
    page = 1
    
    while True:
        ep_api_url = f"{BASE_URL}/api?m=release&id={anime_session_id}&sort=episode_asc&page={page}"
        driver.get(ep_api_url)
        time.sleep(1.5)
        
        try:
            raw_text = driver.find_element(By.TAG_NAME, "pre").text
            res = json.loads(raw_text)
            current_page_data = res.get('data', [])
            if not current_page_data:
                break
            episodes.extend(current_page_data)
            
            if page >= res.get('last_page', 1):
                break
            page += 1
        except Exception:
            break
            
    return episodes

def get_download_url(driver, anime_session_id, episode_session_id, target_quality):
    """Finds download mirrors, extracts the underlying video files, and filters by resolution."""
    ep_page_url = f"{BASE_URL}/play/{anime_session_id}/{episode_session_id}"
    driver.get(ep_page_url)
    
    try:
        wait = WebDriverWait(driver, 10)
        download_menu = wait.until(EC.presence_of_element_located((By.ID, "download")))
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        drop_menu = soup.find('div', {'id': 'download'})
        links = drop_menu.find_all('a') if drop_menu else []
        
        matched_link = None
        fallback_link = None
        
        for link in links:
            text = link.text.lower()
            href = link.get('href', '')
            
            if target_quality in text:
                matched_link = href
                break
            fallback_link = href 
            
        final_url = matched_link if matched_link else fallback_link
        return final_url
    except Exception:
        return None

def download_video_file(url, output_path):
    """Downloads the target content file to local storage with interactive progress tracker bar."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(output_path, 'wb') as file, tqdm(
        desc=os.path.basename(output_path),
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

def main():
    print("==============================================")
    print("      AnimePahe Python Batch Downloader       ")
    print("==============================================")
    
    anime_input = input("🔹 Enter Anime Name or Direct URL: ").strip()
    if not anime_input:
        print("❌ Input cannot be blank.")
        return

    dub_sub = input("🔹 Select Type (sub / dub / all): ").strip().lower()
    if dub_sub not in ['sub', 'dub', 'all']:
        dub_sub = 'all'

    quality = input("🔹 Enter Preferred Quality (360p / 720p / 1080p): ").strip().lower()
    if quality not in ['360p', '720p', '1080p']:
        quality = '720p'

    driver = get_headless_browser()
    
    try:
        # Check if the user passed a direct URL instead of a search string
        if "animepahe.pw/anime/" in anime_input or "://animepahe.com" in anime_input:
            print("🔗 Direct AnimePahe link detected! Extracting session variables...")
            
            driver.get(anime_input)
            time.sleep(2)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            anime_id = None
            
            # Scrape page scripts for the API release runtime argument mapping
            for script in soup.find_all('script'):
                if script.string and 'id=' in script.string and 'release' in script.string:
                    match = re.search(r'id=([a-f0-9]+)', script.string)
                    if match:
                        anime_id = match.group(1)
                        break
            
            # Fallback 1: Extract from structural meta headers if direct regex target fails
            if not anime_id:
                meta_og = soup.find('meta', {'property': 'og:url'})
                if meta_og and 'play/' in meta_og.get('content', ''):
                    anime_id = meta_og.get('content').split('/')[-2]
            
            # Fallback 2: Direct text split context
            if not anime_id:
                anime_id = anime_input.strip('/').split('/')[-1]
                
            anime_title = soup.find('title').text.replace('- AnimePahe', '').strip() if soup.find('title') else "Downloaded_Anime"
            anime_title = "".join([c for c in anime_title if c.isalpha() or c.isdigit() or c in ' ']).rstrip()
            print(f"✅ Target Resolved: {anime_title} (Internal ID: {anime_id})")
            
        else:
            results = search_anime(driver, anime_input)
            filtered_results = filter_audio_preference(results, dub_sub)
            
            if not filtered_results:
                print("❌ No matching titles discovered with current filter configuration.")
                return
                
            print("\n💡 Found matching Series results:")
            for idx, anime in enumerate(filtered_results):
                print(f" [{idx + 1}] {anime.get('title')} ({anime.get('type', 'N/A')} - {anime.get('status', 'N/A')})")
                
            selection = int(input("\n👉 Select Anime number to fetch batch: ")) - 1
            selected_anime = filtered_results[selection]
            anime_id = selected_anime.get('session')
            anime_title = "".join([c for c in selected_anime.get('title') if c.isalpha() or c.isdigit() or c in ' ']).rstrip()
        
        # Pull down entire episode manifest
        episode_list = fetch_episode_links(driver, anime_id)
        if not episode_list:
            print("❌ Could not query dynamic episode listings from server framework database indexes.")
            return
            
        print(f"\n📂 Total Episodes Found: {len(episode_list)}")
        start_ep = int(input(f"👉 Enter Start Episode (1-{len(episode_list)}): "))
        end_ep = int(input(f"👉 Enter End Episode ({start_ep}-{len(episode_list)}): "))
        
        os.makedirs(anime_title, exist_ok=True)
        target_batch = episode_list[start_ep-1 : end_ep]
        
        print(f"\n🚀 Initiating batch download for episodes {start_ep} to {end_ep}...")
        for ep_node in target_batch:
            ep_num = ep_node.get('episode')
            ep_session = ep_node.get('session')
            print(f"\nProcessing Episode {ep_num}...")
            
            dl_url = get_download_url(driver, anime_id, ep_session, quality)
            if dl_url:
                out_file = os.path.join(anime_title, f"Episode_{ep_num}.mp4")
                try:
                    download_video_file(dl_url, out_file)
                except Exception as e:
                    print(f"❌ Failed to download episode {ep_num}: {e}")
            else:
                print(f"⚠️ Could not find a suitable download mirror link for episode {ep_num}")
                
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
