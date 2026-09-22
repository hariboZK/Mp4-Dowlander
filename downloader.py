#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Purpose Media Downloader
Supported Platforms: YouTube, Twitter/X, Instagram (Reels, Posts, Stories), TikTok, etc.
"""

import os
import sys
import shutil
from pathlib import Path

# Ensure UTF-8 output encoding across Windows terminals
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Base & Download directories
BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = BASE_DIR / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

def get_ffmpeg_path():
    """
    Locates ffmpeg executable in the tool directory, system PATH,
    or default winget install locations.
    """
    # 1. Check local tool folder first
    local_ffmpeg = BASE_DIR / "ffmpeg.exe"
    if local_ffmpeg.exists():
        return str(local_ffmpeg)

    # 2. Check system PATH
    in_path = shutil.which("ffmpeg")
    if in_path:
        return in_path

    # 3. Check Windows WinGet default directories
    local_app_data = os.environ.get("LOCALAPPDATA", "")
    if local_app_data:
        winget_links = Path(local_app_data) / "Microsoft" / "WinGet" / "Links" / "ffmpeg.exe"
        if winget_links.exists():
            return str(winget_links)

        winget_pkg = Path(local_app_data) / "Microsoft" / "WinGet" / "Packages"
        if winget_pkg.exists():
            for p in winget_pkg.glob("**/ffmpeg.exe"):
                return str(p)

    return None

def check_dependencies():
    """Checks if the required dependencies are installed."""
    missing = []
    try:
        import yt_dlp
    except ImportError:
        missing.append("yt-dlp")

    try:
        import instaloader
    except ImportError:
        missing.append("instaloader")

    if missing:
        print("\n[!] Missing dependencies detected:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nPlease install the required packages using the following command:")
        print("pip install -r requirements.txt\n")
        return False
    return True

def download_with_ytdlp(url: str, extract_audio: bool = False, browser_cookies: str = None):
    """
    Downloads video or audio from YouTube, Twitter (X), Instagram, and other supported platforms using yt-dlp.
    """
    import yt_dlp

    print(f"\n[*] Fetching and downloading media: {url}")

    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path:
        ffmpeg_dir = str(Path(ffmpeg_path).parent)
        if ffmpeg_dir not in os.environ.get("PATH", ""):
            os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

    outtmpl = str(DOWNLOAD_DIR / "%(title)s [%(id)s].%(ext)s")

    ydl_opts = {
        'outtmpl': outtmpl,
        'quiet': False,
        'no_warnings': False,
        'nocheckcertificate': True,
        'retries': 5,
        'fragment_retries': 5,
        'windowsfilenames': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['web', 'mweb', 'ios', 'android']
            }
        },
    }

    if ffmpeg_path:
        ydl_opts['ffmpeg_location'] = ffmpeg_path

    if extract_audio:
        if ffmpeg_path:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            print("[!] Warning: FFmpeg not detected. Downloading original audio format instead of MP3...")
            ydl_opts.update({
                'format': 'bestaudio/best',
            })
    else:
        if ffmpeg_path:
            # Best mp4 video and audio merged
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best',
                'merge_output_format': 'mp4',
            })
        else:
            print("[!] Note: FFmpeg not detected. Downloading best pre-merged stream...")
            ydl_opts.update({
                'format': 'b[ext=mp4]/best[ext=mp4]/best',
            })

    # If browser cookies are provided (for Instagram stories, private content, etc.)
    if browser_cookies:
        ydl_opts['cookiesfrombrowser'] = (browser_cookies, None, None, None)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'Unknown Title')
            print(f"\n[+] Download completed successfully: {title}")
            print(f"[+] Saved to: {DOWNLOAD_DIR}")
    except Exception as e:
        print(f"\n[-] An error occurred during download: {e}")

def download_instagram_story():
    """
    Downloads Instagram stories using Instaloader or browser cookies via yt-dlp.
    Instagram requires authentication to view and download stories.
    """
    import instaloader

    print("\n--- Instagram Story Downloader ---")
    print("Note: Instagram requires an authenticated session to view stories.")
    print("1) Login with your Instagram credentials to download")
    print("2) Use browser cookies via yt-dlp from story URL (Chrome / Edge / Firefox)")
    print("3) Back to main menu")

    choice = input("\nYour choice (1/2/3): ").strip()

    if choice == "1":
        username = input("Your Instagram Username: ").strip()
        target_username = input("Target profile username to download stories from: ").strip()

        if not username or not target_username:
            print("[-] Usernames cannot be empty.")
            return

        loader = instaloader.Instaloader(dirname_pattern=str(DOWNLOAD_DIR / "instagram_stories" / "{target}"))
        try:
            print(f"[*] Logging in as {username}...")
            loader.interactive_login(username)
            print(f"[*] Fetching stories for {target_username}...")
            profile = instaloader.Profile.from_username(loader.context, target_username)
            
            story_count = 0
            for story in loader.get_stories(userids=[profile.userid]):
                for item in story.get_items():
                    loader.download_storyitem(item, target=target_username)
                    story_count += 1

            if story_count > 0:
                print(f"[+] Successfully downloaded {story_count} stories.")
                print(f"[+] Directory: {DOWNLOAD_DIR / 'instagram_stories' / target_username}")
            else:
                print(f"[-] No active stories found on {target_username} or profile is private.")
        except Exception as e:
            print(f"[-] Instagram error: {e}")

    elif choice == "2":
        story_url = input("Story URL (e.g. https://www.instagram.com/stories/username/12345/): ").strip()
        browser = input("Browser you are logged in with (chrome / edge / firefox): ").strip().lower()
        if browser not in ["chrome", "edge", "firefox", "brave", "opera"]:
            browser = "chrome"

        download_with_ytdlp(story_url, extract_audio=False, browser_cookies=browser)

    else:
        return

def main():
    if not check_dependencies():
        sys.exit(1)

    ffmpeg_path = get_ffmpeg_path()
    ffmpeg_status = f"[OK] Ready ({Path(ffmpeg_path).name})" if ffmpeg_path else "[!] Not found (HD merge / MP3 disabled)"

    while True:
        print("\n" + "=" * 54)
        print("     MEDIA DOWNLOADER (YouTube, Twitter/X, Instagram)")
        print(f"     FFmpeg Engine: {ffmpeg_status}")
        print("=" * 54)
        print("1) Download Video (YouTube, Twitter/X, Reels/Posts, TikTok, etc.)")
        print("2) Download Audio Only - MP3 (YouTube, etc.)")
        print("3) Download Instagram Story")
        print("4) Open Downloads Folder")
        print("0) Exit")
        print("=" * 54)

        choice = input("Select an option: ").strip()

        if choice == "1":
            url = input("\nEnter video URL: ").strip()
            if url:
                download_with_ytdlp(url, extract_audio=False)
            else:
                print("[-] Invalid URL.")

        elif choice == "2":
            url = input("\nEnter URL for audio extraction: ").strip()
            if url:
                download_with_ytdlp(url, extract_audio=True)
            else:
                print("[-] Invalid URL.")

        elif choice == "3":
            download_instagram_story()

        elif choice == "4":
            print(f"\n[*] Opening folder: {DOWNLOAD_DIR}")
            if os.name == 'nt':
                os.startfile(DOWNLOAD_DIR)
            else:
                os.system(f"xdg-open '{DOWNLOAD_DIR}'")

        elif choice == "0":
            print("\nExiting. Have a great day!")
            break
        else:
            print("\n[-] Invalid selection, please try again.")

if __name__ == "__main__":
    main()
