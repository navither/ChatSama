const chatbox = document.getElementById('chatbox');
const userInput = document.getElementById('user-input');
const submitButton = document.getElementById('submit-button');


// 添加用户输入到聊天记录
function addUserMessage(message) {
    const userMessage = document.createElement('p');
    userMessage.textContent = message;
    chatbox.appendChild(userMessage);
}

// 添加机器人回复到聊天记录
function addBotReply(reply) {
    const botReply = document.createElement('p');
    botReply.textContent = reply;
    chatbox.appendChild(botReply);
}
// 播放语音
function playAudio(url) {
   
    audio = new Audio(url);
    audio.play();
}
// 处理用户输入
function handleUserInput() {
    const userMessage = userInput.value.trim();

    if (userMessage !== '') {
        addUserMessage(userMessage);
        userInput.value = '';

        // 发送 POST 请求到后端 API
        fetch('http://localhost:5000/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // 处理后端返回的回复
            const reply = data.reply;
            addBotReply(reply);
            
            playAudio(data.audio_file);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}



// 模拟机器人回复
function simulateBotReply() {
    const reply = 'This is a sample bot reply.';
    addBotReply(reply);
}

submitButton.addEventListener('click', handleUserInput);
userInput.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        handleUserInput();
    }
});
