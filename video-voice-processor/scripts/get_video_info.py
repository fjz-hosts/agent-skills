import subprocess
import json
import os
from pathlib import Path

def get_ffprobe_path():
    script_dir = Path(__file__).resolve().parent
    return str(script_dir.parent / "ffprobe.exe")

def get_video_info(video_path, ffprobe_path=None):
    """
    获取视频文件的详细信息
    
    Args:
        video_path: 视频文件路径
        ffprobe_path: ffprobe可执行文件路径,如果为None则使用技能目录下的ffprobe.exe
    
    Returns:
        dict: 包含视频信息的字典,包括:
            - duration: 时长(秒)
            - width: 视频宽度
            - height: 视频高度
            - frame_rate: 帧率
            - codec: 视频编码
            - audio_codec: 音频编码
            - bitrate: 比特率
    """
    if ffprobe_path is None:
        ffprobe_path = get_ffprobe_path()
    
    cmd = [
        ffprobe_path,
        '-v', 'error',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        video_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    
    if result.returncode != 0:
        raise Exception(f"ffprobe执行失败: {result.stderr}")
    
    data = json.loads(result.stdout)
    
    info = {
        'duration': 0,
        'width': 0,
        'height': 0,
        'frame_rate': 0,
        'codec': '',
        'audio_codec': '',
        'bitrate': 0
    }
    
    if 'format' in data:
        info['duration'] = float(data['format'].get('duration', 0))
        info['bitrate'] = int(data['format'].get('bit_rate', 0))
    
    for stream in data.get('streams', []):
        if stream['codec_type'] == 'video':
            info['width'] = int(stream.get('width', 0))
            info['height'] = int(stream.get('height', 0))
            info['codec'] = stream.get('codec_name', '')
            
            r_frame_rate = stream.get('r_frame_rate', '').split('/')
            if len(r_frame_rate) == 2:
                numerator, denominator = r_frame_rate
                info['frame_rate'] = float(numerator) / float(denominator) if denominator != '0' else 0
        elif stream['codec_type'] == 'audio':
            info['audio_codec'] = stream.get('codec_name', '')
    
    return info

def print_video_info(video_path, ffprobe_path=None):
    """
    打印视频信息
    
    Args:
        video_path: 视频文件路径
        ffprobe_path: ffprobe可执行文件路径
    """
    info = get_video_info(video_path, ffprobe_path)
    
    print("视频信息:")
    print(f"  时长: {info['duration']:.2f} 秒")
    print(f"  分辨率: {info['width']}x{info['height']}")
    print(f"  帧率: {info['frame_rate']:.2f} fps")
    print(f"  视频编码: {info['codec']}")
    print(f"  音频编码: {info['audio_codec']}")
    print(f"  比特率: {info['bitrate']} bps")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python get_video_info.py <视频文件路径> [ffprobe路径]")
        sys.exit(1)
    
    video_path = sys.argv[1]
    ffprobe_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    print_video_info(video_path, ffprobe_path)
