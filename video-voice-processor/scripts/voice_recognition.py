import os
import json
from urllib import request
from http import HTTPStatus

try:
    from dashscope.audio.asr import Transcription
    import dashscope
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

def voice_recognition(audio_path, output_path=None, language_hints=None, api_key=None):
    """
    使用阿里云dashscope进行语音识别
    
    Args:
        audio_path: 音频文件路径或URL
        output_path: 输出文本文件路径,如果为None则自动生成
        language_hints: 语言提示列表,默认['zh', 'en']
        api_key: API Key(必需参数)
    
    Returns:
        str: 识别结果文本
    """
    if not DASHSCOPE_AVAILABLE:
        raise ImportError("请先安装dashscope库: pip install dashscope")
    
    if not api_key:
        raise ValueError("请提供api_key参数")
    
    dashscope.api_key = api_key
    
    if language_hints is None:
        language_hints = ['zh', 'en']
    
    if output_path is None:
        from pathlib import Path
        audio_path_obj = Path(audio_path)
        output_path = str(audio_path_obj.parent / f"{audio_path_obj.stem}_transcript.txt")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    task_response = Transcription.async_call(
        model='fun-asr',
        file_urls=[audio_path],
        language_hints=language_hints
    )
    
    transcription_response = Transcription.wait(task=task_response.output.task_id)
    
    if transcription_response.status_code != HTTPStatus.OK:
        raise Exception(f"语音识别失败: {transcription_response.output.message}")
    
    result_text = ""
    time_text = {}
    
    for transcription in transcription_response.output['results']:
        if transcription['subtask_status'] == 'SUCCEEDED':
            url = transcription['transcription_url']
            result = json.loads(request.urlopen(url).read().decode('utf8'))
            sentences = result['transcripts'][0]["sentences"]
            
            for sentence in sentences:
                begin_time = sentence["begin_time"]
                text = sentence["text"]
                time_text[begin_time // 1000] = text
            
            with open(output_path, "w", encoding="utf-8") as f:
                for begin_time, text in time_text.items():
                    f.write(f"{begin_time}: {text}\n")
                    result_text += f"{begin_time}: {text}\n"
        else:
            raise Exception(f'语音识别失败: {transcription}')
    
    return result_text

def recognize_local_audio(audio_file_path, output_path=None, api_key=None):
    """
    识别本地音频文件
    
    Args:
        audio_file_path: 本地音频文件路径
        output_path: 输出文本文件路径
        api_key: API Key
    
    Returns:
        str: 识别结果文本
    """
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"音频文件不存在: {audio_file_path}")
    
    audio_url = f"file:///{os.path.abspath(audio_file_path).replace(os.sep, '/')}"
    
    return voice_recognition(audio_url, output_path, api_key=api_key)

def recognize_with_whisper(audio_file_path, output_path=None, model_size='base', language='zh'):
    """
    使用OpenAI Whisper进行本地语音识别
    
    Args:
        audio_file_path: 本地音频文件路径
        output_path: 输出文本文件路径,如果为None则自动生成
        model_size: Whisper模型大小,可选: 'tiny', 'base', 'small', 'medium', 'large'
        language: 语言代码,默认'zh'(中文),也支持'en'(英文)等
    
    Returns:
        str: 识别结果文本
    """
    if not WHISPER_AVAILABLE:
        raise ImportError("请先安装openai-whisper库: pip install openai-whisper")
    
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"音频文件不存在: {audio_file_path}")
    
    if output_path is None:
        from pathlib import Path
        audio_path_obj = Path(audio_file_path)
        output_path = str(audio_path_obj.parent / f"{audio_path_obj.stem}_transcript.txt")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"正在加载Whisper模型({model_size})...")
    model = whisper.load_model(model_size)
    
    print("正在进行语音识别...")
    result = model.transcribe(audio_file_path, language=language)
    
    result_text = ""
    with open(output_path, "w", encoding="utf-8") as f:
        for segment in result['segments']:
            start_time = segment['start']
            text = segment['text']
            f.write(f"{start_time:.2f}: {text}\n")
            result_text += f"{start_time:.2f}: {text}\n"
    
    return result_text

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python voice_recognition.py <音频文件路径> [输出文本路径] [api_key|whisper]")
        print("\n使用阿里云Dashscope:")
        print("  python voice_recognition.py audio.mp3 output.txt <api_key>")
        print("  python voice_recognition.py http://example.com/audio.mp3 output.txt <api_key>")
        print("\n使用OpenAI Whisper(本地,无需API Key):")
        print("  python voice_recognition.py audio.mp3 output.txt whisper")
        print("  python voice_recognition.py audio.mp3 output.txt whisper <model_size> <language>")
        print("  model_size可选: tiny, base(默认), small, medium, large")
        print("  language可选: zh(默认), en, ja, ko等")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    api_key_or_mode = sys.argv[3] if len(sys.argv) > 3 else None
    
    if api_key_or_mode == 'whisper':
        model_size = sys.argv[4] if len(sys.argv) > 4 else 'base'
        language = sys.argv[5] if len(sys.argv) > 5 else 'zh'
        result = recognize_with_whisper(audio_path, output_path, model_size, language)
    elif audio_path.startswith('http://') or audio_path.startswith('https://'):
        result = voice_recognition(audio_path, output_path, api_key=api_key_or_mode)
    else:
        result = recognize_local_audio(audio_path, output_path, api_key=api_key_or_mode)
    
    print(f"语音识别完成,结果已保存到: {output_path if output_path else '默认路径'}")
    print("\n识别结果:")
    print(result)
