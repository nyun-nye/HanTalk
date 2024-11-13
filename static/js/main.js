document.querySelectorAll('.main-button').forEach(button => {
  button.addEventListener('click', async function (event) {
    event.preventDefault();

    try {
      const response = await fetch('/auth/check', { method: 'GET', credentials: 'include' });
      
      if (response.ok) {
        window.location.href = this.getAttribute('onclick').split("'")[1]; // 버튼 클릭 동작 수행
      } else {
        alert('로그인이 필요합니다.');
        window.location.href = '/login';  // 로그인 페이지로 리디렉션
      }
    } catch (error) {
      console.error('Error checking login status:', error);
      alert('서버와 통신 오류가 발생했습니다.');
    }
  });
});

document.addEventListener("DOMContentLoaded", async function () {
  try {
      const response = await fetch('/auth/check');
      if (!response.ok) {
          throw new Error('로그인이 필요합니다.');
      }
  } catch (error) {
      alert(error.message);
      window.location.href = '/login';  // 로그인 페이지로 리다이렉트
  }
});
