document.addEventListener('DOMContentLoaded', function () {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatBody = document.querySelector('.chat-body');
    const microphoneIcon = document.querySelector('.microphone-icon');
  
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;
  
    // Function to add initial system message
    function displayWelcomeMessage() {
        const welcomeMessage = document.createElement('div');
        welcomeMessage.classList.add('system-message');
        welcomeMessage.textContent = "Hi! How can I help you?";
        chatBody.appendChild(welcomeMessage);
        chatBody.scrollTop = chatBody.scrollHeight;
    }
  
    // Call displayWelcomeMessage immediately on load
    displayWelcomeMessage();
  
    function sendMessage() {
        const messageText = messageInput.value.trim();
  
        if (messageText) {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message');
            messageElement.textContent = messageText;
  
            chatBody.appendChild(messageElement);
            messageInput.value = '';
            chatBody.scrollTop = chatBody.scrollHeight;
        }
    }
  
    sendButton.addEventListener('click', sendMessage);
  
    messageInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });
  
    microphoneIcon.addEventListener('click', async function () {
        if (!isRecording) {
            startRecording();
        } else {
            await stopRecording();
        }
    });
  
    async function startRecording() {
        audioChunks = [];
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
  
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
  
        mediaRecorder.start();
        isRecording = true;
        microphoneIcon.textContent = "🔴";
    }
  
    async function stopRecording() {
        mediaRecorder.stop();
        isRecording = false;
        microphoneIcon.textContent = "🎤";
  
        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append('audio', audioBlob, 'audio.wav');
  
            try {
                const response = await fetch('/transcribe', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                if (data.text) {
                    messageInput.value = data.text; // Set transcribed text in input box
                }
            } catch (error) {
                console.error('Error transcribing audio:', error);
            }
        };
    }
  });
  