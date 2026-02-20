---
name: "yt-dlp"
description: "Downloads videos from various websites using yt-dlp. Invoke when user provides a video link and asks to download it."
---

# yt-dlp Downloader

This skill uses yt-dlp, a feature-rich command-line audio/video downloader, to download videos from thousands of websites.

## When to Use

Invoke this skill when:
- User provides a video link and asks to download it
- User wants to save videos from websites for offline viewing
- User needs to download audio or video content from supported sites

## Installation

yt-dlp can be installed in several ways:

### Windows
Download the standalone executable from the [GitHub releases](https://github.com/yt-dlp/yt-dlp/releases):
- `yt-dlp.exe` (recommended for Windows x64)

### macOS
Download the universal executable:
- `yt-dlp_macos` (recommended for macOS 10.15+)

### Linux
Download the appropriate binary for your system:
- `yt-dlp` (platform-independent zipimport binary)
- `yt-dlp_linux` (standalone x86_64 binary)

### Using pip
```bash
pip install yt-dlp
```

## Usage

To download a video, simply provide the video URL:

```bash
yt-dlp [OPTIONS] URL
```

## Common Options

### Download Options
- `-f FORMAT`: Specify format code
- `-x`: Extract audio only
- `--audio-format FORMAT`: Set audio format (best, aac, flac, mp3, m4a, opus, vorbis, wav)
- `--audio-quality QUALITY`: Set audio quality (0-10)

### Output Options
- `-o TEMPLATE`: Output filename template
- `--download-archive FILE`: Download only videos not in archive

### Subtitle Options
- `--write-sub`: Write subtitle file
- `--write-auto-sub`: Write automatically generated subtitle file
- `--sub-lang LANGS`: Languages of subtitles to download

## Examples

### Download a video in best quality
```bash
yt-dlp https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Download only audio
```bash
yt-dlp -x https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Download with specific format
```bash
yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]" https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Download and save with custom filename
```bash
yt-dlp -o "%(title)s.%(ext)s" https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Supported Sites

yt-dlp supports thousands of sites, including:
- YouTube
- Bilibili
- Vimeo
- Twitch
- Twitter/X
- and many more

For a complete list, refer to the [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

## Updating

To update yt-dlp:

### Using the executable
```bash
yt-dlp -U
```

### Using pip
```bash
pip install --upgrade yt-dlp
```

## Troubleshooting

If you encounter issues:
- Check that yt-dlp is up to date
- Verify the video URL is correct and accessible
- Check your network connection
- Refer to the [yt-dlp GitHub issues](https://github.com/yt-dlp/yt-dlp/issues) for known problems

## Notes

- Respect copyright laws and terms of service of the websites you download from
- Some sites may require authentication or have geo-restrictions
- yt-dlp is a command-line tool, and this skill will execute it on your behalf
