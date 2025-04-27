let cauHoi = [
  {
    text: "Tôi ___ to school every day.",
    options: ["go", "goes", "going", "gone"],
    correct: "go"
  },
  {
    text: "She ___ English very well.",
    options: ["speak", "speaks", "speaking", "spoke"],
    correct: "speaks"
  },
  {
    text: "They ___ football every weekend.",
    options: ["play", "plays", "playing", "played"],
    correct: "play"
  },
  {
    text: "We ___ dinner at 7 PM.",
    options: ["have", "has", "having", "had"],
    correct: "have"
  }
];

let total = cauHoi.length;
let userAnswers = new Array(total).fill("");
let current = 0;

function chonDapAn(answer) {
  userAnswers[current] = answer;
  hienCauHoi();
}

function hienCauHoi() {
  document.getElementById("currentQuestion").innerText = current + 1;
  document.getElementById("totalQuestions").innerText = total;

  let q = cauHoi[current];
  if (!q) {
    q = {
      text: `Câu ${current + 1} đang được cập nhật...`,
      options: []
    };
  }

  let html = `<div class="question-text">${q.text}</div>`;
  html += `<div class="options">`;
  q.options.forEach(opt => {
    const selectedClass = (userAnswers[current] === opt) ? "selected" : "";
    html += `<button class="${selectedClass}" onclick="chonDapAn('${opt}')">${opt}</button>`;
  });
  html += `</div>`;

  document.getElementById("questionBox").innerHTML = html;
}

function cauTiepTheo() {
  if (current < total - 1) {
    current++;
    hienCauHoi();
  } else {
    alert("🚀 Bạn đã đến câu cuối!");
  }
}

function cauTruoc() {
  if (current > 0) {
    current--;
    hienCauHoi();
  } else {
    alert("🔁 Đây là câu đầu tiên!");
  }
}

function nopBai() {
  let score = 0;
  let resultMsg = "";
  for (let i = 0; i < total; i++) {
    const q = cauHoi[i];
    if (!q || !q.correct) {
      resultMsg += `Câu ${i + 1}: Đang cập nhật\n`;
      continue;
    }
    if (userAnswers[i] === q.correct) {
      score++;
      resultMsg += `Câu ${i + 1}: ✅ Đúng\n`;
    } else {
      resultMsg += `Câu ${i + 1}: ❌ Sai (Đáp án đúng: ${q.correct})\n`;
    }
  }
  resultMsg = `Bạn được ${score}/${total} điểm.\n\n` + resultMsg;
  alert(resultMsg);
}

function huyBai() {
  if (confirm("Bạn có chắc muốn hủy bài tập không?")) {
    current = 0;
    userAnswers = new Array(total).fill("");
    hienCauHoi();
  }
}

// Hiển thị câu hỏi đầu tiên khi tải trang
hienCauHoi();
