document.querySelectorAll('.main-button').forEach(button => {
  button.addEventListener('click', () => {
    alert(`${button.textContent} 버튼이 클릭되었습니다.`);
  });
});
