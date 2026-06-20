const MANIFEST_URL = "./geography_bank/review_manifest.json";
const REVIEW_STORAGE_KEY = "geography-cleaning-review-v1";
const IMAGE_CACHE_VERSION = "2026-06-11-q5-q10-q15-q22-q28-q30-q34";

const state = {
  banks: [],
  bankId: "",
  filter: "all",
  search: "",
  currentId: "",
  records: loadRecords(),
};

const elements = {
  bankSelect: document.querySelector("#bankSelect"),
  searchInput: document.querySelector("#searchInput"),
  questionList: document.querySelector("#questionList"),
  progressText: document.querySelector("#progressText"),
  questionMeta: document.querySelector("#questionMeta"),
  questionTitle: document.querySelector("#questionTitle"),
  groupPrompt: document.querySelector("#groupPrompt"),
  questionStem: document.querySelector("#questionStem"),
  questionOptions: document.querySelector("#questionOptions"),
  questionAnswer: document.querySelector("#questionAnswer"),
  cleanedImages: document.querySelector("#cleanedImages"),
  sourceReviews: document.querySelector("#sourceReviews"),
  reviewNotes: document.querySelector("#reviewNotes"),
  reviewContent: document.querySelector("#reviewContent"),
  emptyState: document.querySelector("#emptyState"),
  prevButton: document.querySelector("#prevButton"),
  nextButton: document.querySelector("#nextButton"),
  pageDialog: document.querySelector("#pageDialog"),
  pageDialogImage: document.querySelector("#pageDialogImage"),
  dialogTitle: document.querySelector("#dialogTitle"),
  closeDialog: document.querySelector("#closeDialog"),
};

function loadRecords() {
  try {
    return JSON.parse(localStorage.getItem(REVIEW_STORAGE_KEY)) || {};
  } catch {
    return {};
  }
}

function saveRecords() {
  localStorage.setItem(REVIEW_STORAGE_KEY, JSON.stringify(state.records));
}

function recordKey(question) {
  return `${state.bankId}:${question.id}`;
}

function getRecord(question) {
  return state.records[recordKey(question)] || { status: "pending", notes: "" };
}

function getBank() {
  return state.banks.find((bank) => bank.id === state.bankId);
}

function filteredQuestions() {
  const bank = getBank();
  if (!bank) return [];
  const keyword = state.search.trim().toLowerCase();
  return bank.questions.filter((question) => {
    const record = getRecord(question);
    const statusMatches = state.filter === "all" || record.status === state.filter;
    const content = [
      question.number,
      question.stem,
      question.groupPrompt,
      Object.values(question.options || {}).join(" "),
    ]
      .join(" ")
      .toLowerCase();
    return statusMatches && (!keyword || content.includes(keyword));
  });
}

function currentQuestion() {
  const list = filteredQuestions();
  return list.find((question) => question.id === state.currentId) || list[0] || null;
}

function statusLabel(status) {
  return { pending: "待核对", approved: "已通过", rework: "需返工" }[status] || "待核对";
}

function ensureCurrentQuestion() {
  const list = filteredQuestions();
  if (!list.some((question) => question.id === state.currentId)) {
    state.currentId = list[0]?.id || "";
  }
}

function renderBankOptions() {
  elements.bankSelect.innerHTML = state.banks
    .map((bank) => `<option value="${bank.id}">${bank.title}</option>`)
    .join("");
  elements.bankSelect.value = state.bankId;
}

function renderQuestionList() {
  const bank = getBank();
  const list = filteredQuestions();
  const approvedCount = bank
    ? bank.questions.filter((question) => getRecord(question).status === "approved").length
    : 0;
  elements.progressText.textContent = `${approvedCount} / ${bank?.questions.length || 0}`;
  elements.questionList.innerHTML = list
    .map((question) => {
      const record = getRecord(question);
      const active = question.id === state.currentId ? " active" : "";
      return `
        <button class="review-question${active}" data-id="${question.id}" type="button">
          <span>第 ${question.number} 题</span>
          <small class="status ${record.status}">${statusLabel(record.status)}</small>
        </button>
      `;
    })
    .join("");
}

function renderOptions(question) {
  const entries = Object.entries(question.options || {});
  elements.questionOptions.innerHTML = entries
    .map(([key, value]) => `<p><strong>${key}</strong><span>${value}</span></p>`)
    .join("");
}

function renderCleanedImages(question) {
  elements.cleanedImages.innerHTML = question.images
    .map(
      (src, index) => `
        <figure class="cleaned-figure">
          <img src="${src}?v=${IMAGE_CACHE_VERSION}" alt="第${question.number}题清洗后关联图${index + 1}" />
        </figure>
      `,
    )
    .join("");
}

function drawReviewCanvas(canvas, review) {
  const image = new Image();
  image.onload = () => {
    const [x, y, width, height] = review.box;
    const maxWidth = 1500;
    const scale = Math.min(1, maxWidth / width);
    canvas.width = Math.round(width * scale);
    canvas.height = Math.round(height * scale);
    const context = canvas.getContext("2d");
    context.imageSmoothingEnabled = true;
    context.imageSmoothingQuality = "high";
    context.drawImage(image, x, y, width, height, 0, 0, canvas.width, canvas.height);
  };
  image.src = review.pageImage;
}

function openPage(review) {
  elements.pageDialogImage.src = review.pageImage;
  elements.dialogTitle.textContent = `原卷第 ${review.page} 页`;
  elements.pageDialog.showModal();
}

function renderSourceReviews(question) {
  elements.sourceReviews.innerHTML = "";
  question.reviews.forEach((review, index) => {
    const button = document.createElement("button");
    button.className = "source-review";
    button.type = "button";
    button.innerHTML = `
      <canvas aria-label="第${question.number}题原卷区域核对截图${index + 1}"></canvas>
      <span>
        <strong>原卷第 ${review.page} 页</strong>
        <small>${review.caption || "整题区域"} · 点击查看整页</small>
      </span>
    `;
    button.addEventListener("click", () => openPage(review));
    elements.sourceReviews.append(button);
    drawReviewCanvas(button.querySelector("canvas"), review);
  });
}

function renderDecision(question) {
  const record = getRecord(question);
  elements.reviewNotes.value = record.notes || "";
  document.querySelectorAll(".decision-button").forEach((button) => {
    button.classList.toggle("active", button.dataset.status === record.status);
  });
}

function renderCurrent() {
  ensureCurrentQuestion();
  const question = currentQuestion();
  const list = filteredQuestions();
  const isEmpty = !question;
  elements.emptyState.classList.toggle("hidden", !isEmpty);
  elements.reviewContent.classList.toggle("hidden", isEmpty);
  if (isEmpty) {
    elements.questionMeta.textContent = "无匹配结果";
    elements.questionTitle.textContent = "请调整筛选条件";
    return;
  }

  state.currentId = question.id;
  const index = list.findIndex((item) => item.id === question.id);
  elements.questionMeta.textContent = `第 ${question.number} 题 · 原卷第 ${question.sourcePage} 页 · ${question.score} 分`;
  elements.questionTitle.textContent = question.type || "读图题";
  elements.groupPrompt.textContent = question.groupPrompt || "";
  elements.groupPrompt.classList.toggle("hidden", !question.groupPrompt);
  elements.questionStem.textContent = question.stem;
  elements.questionAnswer.textContent = question.answer || "尚未录入";
  elements.prevButton.disabled = index <= 0;
  elements.nextButton.disabled = index >= list.length - 1;
  renderOptions(question);
  renderCleanedImages(question);
  renderSourceReviews(question);
  renderDecision(question);
  renderQuestionList();
}

function moveQuestion(offset) {
  const list = filteredQuestions();
  const index = list.findIndex((question) => question.id === state.currentId);
  const next = list[index + offset];
  if (next) {
    state.currentId = next.id;
    renderCurrent();
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
}

function setStatus(status) {
  const question = currentQuestion();
  if (!question) return;
  const key = recordKey(question);
  state.records[key] = { ...getRecord(question), status };
  saveRecords();
  renderCurrent();
}

async function init() {
  let manifest = window.GEOGRAPHY_REVIEW_MANIFEST;
  let manifestSource = "embedded";
  if (!manifest) {
    const response = await fetch(MANIFEST_URL, { cache: "no-store" });
    if (!response.ok) throw new Error("核对清单加载失败");
    manifest = await response.json();
    manifestSource = "network";
  }
  document.documentElement.dataset.manifestSource = manifestSource;
  state.banks = manifest.banks || [];
  state.bankId = state.banks[0]?.id || "";
  renderBankOptions();
  renderCurrent();
}

elements.bankSelect.addEventListener("change", (event) => {
  state.bankId = event.target.value;
  state.currentId = "";
  renderCurrent();
});

elements.searchInput.addEventListener("input", (event) => {
  state.search = event.target.value;
  renderCurrent();
});

document.querySelectorAll(".status-filter").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".status-filter").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    state.filter = button.dataset.filter;
    renderCurrent();
  });
});

elements.questionList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-id]");
  if (!button) return;
  state.currentId = button.dataset.id;
  renderCurrent();
  window.scrollTo({ top: 0, behavior: "smooth" });
});

document.querySelectorAll(".decision-button").forEach((button) => {
  button.addEventListener("click", () => setStatus(button.dataset.status));
});

elements.reviewNotes.addEventListener("input", () => {
  const question = currentQuestion();
  if (!question) return;
  const key = recordKey(question);
  state.records[key] = { ...getRecord(question), notes: elements.reviewNotes.value };
  saveRecords();
});

elements.prevButton.addEventListener("click", () => moveQuestion(-1));
elements.nextButton.addEventListener("click", () => moveQuestion(1));
elements.closeDialog.addEventListener("click", () => elements.pageDialog.close());
elements.pageDialog.addEventListener("click", (event) => {
  if (event.target === elements.pageDialog) elements.pageDialog.close();
});

init().catch((error) => {
  elements.questionMeta.textContent = "加载失败";
  elements.questionTitle.textContent = error.message;
  elements.emptyState.classList.remove("hidden");
  elements.reviewContent.classList.add("hidden");
});
