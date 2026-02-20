import subprocess
import os
from pathlib import Path

def get_ffmpeg_path():
    script_dir = Path(__file__).resolve().parent
    return str(script_dir.parent / "ffmpeg.exe")

def extract_audio(video_path, output_path=None, ffmpeg_path=None, audio_format='mp3', sample_rate=16000, channels=1, quality=2):
    """
    从视频文件中提取音频
    
    Args:
        video_path: 视频文件路径
        output_path: 输出音频文件路径,如果为None则自动生成
        ffmpeg_path: ffmpeg可执行文件路径,如果为None则使用技能目录下的ffmpeg.exe
        audio_format: 音频格式(mp3, wav, aac等)
        sample_rate: 采样率(默认16000)
        channels: 声道数(1=单声道, 2=立体声)
        quality: 音频质量(对于mp3,0-9,越小质量越好)
    
    Returns:
        str: 输出音频文件路径
    """
    if ffmpeg_path is None:
        ffmpeg_path = get_ffmpeg_path()
    
    if output_path is None:
        video_path_obj = Path(video_path)
        output_path = str(video_path_obj.parent / f"{video_path_obj.stem}.{audio_format}")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    codec_map = {
        'mp3': 'libmp3lame',
        'wav': 'pcm_s16le',
        'aac': 'aac',
        'm4a': 'aac',
        'flac': 'flac'
    }
    
    codec = codec_map.get(audio_format, 'libmp3lame')
    
    cmd = [
        ffmpeg_path,
        '-i', video_path,
        '-vn',
        '-acodec', codec,
        '-q:a', str(quality),
        '-ar', str(sample_rate),
        '-ac', str(channels),
        '-y',
        '-loglevel', 'quiet',
        output_path
    ]
    
    result = subprocess.run(cmd, check=True)
    
    return output_path

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python extract_audio.py <视频文件路径> [输出音频路径] [ffmpeg路径]")
        print("示例: python extract_audio.py video.mp3 output.mp3")
        print("示例: python extract_audio.py video.mp3 output.wav")
        sys.exit(1)
    
    video_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    ffmpeg_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    output = extract_audio(video_path, output_path, ffmpeg_path)
    print(f"音频已提取到: {output}")
