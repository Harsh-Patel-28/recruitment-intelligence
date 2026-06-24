const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("resumeFile");
const dzFilename = document.getElementById("dzFilename");

dropzone.addEventListener("click", () => fileInput.click());
dropzone.addEventListener("keydown", (e) => { if (e.key === "Enter") fileInput.click(); });

fileInput.addEventListener("change", () => {
  if (fileInput.files[0]) dzFilename.textContent = fileInput.files[0].name;
});

["dragover", "dragleave", "drop"].forEach(evt => {
  dropzone.addEventListener(evt, (e) => {
    e.preventDefault();
    dropzone.classList.toggle("drag-over", evt === "dragover");
  });
});
dropzone.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  if (file) {
    fileInput.files = e.dataTransfer.files;
    dzFilename.textContent = file.name;
  }
});

document.getElementById("uploadForm").addEventListener("submit", async function(event) {
  event.preventDefault();

  if (!fileInput.files[0]) {
    dzFilename.style.color = "var(--gap)";
    dzFilename.textContent = "Please choose a PDF file first";
    return;
  }

  const submitBtn = document.getElementById("submitBtn");
  const formData = new FormData();
  formData.append("resume", fileInput.files[0]);
  formData.append("job_description", document.getElementById("jobDescription").value);

  submitBtn.disabled = true;
  document.getElementById("results").innerHTML = "";

  const statusMessages = [
    "Reading resume...",
    "Comparing against job description...",
    "Drafting interview questions..."
  ];
  let statusIndex = 0;
  submitBtn.textContent = statusMessages[0];
  const statusInterval = setInterval(() => {
    statusIndex = (statusIndex + 1) % statusMessages.length;
    submitBtn.textContent = statusMessages[statusIndex];
  }, 2500);

  try {
    const response = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: formData
    });
    const data = await response.json();
    renderResults(data);
  } catch (err) {
    document.getElementById("results").innerHTML = `<div class="card">Something went wrong. Check that the server is running.</div>`;
  } finally {
    clearInterval(statusInterval);
    submitBtn.disabled = false;
    submitBtn.textContent = "Analyze Resume";
  }
});

function renderResults(data) {
  const resume = data.parsed_resume;
  const score = data.score_result;
  const questions = data.interview_questions.questions;

  const matchedChips = score.matched_skills.map(s => `<span class="chip matched">${s}</span>`).join("") || "<span class='chip'>None</span>";
  const missingChips = score.missing_skills.map(s => `<span class="chip missing">${s}</span>`).join("") || "<span class='chip'>None</span>";

  const questionItems = questions.map((q, i) => `
    <li class="q-item">
      <span class="q-num">${String(i + 1).padStart(2, "0")}</span>
      <span class="q-text"><span class="q-type ${q.type}">${q.type.replace("_", " ")}</span>${q.question}</span>
    </li>
  `).join("");

  document.getElementById("results").innerHTML = `
    <div class="card">
      <div class="score-row">
        <div class="score-ring" style="--pct:${score.score}">
          <div class="score-inner">
            <span class="num">${score.score}</span>
            <span class="label">/ 100</span>
          </div>
        </div>
        <p class="score-reasoning">${score.reasoning}</p>
      </div>
      <h2 class="section-title">Matched Skills</h2>
      <div class="chip-group">${matchedChips}</div>
      <h2 class="section-title">Missing Skills</h2>
      <div class="chip-group">${missingChips}</div>
    </div>

    <div class="card">
      <h2 class="section-title">Candidate</h2>
      <p class="resume-meta">
        <strong>${resume.name}</strong><br>
        ${resume.education}<br>
        ${resume.experience_years} years experience
      </p>
    </div>

    <div class="card">
      <h2 class="section-title">Interview Questions</h2>
      <ol class="q-list">${questionItems}</ol>
    </div>
  `;
}