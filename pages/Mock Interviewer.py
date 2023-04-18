import streamlit as st
# from streamlit_audio_recorder import st_audio_recorder
import tempfile
import sounddevice as sd
import soundfile as sf

# 设置录音文件的参数
fs = 44100  # 采样率
seconds = 5  # 录音时长

# 创建 Streamlit 应用程序
def main():
    # 创建一个临时文件来保存录音
    recording_file = tempfile.NamedTemporaryFile(delete=False)

    # 创建 "Start Recording" 按钮并定义回调函数
    if st.button('Start Recording'):
        # 使用 sounddevice 库开始录音
        with sd.rec(int(fs * seconds), samplerate=fs, channels=1) as source:
            # 将录音数据写入临时文件
            sf.write(recording_file.name, source, fs)
        st.success('Recording is complete.')

    # 创建 "Stop Recording" 按钮并定义回调函数
    if st.button('Stop Recording'):
        st.audio(recording_file.name)
        st.stop()

# 运行 Streamlit 应用程序
if __name__ == '__main__':
    main()


