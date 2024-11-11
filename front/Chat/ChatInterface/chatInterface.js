const chatWindow = document.querySelector('.chat-window');
const chatInput = document.querySelector('.chat-input');
const sendButton = document.querySelector('.send-button');

sendButton.addEventListener('click', () => {
  const messageText = chatInput.value.trim();
  
  if (messageText) {
    const message = document.createElement('div');
    message.className = 'message sent';
    message.innerHTML = `나<br>${messageText}`;
    chatWindow.appendChild(message);
    
    chatInput.value = '';
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }
});
