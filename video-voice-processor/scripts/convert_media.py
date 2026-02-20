import subprocess
import os
from pathlib import Path

def get_ffmpeg_path():
    script_dir = Path(__file__).resolve().parent
    return str(script_dir.parent / "ffmpeg.exe")

def convert_media(input_path, output_path, ffmpeg_path=None, video_codec=None, audio_codec=None, video_bitrate=None, audio_bitrate=None, resolution=None, frame_rate=None):
    """
    转换视频或音频格式
    
    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径
        ffmpeg_path: ffmpeg可执行文件路径,如果为None则使用技能目录下的ffmpeg.exe
        video_codec: 视频编码器(如libx264, libx265, copy等)
        audio_codec: 音频编码器(如aac, mp3, copy等)
        video_bitrate: 视频比特率(如5M, 2M, 1M等)
        audio_bitrate: 音频比特率(如192k, 128k等)
        resolution: 分辨率(如1920x1080, 1280x720等)
        frame_rate: 帧率(如30, 60等)
    
    Returns:
        str: 输出文件路径
    """
    if ffmpeg_path is None:
        ffmpeg_path = get_ffmpeg_path()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    cmd = [ffmpeg_path, '-i', input_path]
    
    if video_codec:
        cmd.extend(['-c:v', video_codec])
    
    if audio_codec:
        cmd.extend(['-c:a', audio_codec])
    
    if video_bitrate:
        cmd.extend(['-b:v', video_bitrate])
    
    if audio_bitrate:
        cmd.extend(['-b:a', audio_bitrate])
    
    if resolution:
        cmd.extend(['-vf', f'scale={resolution}'])
    
    if frame_rate:
        cmd.extend(['-r', str(frame_rate)])
    
    cmd.extend(['-y', '-loglevel', 'quiet', output_path])
    
    result = subprocess.run(cmd, check=True)
    
    return output_path

def convert_video_to_mp4(input_path, output_path=None, ffmpeg_path=None, quality='medium'):
    """
    将视频转换为MP4格式
    
    Args:
        input_path: 输入视频路径
        output_path: 输出MP4路径,如果为None则自动生成
        ffmpeg_path: ffmpeg可执行文件路径
        quality: 质量(low/medium/high)
    
    Returns:
        str: 输出文件路径
    """
    if output_path is None:
        input_path_obj = Path(input_path)
        output_path = str(input_path_obj.parent / f"{input_path_obj.stem}.mp4")
    
    quality_map = {
        'low': {'video_bitrate': '1M', 'audio_bitrate': '128k'},
        'medium': {'video_bitrate': '3M', 'audio_bitrate': '192k'},
        'high': {'video_bitrate': '5M', 'audio_bitrate': '256k'}
    }
    
    q = quality_map.get(quality, quality_map['medium'])
    
    return convert_media(
        input_path,
        output_path,
        ffmpeg_path,
        video_codec='libx264',
        audio_codec='aac',
        video_bitrate=q['video_bitrate'],
        audio_bitrate=q['audio_bitrate']
    )

def convert_audio_to_mp3(input_path, output_path=None, ffmpeg_path=None, bitrate='192k'):
    """
    将音频转换为MP3格式
    
    Args:
        input_path: 输入音频路径
        output_path: 输出MP3路径,如果为None则自动生成
        ffmpeg_path: ffmpeg可执行文件路径
        bitrate: 比特率(如192k, 128k等)
    
    Returns:
        str: 输出文件路径
    """
    if output_path is None:
        input_path_obj = Path(input_path)
        output_path = str(input_path_obj.parent / f"{input_path_obj.stem}.mp3")
    
    return convert_media(
        input_path,
        output_path,
        ffmpeg_path,
        video_codec=None,
        audio_codec='libmp3lame',
        audio_bitrate=bitrate
    )

def convert_video_to_audio(input_path, output_path=None, ffmpeg_path=None, audio_format='mp3'):
    """
    将视频转换为音频
    
    Args:
        input_path: 输入视频路径
        output_path: 输出音频路径,如果为None则自动生成
        ffmpeg_path: ffmpeg可执行文件路径
        audio_format: 音频格式(mp3, wav, aac等)
    
    Returns:
        str: 输出文件路径
    """
    if output_path is None:
        input_path_obj = Path(input_path)
        output_path = str(input_path_obj.parent / f"{input_path_obj.stem}.{audio_format}")
    
    from .extract_audio import extract_audio
    return extract_audio(input_path, output_path, ffmpeg_path, audio_format=audio_format)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python convert_media.py <输入文件> <输出文件> [ffmpeg路径]")
        print("示例: python convert_media.py video.avi video.mp4")
        print("示例: python convert_media.py audio.wav audio.mp3")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    ffmpeg_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    output = convert_media(input_path, output_path, ffmpeg_path)
    print(f"转换完成,输出文件: {output}")
