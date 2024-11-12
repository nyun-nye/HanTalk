const socket = io();  // WebSocket 연결

socket.emit('join', { room: room });  // 방 참여

socket.on('connect', () => {
    console.log('[Client Log] Connected to server, joining room:', room);
    socket.emit('join', { room: room });
});


document.querySelector('.send-button').addEventListener('click', function () {
    const message = document.querySelector('.chat-input').value;
    const room = 'hansung1';  // 실제 방 ID
    socket.emit('send_message', { room: room, message: message });
    document.querySelector('.chat-input').value = '';  // 입력 필드 초기화
});

// 메시지 수신 이벤트
socket.on('receive_message', function (data) {
  console.log('[Client Log] Received message from server:', data);  // 메시지 수신 로그 확인
  if (!data) {
      console.error('[Client Log] No data received');
      return;
  }

  const chatWindow = document.querySelector('.chat-window');
  const newMessage = document.createElement('div');
  const isSent = data.sender === session_user_id;

  newMessage.classList.add('message', isSent ? 'sent' : 'received');
  newMessage.innerHTML = `<b>${data.sender}:</b> ${data.message}`;
  chatWindow.appendChild(newMessage);
  chatWindow.scrollTop = chatWindow.scrollHeight;
});
