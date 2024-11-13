document.addEventListener('DOMContentLoaded', function () {
  const chatItems = document.querySelectorAll('.chat-item');

  chatItems.forEach(item => {
      item.addEventListener('click', function () {
          const receiverId = this.textContent; // 클릭한 사용자의 ID
          window.location.href = `/chatInterface/${receiverId}`; // 해당 ID로 채팅 화면 이동
      });
  });
});
