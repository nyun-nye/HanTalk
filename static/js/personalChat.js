document.addEventListener('DOMContentLoaded', function () {
  const chatItems = document.querySelectorAll('.chat-item');
  const searchInput = document.querySelector('.search-input');

  chatItems.forEach(item => {
      item.addEventListener('click', function () {
          const receiverId = this.getAttribute('data-room'); // 클릭한 사용자의 ID
          window.location.href = `/chatInterface/${receiverId}`; // 해당 ID로 채팅 화면 이동
      });
  });

  searchInput.addEventListener('keypress', async function (event) {
    if (event.key === 'Enter') {
      const userId = searchInput.value.trim();

      if (!userId) {
        alert('검색어를 입력하세요.');
        return;
      }

      try {
        const response = await fetch(`/auth/check_user/${userId}`);
        if (response.ok) {
          window.location.href = `/chatInterface/${userId}`; // 해당 ID로 채팅 화면 이동
        } else {
          alert('존재하지 않는 사용자 ID입니다.');
        }
      } catch (error) {
        console.error('Error checking user ID:', error);
        alert('서버 오류가 발생했습니다. 나중에 다시 시도하세요.');
      }
    }
  });
});
