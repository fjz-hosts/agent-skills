---
name: video-voice-processor
description: "Comprehensive video and audio processing toolkit for extracting information, converting formats, and performing voice recognition. Use when Claude needs to get video metadata, extract audio from video files, convert video/audio formats, perform speech-to-text recognition using Aliyun Dashscope API, or process local video/audio files for analysis."
---

# Video Voice Processor

## Overview

This skill provides a complete toolkit for video and audio processing operations. It enables extraction of video metadata, audio extraction from videos, format conversion, and speech recognition using both Aliyun's Dashscope API and OpenAI's Whisper. All operations are performed using ffmpeg/ffprobe for media processing, dashscope for cloud-based voice recognition, and whisper for local offline voice recognition.

## Quick Start

### Get Video Information

Extract detailed metadata from video files including duration, resolution, frame rate, and codec information:

```python
from scripts.get_video_info import get_video_info

info = get_video_info("path/to/video.mp4")
print(f"Duration: {info['duration']}s, Resolution: {info['width']}x{info['height']}")
```

Or run directly:
```bash
python scripts/get_video_info.py video.mp4
```

### Extract Audio from Video

Extract audio track from video files in various formats (MP3, WAV, AAC, FLAC):

```python
from scripts.extract_audio import extract_audio

audio_path = extract_audio("video.mp4", "output.mp3")
```

Or run directly:
```bash
python scripts/extract_audio.py video.mp4 output.mp3
```

### Convert Media Formats

Convert between different video and audio formats:

```python
from scripts.convert_media import convert_video_to_mp4, convert_audio_to_mp3

# Convert video to MP4
mp4_path = convert_video_to_mp4("video.avi", "output.mp4", quality='high')

# Convert audio to MP3
mp3_path = convert_audio_to_mp3("audio.wav", "output.mp3", bitrate='192k')
```

Or run directly:
```bash
python scripts/convert_media.py input.avi output.mp4
```

### Voice Recognition

Perform speech-to-text recognition on audio files using either Aliyun Dashscope (cloud-based) or OpenAI Whisper (local, offline):

**Option 1: Using OpenAI Whisper (Recommended for offline use)**

```python
from scripts.voice_recognition import recognize_with_whisper

transcript = recognize_with_whisper("audio.mp3", "output.txt")
```

Or run directly:
```bash
python scripts/voice_recognition.py audio.mp3 output.txt whisper
```

**Option 2: Using Aliyun Dashscope (Cloud-based)**

```python
from scripts.voice_recognition import recognize_local_audio

transcript = recognize_local_audio("audio.mp3", "output.txt", api_key="your-api-key")
```

Or run directly:
```bash
python scripts/voice_recognition.py audio.mp3 output.txt <api-key>
```

## Core Capabilities

### 1. Video Information Extraction

Use `scripts/get_video_info.py` to extract comprehensive video metadata:

**Supported information:**
- Duration (in seconds)
- Resolution (width x height)
- Frame rate (fps)
- Video codec
- Audio codec
- Bitrate

**Requirements:**
- ffprobe.exe is included in the skill directory

**Example usage:**
```python
from scripts.get_video_info import get_video_info, print_video_info

# Get info as dictionary
info = get_video_info("video.mp4")

# Print formatted info
print_video_info("video.mp4")
```

### 2. Audio Extraction

Use `scripts/extract_audio.py` to extract audio from video files:

**Supported audio formats:**
- MP3 (default, libmp3lame)
- WAV (pcm_s16le)
- AAC
- M4A
- FLAC

**Parameters:**
- `sample_rate`: Default 16000 Hz (adjustable)
- `channels`: 1 (mono) or 2 (stereo)
- `quality`: 0-9 for MP3 (lower = better quality)

**Example usage:**
```python
from scripts.extract_audio import extract_audio

# Extract with default settings
audio = extract_audio("video.mp4", "audio.mp3")

# Extract with custom settings
audio = extract_audio(
    "video.mp4", 
    "audio.wav",
    audio_format='wav',
    sample_rate=44100,
    channels=2
)
```

### 3. Format Conversion

Use `scripts/convert_media.py` for comprehensive media format conversion:

**Video conversion:**
```python
from scripts.convert_media import convert_video_to_mp4

# Convert to MP4 with quality preset
mp4 = convert_video_to_mp4("video.avi", "output.mp4", quality='high')
# Quality options: 'low', 'medium', 'high'
```

**Audio conversion:**
```python
from scripts.convert_media import convert_audio_to_mp3

# Convert to MP3 with custom bitrate
mp3 = convert_audio_to_mp3("audio.wav", "output.mp3", bitrate='320k')
```

**Advanced conversion:**
```python
from scripts.convert_media import convert_media

# Full control over conversion parameters
output = convert_media(
    "input.mp4",
    "output.mp4",
    video_codec='libx265',
    audio_codec='aac',
    video_bitrate='5M',
    audio_bitrate='256k',
    resolution='1920x1080',
    frame_rate=30
)
```

### 4. Voice Recognition

Use `scripts/voice_recognition.py` for speech-to-text recognition:

**Two recognition engines available:**

#### Option 1: OpenAI Whisper (Local, Offline)

**Requirements:**
- Install openai-whisper: `pip install openai-whisper`
- No API key required
- Works completely offline

**Features:**
- Supports local audio files only
- Multi-language support (Chinese, English, Japanese, Korean, etc.)
- Multiple model sizes: tiny, base, small, medium, large
- Timestamp output (seconds from start)
- Better for privacy and offline use

**Example usage:**
```python
from scripts.voice_recognition import recognize_with_whisper

# Recognize with default settings (base model, Chinese)
transcript = recognize_with_whisper("audio.mp3", "transcript.txt")

# Recognize with custom model and language
transcript = recognize_with_whisper(
    "audio.mp3",
    "transcript.txt",
    model_size='small',  # tiny, base, small, medium, large
    language='zh'  # zh, en, ja, ko, etc.
)
```

#### Option 2: Aliyun Dashscope (Cloud-based)

**Requirements:**
- Dashscope API key (must be provided as parameter)
- Install dashscope: `pip install dashscope`

**Features:**
- Supports local audio files
- Supports audio URLs
- Multi-language support (Chinese, English)
- Timestamp output (seconds from start)
- Requires internet connection

**Example usage:**
```python
from scripts.voice_recognition import recognize_local_audio, voice_recognition

# Recognize local audio file
transcript = recognize_local_audio("audio.mp3", "transcript.txt", api_key="your-key")

# Recognize from URL
transcript = voice_recognition(
    "http://example.com/audio.mp3",
    "transcript.txt",
    language_hints=['zh', 'en'],
    api_key="your-key"
)
```

## Workflow Decision Tree

When processing video/audio files:

1. **Need video metadata?** → Use `get_video_info.py`
2. **Need audio from video?** → Use `extract_audio.py`
3. **Need format conversion?** → Use `convert_media.py`
4. **Need speech recognition?** → Use `voice_recognition.py`
5. **Complete pipeline (video → audio → text)?** → Chain: `extract_audio.py` → `voice_recognition.py`

## Environment Setup

### Required Python Packages

Choose one or both based on your needs:

**For OpenAI Whisper (Local, Offline):**
```bash
pip install openai-whisper
```

**For Aliyun Dashscope (Cloud-based):**
```bash
pip install dashscope
```

**Both (Recommended for maximum flexibility):**
```bash
pip install openai-whisper dashscope
```

## Common Use Cases

### Extract Transcript from Video

Complete workflow to get text from video:

**Option 1: Using Whisper (Recommended, Offline)**
```python
from scripts.extract_audio import extract_audio
from scripts.voice_recognition import recognize_with_whisper

# Step 1: Extract audio
audio_path = extract_audio("video.mp4", "temp_audio.wav", audio_format='wav')

# Step 2: Recognize speech with Whisper
transcript = recognize_with_whisper(audio_path, "transcript.txt")
```

**Option 2: Using Dashscope (Cloud-based)**
```python
from scripts.extract_audio import extract_audio
from scripts.voice_recognition import recognize_local_audio

# Step 1: Extract audio
audio_path = extract_audio("video.mp4", "temp_audio.mp3")

# Step 2: Recognize speech with Dashscope
transcript = recognize_local_audio(audio_path, "transcript.txt", api_key="your-api-key")
```

### Convert Video for Web

Convert video to web-friendly MP4 format:

```python
from scripts.convert_media import convert_video_to_mp4

web_video = convert_video_to_mp4(
    "source.avi",
    "web.mp4",
    quality='medium'
)
```

### Batch Process Videos

Process multiple videos:

```python
from pathlib import Path
from scripts.get_video_info import get_video_info

video_dir = Path("videos")
for video in video_dir.glob("*.mp4"):
    info = get_video_info(str(video))
    print(f"{video.name}: {info['duration']}s")
```

## Resources

### scripts/

- **get_video_info.py**: Extract video metadata using ffprobe
- **extract_audio.py**: Extract audio from video files using ffmpeg
- **convert_media.py**: Convert between video/audio formats
- **voice_recognition.py**: Speech-to-text recognition using OpenAI Whisper (local) or Aliyun Dashscope (cloud)

All scripts can be executed directly from command line or imported as Python modules.

### Voice Recognition Comparison

| Feature | Whisper (Local) | Dashscope (Cloud) |
|---------|----------------|-------------------|
| **API Key Required** | No | Yes |
| **Internet Required** | No | Yes |
| **Privacy** | High (local processing) | Medium (cloud processing) |
| **Speed** | Depends on hardware | Fast (cloud processing) |
| **Accuracy** | Good to Excellent | Good |
| **Languages** | 99+ languages | Chinese, English |
| **Audio Sources** | Local files only | Local files & URLs |
| **Model Sizes** | tiny, base, small, medium, large | Single model |
| **Cost** | Free (after initial download) | Pay-per-use |
