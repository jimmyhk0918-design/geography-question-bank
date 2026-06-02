# 一本地理生地会考预测卷题库

本目录由扫描试卷和答案页整理生成，适合导入地理刷题系统。

## 文件

- `yiben_geography_prediction_2026_question_bank.json`：推荐用于程序导入的结构化题库。
- `yiben_geography_prediction_2026_question_bank.csv`：便于表格校对。
- `yiben_geography_prediction_2026_question_bank.md`：便于人工预览。
- `question_images/`：读图题、表格题的高清切片。

## 说明

- 本卷共整理 30 题：25 道选择题、5 道非选择题。
- 选择题答案已按答案页逐一对应。
- 非选择题保留参考答案要点，适合刷题后自评或教师批改。

## 重新生成

```bash
python3 geography_bank/yiben_geography_prediction_2026/build_question_bank.py
```
