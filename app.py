from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from gtts import gTTS
import tempfile
import openai
import API_KEY

app = Flask(__name__)
CORS(app)
openai.api_key = API_KEY.openai_key
system_set = "hello"
input = system_set


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json  # 获取前端发送的JSON数据
    input = data.get('message')  # 获取消息内容

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        messages=[
            {"role": "user", "content": input},
        ]
    )
    # 回复
    reply = completion.choices[0].message
    # 将文本转换为语音
    tts = gTTS(reply.content)
    #tts.save('output.wav')
    
    print(completion.usage)

    try:
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            tts.write_to_fp(f)
            audio_file = f.name
    except Exception as e:
        print(f'Error saving audio file: {e}')
        audio_file = None

    return jsonify({'reply': reply,
                    'audio_file': audio_file
                    })


@app.route('/api/chat/audio')
def audio():
    # 返回语音文件
    audio_file = request.args.get('file')
    if audio_file is None:
        return 'Missing audio file', 400

    return send_file(audio_file, mimetype='audio/wav')


if __name__ == '__main__':
    app.run()
