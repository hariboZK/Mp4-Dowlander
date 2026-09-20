#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Purpose Media Downloader
Supported Platforms: YouTube, Twitter/X, Instagram (Reels, Posts, Stories), TikTok, etc.
"""

import os
import sys
from pathlib import Path

# Download directory
DOWNLOAD_DIR = Path(__file__).resolve().parent / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)

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
        print(f"pip install -r requirements.txt\n")
        return False
    return True

def download_with_ytdlp(url: str, extract_audio: bool = False, browser_cookies: str = None):
    """
    Downloads video or audio from YouTube, Twitter (X), Instagram, and other supported platforms using yt-dlp.
    """
    import yt_dlp

    print(f"\n[*] Fetching and downloading media: {url}")

    outtmpl = str(DOWNLOAD_DIR / "%(title)s [%(id)s].%(ext)s")

    ydl_opts = {
        'outtmpl': outtmpl,
        'quiet': False,
        'no_warnings': False,
    }

    if extract_audio:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # Best mp4 video and audio merged, or best standalone file
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
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

    while True:
        print("\n" + "=" * 50)
        print("     MEDIA DOWNLOADER (YouTube, Twitter/X, Instagram)")
        print("=" * 50)
        print("1) Download Video (YouTube, Twitter/X, Instagram Reels/Posts, TikTok, etc.)")
        print("2) Download Audio Only - MP3 (YouTube, etc.)")
        print("3) Download Instagram Story")
        print("4) Open Downloads Folder")
        print("0) Exit")
        print("=" * 50)

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
