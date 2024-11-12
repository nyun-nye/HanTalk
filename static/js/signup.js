document.getElementById("signup-form").addEventListener("submit", function (e) {
  e.preventDefault(); // 폼 기본 동작 방지

  const formData = {
    name: document.getElementById("name").value,
    student_id: document.getElementById("student_id").value,
    user_id: document.getElementById("user_id").value,
    password: document.getElementById("password").value,
    password_confirm: document.getElementById("confirm-password").value
  };

  if (formData.password !== formData.password_confirm) {
    alert("비밀번호가 일치하지 않습니다.");
    return;
  }

  fetch("/auth/signUp", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(formData)
  })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
        alert(data.message);
        window.location.href = "/login"; // 성공 시 로그인 페이지로 이동
      } else if (data.error) {
        alert(`Error: ${data.error}`);
      }
    })
    .catch(error => console.error("Error:", error));
});
