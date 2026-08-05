import os
import sys
import time
import json
import asyncio
import aiohttp
import aiofiles
import requests
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm_asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://animepahe.pw"
MAX_CONCURRENT_DOWNLOADS = 3  # Adjust this to change how many episodes download at once

def get_headless_browser():
    """Initializes a headless Selenium instance to pull search/episode maps safely."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def search_anime(driver, query):
    """Searches AnimePahe API for structural matches."""
    print(f"\n🔍 Searching for '{query}'...")
    search_url = f"{BASE_URL}/api?m=search&q={requests.utils.quote(query)}"
    driver.get(search_url)
    time.sleep(2)
    try:
        page_source = driver.find_element(By.TAG_NAME, "pre").text
        return json.loads(page_source).get('data', [])
    except Exception:
        return []

def fetch_episode_links(driver, anime_session_id):
    """Iterates through API pagination endpoints to gather all episode tokens."""
    print("📦 Scraping complete episode manifest maps...")
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
    """Resolves individual video links using Selenium to read dynamic embed menus."""
    ep_page_url = f"{BASE_URL}/play/{anime_session_id}/{episode_session_id}"
    driver.get(ep_page_url)
    try:
        wait = WebDriverWait(driver, 8)
        wait.until(EC.presence_of_element_located((By.ID, "download")))
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
        return matched_link if matched_link else fallback_link
    except Exception:
        return None

async def download_episode_worker(semaphore, session, url, output_path, ep_num):
    """Async worker bounded by a Semaphore to stream the file data without locking disk I/O."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    async with semaphore:
        try:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    print(f"❌ Failed to download Episode {ep_num} (HTTP status {response.status})")
                    return
                
                total_size = int(response.headers.get('content-length', 0))
                file_name = os.path.basename(output_path)
                
                # Initialize async progress tracker
                progress_bar = tqdm_asyncio(
                    desc=f"🎬 Ep {ep_num:02d}",
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                    leave=False
                )

                async with aiofiles.open(output_path, 'wb') as file:
                    # Stream file chunk by chunk asynchronously
                    async for chunk in response.content.iter_chunked(4096):
                        await file.write(chunk)
                        progress_bar.update(len(chunk))
                
                progress_bar.close()
                print(f"✅ Download Finished: {file_name}")
                
        except Exception as e:
            print(f"❌ Error during download processing execution for Episode {ep_num}: {e}")

async def batch_download_pipeline(download_queue, anime_title):
    """Coordinates and sets up concurrent downloading tasks using a common client session."""
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)
    
    # Clean output path directory structures cleanly
    os.makedirs(anime_title, exist_ok=True)
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for ep_num, dl_url in download_queue:
            file_name = f"{anime_title} - Episode {ep_num:02d}.mp4"
            output_file = os.path.join(anime_title, file_name)
            
            # Form task and append directly to the async run loop mapping tracker
            task = asyncio.ensure_future(
                download_episode_worker(semaphore, session, dl_url, output_file, ep_num)
            )
            tasks.append(task)
            
        # Execute concurrent worker pool wait queue
        await asyncio.gather(*tasks)

def main():
    print("==============================================")
    print("   AnimePahe Async Concurrent Downloader      ")
    print("==============================================")
    
    anime_name = input("🔹 Enter Anime Name: ").strip()
    quality = input("🔹 Enter Preferred Quality (360p / 720p / 1080p): ").strip().lower()
    if quality not in ['360p', '720p', '1080p']: quality = '720p'

    driver = get_headless_browser()
    
    try:
        results = search_anime(driver, anime_name)
        if not results:
            print("❌ No matching titles found.")
            return
            
        for idx, anime in enumerate(results):
            print(f" [{idx + 1}] {anime.get('title')} ({anime.get('type')} - {anime.get('status')})")
            
        selection = int(input("\n👉 Select Anime number: ")) - 1
        selected_anime = results[selection]
        anime_id = selected_anime.get('session')
        anime_title = "".join([c for c in selected_anime.get('title') if c.isalnum() or c in ' ']).strip()
        
        episode_list = fetch_episode_links(driver, anime_id)
        if not episode_list:
            print("❌ Episode mapping empty.")
            return
            
        print(f"\n📂 Total Episodes Found: {len(episode_list)}")
        start_ep = int(input(f"👉 Enter Start Episode (1-{len(episode_list)}): "))
        end_ep = int(input(f"👉 Enter End Episode ({start_ep}-{len(episode_list)}): "))
        
        target_batch = episode_list[start_ep-1 : end_ep]
        download_queue = []
        
        print("\n⚙️ Resolving video streaming source links. Please wait...")
        for ep_node in target_batch:
            ep_num = ep_node.get('episode')
            ep_session = ep_node.get('session')
            
            dl_url = get_download_url(driver, anime_id, ep_session, quality)
            if dl_url:
                download_queue.append((ep_num, dl_url))
            else:
                print(f"⚠️ Resolution link missing for Episode {ep_num}. Skipping.")
        
        # Shutdown browser instance immediately after structural link metadata harvesting finishes
        driver.quit()
        
        if not download_queue:
            print("❌ No valid download files could be mapped. Exiting pipeline.")
            return

        print(f"\n🚀 Launching async downloader. Downloading {MAX_CONCURRENT_DOWNLOADS} files at once...\n")
        
        # Hand off control directly over into the core asyncio loop structure
        asyncio.run(batch_download_pipeline(download_queue, anime_title))
        
        print("\n🎉 Batch download processing pipeline wrapped successfully!")

    except KeyboardInterrupt:
        print("\n🛑 Execution pipeline interrupted by user.")
    finally:
        try:
            driver.quit()
        except Exception:
            pass

if __name__ == "__main__":
    main()
