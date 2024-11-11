document.querySelector('.signup-form').addEventListener('submit', function(event) {
  event.preventDefault();

  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirm-password').value;

  if (password !== confirmPassword) {
    alert('비밀번호가 일치하지 않습니다.');
    return;
  }

  alert('회원가입 정보가 제출되었습니다!');
});
