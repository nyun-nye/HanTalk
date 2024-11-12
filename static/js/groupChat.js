document.addEventListener('DOMContentLoaded', function () {
  const socket = io();

  document.querySelectorAll('.group-item').forEach(item => {
      item.addEventListener('click', function () {
          const roomId = this.getAttribute('data-room-id');
          if (roomId) {
              window.location.href = `/chat/${roomId}`;
          } else {
              console.error('Room ID not found in data-room-id attribute.');
          }
      });
  });
});
