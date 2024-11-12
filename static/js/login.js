document.querySelector('.login-form').addEventListener('submit', async function (event) {
  event.preventDefault(); // 폼 기본 동작 막기

  const userId = document.querySelector('input[name="user_id"]').value;
  const password = document.querySelector('input[name="password"]').value;

  try {
      const response = await fetch('/auth/login', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ user_id: userId, password: password }),
      });

      const result = await response.json();
      
      if (response.ok) {
          alert('로그인 성공!');
          // 로그인 성공 시 원하는 페이지로 리다이렉트
          window.location.href = '/';
      } else {
          alert(result.error || '로그인 실패. 아이디와 비밀번호를 확인해주세요.');
      }
  } catch (error) {
      console.error('Error:', error);
      alert('서버 오류가 발생했습니다.');
  }
});
