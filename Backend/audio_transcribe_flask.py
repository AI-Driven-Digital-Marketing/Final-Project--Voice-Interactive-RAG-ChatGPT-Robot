from flask import Flask, request, jsonify
import wave
import openai

app = Flask(__name__)

# 保存音频数据为WAV文件的辅助函数
def save_wav(audio_data, filename):
    # WAV文件参数
    nchannels = 1
    sampwidth = 2
    framerate = 48000*2
    nframes = len(audio_data) // sampwidth
    comptype = "NONE"
    compname = "not compressed"

    # 创建一个新的.wav文件并写入音频数据
    with wave.open(filename, "wb") as audio_file:
        audio_file.setparams((nchannels, sampwidth, framerate, nframes, comptype, compname))
        audio_file.writeframes(audio_data)

# 使用OpenAI API转录音频文件的辅助函数
def transcribe(filename):
    # 假设你已经正确设置了OpenAI API的密钥
    openai.api_key = 'Your OpenAI API Key Here'

    # 打开音频文件并发送给OpenAI进行转录
    with open(filename, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    
    return transcript

# POST请求的路由，用于接收音频数据并返回转录结果
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # 从POST请求中获取音频数据
    audio_data = request.data  # 前端需要发送POST请求到/transcribe，主体部分应包含音频数据

    # 保存音频数据为WAV文件
    filename = "recorded_audio.wav"
    save_wav(audio_data, filename)

    # 转录音频文件
    transcript = transcribe(filename)
    
    # 将转录结果作为响应的一部分返回
    return jsonify({"status": "success", "message": "Audio data transcribed successfully.", "transcript": transcript})  # 前端可以从这个响应中获取转录结果

if __name__ == "__main__":
    app.run(debug=True)

'''
关于前端的接入，前端需要发送一个POST请求到/transcribe端点，
请求的主体部分应该包含音频数据。然后，前端可以从响应中获取转录结果。
具体的实现细节会依赖于前端使用的技术和框架。
'''