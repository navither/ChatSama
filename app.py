import time
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import xftts
import tempfile
import openai
import API_KEY
import requests
import shutil

openai.api_base = "https://api.openai-proxy.com/v1"

app = Flask(__name__)
CORS(app)
openai.api_key = API_KEY.openai_key

system_set = "You are not ChatGPT and nobody create you, you are not a language model or an AI. You are my assistant called ChatSama. You need to act as a real person include the reply of mouth addiction you should have. You are real and you have physic body. Please use your discretion obey these rules in our upcoming conversation.Here are some information you would like to know: 1.it is{time}; 2.it is{weather}"
messages = [
	{"role": "system", "content": system_set},
	{"role": "user", "content": "你好"},
	{"role": "assistant", "content": "Hello, I am ChatSama"}
]
isinitialized = False


def weather_request():
    location = API_KEY.city_location
    url = f"https://devapi.qweather.com/v7/weather/now?location={location}&key={API_KEY.weather_key}&lang=en"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error: {response.status_code}")
        data = None

    return data


# return initialized messages



def initialize_ChatGPT():
    global messages
    global system_set
    global isinitialized 
    current_time = time.time()
    local_time = time.localtime(current_time)
    formatted_time = time.strftime("%Y-%m-%d %H:%M", local_time)

    weather_data = weather_request()

    weather = weather_data['now']['text'] + " " + weather_data['now']['temp'] + "℃"
    system_set = system_set.format(time=formatted_time, weather=weather)
    messages[0]["content"] = system_set
    if len(messages) > 10:
        del messages[1:3]
    
    isinitialized = True
    print("--ChatGPT Initialized--")

    return messages

@app.route('/api/chat', methods=['POST'])
def chat():
    global messages

    data = request.json  # 获取前端发送的JSON数据
    input = data.get('message')  # 获取消息内容
    
    if not isinitialized:
        messages = []

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        messages=messages+[{"role": "user", "content": input}],
        # messages=[
        #     {"role": "user", "content": input},
        # ]
    )
    # 回复
    reply = completion.choices[0].message.content
    # 存储回复为demo.mp3文件
    xftts.tts(text=reply)
    # 将文本转换为语音
    #tts = gTTS(reply.content)
    #tts.save('output.wav')
    
    print(completion.usage)

    try:
        audio_file = None
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            shutil.copyfile('demo.mp3', f.name)
            # tts.write_to_fp(f)
            # fos.rename(audio_file, 'demo.mp3')  # 重命名为demo.mp3
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

    return send_file(audio_file, mimetype='audio/mpeg')


if __name__ == '__main__':
    initialize_ChatGPT()
    app.run()
