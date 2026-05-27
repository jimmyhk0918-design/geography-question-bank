const BANK_INDEX_URL = "./geography_bank/question_banks.json";
const SELECTED_BANK_KEY = "geo-question-bank-selected-bank-v1";
const FALLBACK_BANK = {
  id: "haikou_2025_mock1",
  title: "海口市2025年初中学业水平考试地理模拟试题（一）",
  url: "./geography_bank/haikou_2025_geography_mock1_question_bank.json",
  basePath: "./geography_bank",
};

const state = {
  source: null,
  banks: [],
  currentBank: null,
  questions: [],
  currentIndex: 0,
  filter: "all",
  search: "",
  progress: {},
};

const els = {
  bankTitle: document.querySelector("#bankTitle"),
  bankSelect: document.querySelector("#bankSelect"),
  attemptedCount: document.querySelector("#attemptedCount"),
  accuracyRate: document.querySelector("#accuracyRate"),
  wrongCount: document.querySelector("#wrongCount"),
  totalCount: document.querySelector("#totalCount"),
  questionList: document.querySelector("#questionList"),
  searchInput: document.querySelector("#searchInput"),
  questionMeta: document.querySelector("#questionMeta"),
  questionHeading: document.querySelector("#questionHeading"),
  groupPrompt: document.querySelector("#groupPrompt"),
  imageArea: document.querySelector("#imageArea"),
  questionStem: document.querySelector("#questionStem"),
  answerForm: document.querySelector("#answerForm"),
  resultPanel: document.querySelector("#resultPanel"),
  submitButton: document.querySelector("#submitButton"),
  markCorrectButton: document.querySelector("#markCorrectButton"),
  markWrongButton: document.querySelector("#markWrongButton"),
  clearCurrentButton: document.querySelector("#clearCurrentButton"),
  prevButton: document.querySelector("#prevButton"),
  nextButton: document.querySelector("#nextButton"),
  randomButton: document.querySelector("#randomButton"),
  imageDialog: document.querySelector("#imageDialog"),
  dialogImage: document.querySelector("#dialogImage"),
  closeImageDialog: document.querySelector("#closeImageDialog"),
};

function progressKey(bankId) {
  return `geo-question-bank-progress-v1:${bankId || "default"}`;
}

function loadProgress(bankId) {
  try {
    return JSON.parse(localStorage.getItem(progressKey(bankId))) || {};
  } catch {
    return {};
  }
}

function saveProgress() {
  localStorage.setItem(progressKey(state.currentBank?.id), JSON.stringify(state.progress));
}

function getRecord(questionId) {
  if (!state.progress[questionId]) {
    state.progress[questionId] = {
      selected: "",
      textAnswer: "",
      submitted: false,
      isCorrect: null,
      attempts: 0,
      updatedAt: "",
    };
  }
  return state.progress[questionId];
}

function normalizeText(value) {
  return String(value || "").toLowerCase().trim();
}

function hasAnswer(question) {
  return Boolean(question.answer && String(question.answer).trim());
}

function isChoice(question) {
  return question.type === "single_choice";
}

function isQuestionVisible(question) {
  const record = getRecord(question.id);
  const text = [
    question.number,
    question.group_prompt,
    question.stem,
    Object.values(question.options || {}).join(" "),
  ]
    .map(normalizeText)
    .join(" ");
  const matchesSearch = !state.search || text.includes(normalizeText(state.search));

  if (!matchesSearch) return false;
  if (state.filter === "choice") return isChoice(question);
  if (state.filter === "non_choice") return question.type === "non_choice";
  if (state.filter === "image") return (question.images || []).length > 0;
  if (state.filter === "wrong") return record.submitted && record.isCorrect === false;
  if (state.filter === "unanswered") return !record.submitted;
  return true;
}

function visibleQuestions() {
  return state.questions.filter(isQuestionVisible);
}

function findVisibleIndex() {
  const visible = visibleQuestions();
  const current = state.questions[state.currentIndex];
  const match = visible.findIndex((question) => question.id === current?.id);
  return { visible, match };
}

function setCurrentByQuestionId(questionId) {
  const index = state.questions.findIndex((question) => question.id === questionId);
  if (index >= 0) {
    state.currentIndex = index;
    render();
  }
}

function currentQuestion() {
  return state.questions[state.currentIndex];
}

function updateStats() {
  const records = state.questions.map((question) => getRecord(question.id));
  const submitted = records.filter((record) => record.submitted);
  const graded = submitted.filter((record) => record.isCorrect !== null);
  const correct = graded.filter((record) => record.isCorrect === true);
  const wrong = records.filter((record) => record.submitted && record.isCorrect === false);

  els.attemptedCount.textContent = submitted.length;
  els.totalCount.textContent = state.questions.length;
  els.wrongCount.textContent = wrong.length;
  els.accuracyRate.textContent = graded.length ? `${Math.round((correct.length / graded.length) * 100)}%` : "--";
}

function renderQuestionList() {
  const visible = visibleQuestions();
  els.questionList.innerHTML = "";

  visible.forEach((question) => {
    const record = getRecord(question.id);
    const button = document.createElement("button");
    button.type = "button";
    button.className = "question-jump";
    button.textContent = question.number;
    button.title = `第${question.number}题`;

    if (question.id === currentQuestion()?.id) button.classList.add("active");
    if (record.submitted) button.classList.add("done");
    if (record.submitted && record.isCorrect === false) button.classList.add("wrong");

    button.addEventListener("click", () => setCurrentByQuestionId(question.id));
    els.questionList.append(button);
  });
}

function renderImages(question) {
  els.imageArea.innerHTML = "";
  (question.images || []).forEach((imagePath, index) => {
    const frame = document.createElement("div");
    frame.className = "image-frame";

    const button = document.createElement("button");
    button.type = "button";
    button.title = "查看大图";

    const img = document.createElement("img");
    img.src = `${state.currentBank?.basePath || "./geography_bank"}/${imagePath}`;
    img.alt = `第${question.number}题关联图${index + 1}`;
    button.append(img);

    button.addEventListener("click", () => {
      els.dialogImage.src = img.src;
      els.dialogImage.alt = img.alt;
      els.imageDialog.showModal();
    });

    frame.append(button);
    els.imageArea.append(frame);
  });
}

function renderAnswer(question) {
  const record = getRecord(question.id);
  els.answerForm.innerHTML = "";

  if (isChoice(question)) {
    Object.entries(question.options || {}).forEach(([key, value]) => {
      const label = document.createElement("label");
      label.className = "option-row";
      if (record.selected === key) label.classList.add("selected");

      const input = document.createElement("input");
      input.type = "radio";
      input.name = "answer";
      input.value = key;
      input.checked = record.selected === key;
      input.addEventListener("change", () => {
        record.selected = key;
        record.isCorrect = null;
        saveProgress();
        render();
      });

      const text = document.createElement("div");
      text.className = "option-text";
      text.innerHTML = `<span class="option-label">${key}.</span> ${escapeHtml(value)}`;

      label.append(input, text);
      els.answerForm.append(label);
    });
  } else {
    const textarea = document.createElement("textarea");
    textarea.className = "written-answer";
    textarea.placeholder = "填写作答内容";
    textarea.value = record.textAnswer || "";
    textarea.addEventListener("input", () => {
      record.textAnswer = textarea.value;
      record.isCorrect = null;
      saveProgress();
    });
    els.answerForm.append(textarea);
  }
}

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function answerSummary(question, record) {
  if (isChoice(question)) return record.selected ? `你的选择：${record.selected}` : "未选择";
  return record.textAnswer ? "已填写主观题答案" : "未填写";
}

function renderResult(question) {
  const record = getRecord(question.id);
  els.resultPanel.className = "result-panel hidden";
  els.resultPanel.textContent = "";
  els.markCorrectButton.classList.add("hidden");
  els.markWrongButton.classList.add("hidden");

  if (!record.submitted) return;

  els.resultPanel.classList.remove("hidden");

  if (hasAnswer(question)) {
    const correctAnswer = String(question.answer).trim();

    if (!isChoice(question) && record.isCorrect === null) {
      els.resultPanel.classList.add("pending");
      els.resultPanel.textContent = `${answerSummary(question, record)}。参考答案：${correctAnswer}`;
      els.markCorrectButton.classList.remove("hidden");
      els.markWrongButton.classList.remove("hidden");
      return;
    }

    const isCorrect = record.isCorrect === true;
    els.resultPanel.classList.add(isCorrect ? "correct" : "wrong");
    els.resultPanel.textContent = `${answerSummary(question, record)}。参考答案：${correctAnswer}`;
    return;
  }

  if (record.isCorrect === true) {
    els.resultPanel.classList.add("correct");
    els.resultPanel.textContent = `${answerSummary(question, record)}。已标记为正确。`;
    els.markWrongButton.classList.remove("hidden");
    return;
  }

  if (record.isCorrect === false) {
    els.resultPanel.classList.add("wrong");
    els.resultPanel.textContent = `${answerSummary(question, record)}。已加入错题。`;
    els.markCorrectButton.classList.remove("hidden");
    return;
  }

  els.resultPanel.classList.add("pending");
  els.resultPanel.textContent = `${answerSummary(question, record)}。`;
  els.markCorrectButton.classList.remove("hidden");
  els.markWrongButton.classList.remove("hidden");
}

function renderQuestion() {
  const question = currentQuestion();
  if (!question) {
    els.questionMeta.textContent = "暂无题目";
    els.questionHeading.textContent = "没有匹配题目";
    els.groupPrompt.textContent = "";
    els.imageArea.innerHTML = "";
    els.questionStem.textContent = "请调整筛选或搜索条件。";
    els.answerForm.innerHTML = "";
    els.resultPanel.className = "result-panel hidden";
    els.prevButton.disabled = true;
    els.nextButton.disabled = true;
    return;
  }

  const record = getRecord(question.id);
  els.questionMeta.textContent = `第 ${question.number} 题 · ${question.score} 分 · 第 ${question.source_page} 页`;
  els.questionHeading.textContent = isChoice(question) ? "选择题" : "非选择题";
  els.groupPrompt.textContent = question.group_prompt || "";
  els.questionStem.textContent = question.stem || "";
  els.submitButton.textContent = record.submitted ? "重新提交" : "提交";
  els.prevButton.disabled = state.currentIndex === 0;
  els.nextButton.disabled = state.currentIndex === state.questions.length - 1;

  renderImages(question);
  renderAnswer(question);
  renderResult(question);
}

function render() {
  updateStats();
  renderQuestionList();
  renderQuestion();
}

function renderBankSelect() {
  els.bankSelect.innerHTML = "";
  state.banks.forEach((bank) => {
    const option = document.createElement("option");
    option.value = bank.id;
    option.textContent = bank.title;
    option.selected = bank.id === state.currentBank?.id;
    els.bankSelect.append(option);
  });
}

function submitCurrent() {
  const question = currentQuestion();
  const record = getRecord(question.id);
  const hasResponse = isChoice(question) ? Boolean(record.selected) : Boolean(record.textAnswer?.trim());

  if (!hasResponse) {
    els.resultPanel.className = "result-panel pending";
    els.resultPanel.textContent = isChoice(question) ? "请选择一个选项。" : "请先填写答案。";
    return;
  }

  record.submitted = true;
  record.attempts += 1;
  record.updatedAt = new Date().toISOString();

  if (hasAnswer(question) && isChoice(question)) {
    record.isCorrect = record.selected === String(question.answer).trim();
  } else {
    record.isCorrect = null;
  }

  saveProgress();
  render();
}

function markCurrent(isCorrect) {
  const question = currentQuestion();
  const record = getRecord(question.id);
  record.submitted = true;
  record.isCorrect = isCorrect;
  record.updatedAt = new Date().toISOString();
  saveProgress();
  render();
}

function clearCurrent() {
  const question = currentQuestion();
  delete state.progress[question.id];
  saveProgress();
  render();
}

function move(delta) {
  const nextIndex = Math.min(Math.max(state.currentIndex + delta, 0), state.questions.length - 1);
  state.currentIndex = nextIndex;
  render();
}

function randomQuestion() {
  const visible = visibleQuestions();
  if (!visible.length) return;
  const question = visible[Math.floor(Math.random() * visible.length)];
  setCurrentByQuestionId(question.id);
}

function bindEvents() {
  els.bankSelect.addEventListener("change", async (event) => {
    await loadBank(event.target.value);
  });

  document.querySelectorAll(".filter-button").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".filter-button").forEach((item) => item.classList.remove("active"));
      button.classList.add("active");
      state.filter = button.dataset.filter;
      const { visible, match } = findVisibleIndex();
      if (match === -1 && visible.length) setCurrentByQuestionId(visible[0].id);
      render();
    });
  });

  els.searchInput.addEventListener("input", (event) => {
    state.search = event.target.value;
    const { visible, match } = findVisibleIndex();
    if (match === -1 && visible.length) setCurrentByQuestionId(visible[0].id);
    render();
  });

  els.submitButton.addEventListener("click", submitCurrent);
  els.markCorrectButton.addEventListener("click", () => markCurrent(true));
  els.markWrongButton.addEventListener("click", () => markCurrent(false));
  els.clearCurrentButton.addEventListener("click", clearCurrent);
  els.prevButton.addEventListener("click", () => move(-1));
  els.nextButton.addEventListener("click", () => move(1));
  els.randomButton.addEventListener("click", randomQuestion);
  els.closeImageDialog.addEventListener("click", () => els.imageDialog.close());
}

async function loadBank(bankId) {
  const nextBank = state.banks.find((bank) => bank.id === bankId) || state.banks[0] || FALLBACK_BANK;
  state.currentBank = nextBank;
  state.source = null;
  state.questions = [];
  state.currentIndex = 0;
  state.progress = loadProgress(nextBank.id);
  localStorage.setItem(SELECTED_BANK_KEY, nextBank.id);
  renderBankSelect();

  els.bankTitle.textContent = "题库加载中";
  els.questionHeading.textContent = "加载中";
  els.questionStem.textContent = "";
  els.submitButton.disabled = true;

  const response = await fetch(nextBank.url);
  if (!response.ok) throw new Error(`题库加载失败：${response.status}`);
  const data = await response.json();
  state.source = data.source;
  state.questions = data.questions || [];
  els.bankTitle.textContent = data.source?.title || nextBank.title || "地理题库";
  els.submitButton.disabled = false;
  render();
}

async function init() {
  bindEvents();
  try {
    const bankResponse = await fetch(BANK_INDEX_URL);
    state.banks = bankResponse.ok ? await bankResponse.json() : [FALLBACK_BANK];
    const savedBankId = localStorage.getItem(SELECTED_BANK_KEY);
    await loadBank(savedBankId || state.banks[0]?.id || FALLBACK_BANK.id);
  } catch (error) {
    els.bankTitle.textContent = "题库加载失败";
    els.questionHeading.textContent = "无法读取题库";
    els.questionStem.textContent = error.message;
    els.submitButton.disabled = true;
  }
}

init();
