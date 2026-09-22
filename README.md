<div align="center">

# 🎬 Universal Media Downloader

**A lightweight, pure Python CLI tool to download videos, audios, and stories from YouTube, Twitter/X, Instagram, TikTok, and 1000+ sites.**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pure Python](https://img.shields.io/badge/code-100%25%20Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](downloader.py)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg?style=for-the-badge)](https://github.com/)
[![Powered by](https://img.shields.io/badge/powered%20by-yt--dlp%20%26%20instaloader-orange.svg?style=for-the-badge)](https://github.com/yt-dlp/yt-dlp)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

[Features](#-key-features) • [Installation](#-installation) • [How to Run](#-how-to-run) • [FFmpeg Setup](#-ffmpeg-handling) • [Supported Platforms](#-supported-platforms) • [License](#-license)

</div>

---

## ✨ Key Features

- 🐍 **100% Pure Python:** No heavy binary `.exe` files in the repository. Safe, lightweight, and Git-friendly.
- 🎯 **Best Quality Video (MP4):** Automatically pulls the highest resolution streams (up to 4K/8K) and merges them cleanly into `.mp4`.
- 🎵 **High-Quality Audio (MP3):** One-click extraction from video links into 192kbps `.mp3` audio files.
- 📸 **Instagram Story Downloader:** Download active stories via credentials or browser session cookies (Chrome / Edge / Firefox).
- ⚡ **Auto-Engine Detection:** Automatically discovers FFmpeg on your system (WinGet, PATH, or local directories) with zero manual configuration needed.
- 🖥️ **Cross-Platform:** Works on Windows, macOS, and Linux out of the box.

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/media-downloader.git
cd media-downloader
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run

### Windows
Run via Python or double-click `run.bat`:
```powershell
python downloader.py
```

### Linux / macOS
```bash
python3 downloader.py
```

---

## ⚙️ FFmpeg Handling

This project is kept **pure code** without committing 150MB+ `.exe` files to GitHub. 

When you run `downloader.py`, it automatically searches your system for FFmpeg. If you don't have FFmpeg installed yet, you can install it with a single command:

- **Windows (Recommended):**
  ```powershell
  winget install yt-dlp.FFmpeg
  ```
- **macOS:**
  ```bash
  brew install ffmpeg
  ```
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```

> [!NOTE]
> Even if FFmpeg is not installed, the downloader automatically falls back to single-stream downloading so you can still download videos!

---

## 🌐 Supported Platforms

| Platform | Supported Formats | Quality / Notes |
| :--- | :--- | :--- |
| **YouTube** | Videos, Shorts, Music | Up to 8K, 60fps, MP3 extraction |
| **Twitter / X** | Videos, Clips, GIFs | Highest available bitrate |
| **Instagram** | Reels, Posts, Carousels, **Stories** | Stories support login & cookies |
| **TikTok** | Videos, Original Audio | Full HD, watermark-free |
| **Reddit** | Videos with synced audio | Merges video & audio |
| **Twitch** | Clips, Highlights, VODs | Best stream quality |
| **Facebook** | Public Videos, Reels | High Definition MP4 |
| **SoundCloud** | Audio Tracks, Playlists | MP3 / Original audio |
| **1000+ Others** | Vimeo, Dailymotion, Pinterest, etc. | Supported via `yt-dlp` core |

---

## 📂 Repository Structure

```text
media-downloader/
│
├── downloader.py          # Core application (pure Python)
├── run.bat               # Windows quick launcher
├── requirements.txt       # Dependencies (yt-dlp, instaloader)
├── .gitignore            # Keeps repo clean of downloads and temp files
├── LICENSE               # MIT License
└── README.md              # Project documentation
```

---

## ⚖️ Disclaimer

This project is intended for **personal, educational, and backup purposes only**. Downloading copyrighted content without authorization may violate platform terms of service and copyright laws. Always respect intellectual property rights.

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.
