# 海口市2025年地理模拟试题（一）题库

本目录由扫描试卷提取生成，适合导入刷题系统做题库初稿。

## 文件

- `haikou_2025_geography_mock1_question_bank.json`：推荐用于程序导入的结构化题库。
- `haikou_2025_geography_mock1_question_bank.csv`：便于表格校对和人工补答案。
- `haikou_2025_geography_mock1_question_bank.md`：便于人工预览。
- `question_images/`：读图题、表格题的高清切片。
- `pages/`：原PDF逐页渲染图，用于复核。
- `ocr/`：OCR原始文本，仅用于追溯，不建议直接入库。

## 题目字段

- `id`：题目唯一编号。
- `number`：原卷题号。
- `type`：`single_choice` 或 `non_choice`。
- `score`：分值。
- `source_page`：来源页码。
- `group_prompt`：题组材料或导语。
- `stem`：题干。
- `options`：选择题选项。
- `answer`：答案。原PDF未含答案页，当前留空。
- `images`：相对本目录的关联图片路径。

## 导入建议

1. 先导入 `json`，保持题干、选项和图片关系。
2. 后台题库表建议保存 `source_page`、`source_file`、`images`，方便追溯。
3. 答案和解析建议单独补录，不要直接由OCR推断。
4. 如用于正式教学或商业系统，请确认试卷版权与使用授权。
