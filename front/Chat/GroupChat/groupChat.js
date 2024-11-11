document.querySelectorAll('.group-item').forEach(item => {
  item.addEventListener('click', () => {
    document.querySelectorAll('.group-item').forEach(i => i.classList.remove('active'));
    item.classList.add('active');
    alert(`${item.textContent} 그룹 채팅으로 이동합니다.`);
  });
});
