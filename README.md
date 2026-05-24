# 初中会考地理刷题题库

这是从《海口市2025年初中学业水平考试地理模拟试题（一）》扫描试卷整理出的题库初稿，并带有一个纯前端刷题页面。

## 内容

- `index.html`：刷题页面入口。
- `styles.css`：页面样式。
- `app.js`：刷题交互逻辑。
- `geography_bank/haikou_2025_geography_mock1_question_bank.json`：程序导入用题库。
- `geography_bank/haikou_2025_geography_mock1_question_bank.csv`：表格校对用题库。
- `geography_bank/haikou_2025_geography_mock1_question_bank.md`：人工预览版。
- `geography_bank/question_images/`：题目关联图表图片。
- `geography_bank/question_images_contact_sheet.jpg`：图片总览。

## 本地预览

```bash
python3 -m http.server 8080
```

然后打开：

```text
http://localhost:8080
```

## GitHub Pages

仓库推送到 GitHub 后，在仓库页面进入：

```text
Settings → Pages → Build and deployment → Source: Deploy from a branch
```

选择：

```text
Branch: main
Folder: /root
```

保存后即可通过 GitHub Pages 访问刷题页面。

## 说明

- 原试卷未包含答案页，题库中的 `answer` 字段暂为空。
- 当前刷题页面支持学生自评正确/错误；以后补入答案后，可自动按答案判分。
- 图片路径为相对路径，适合直接导入刷题系统。
- 若用于正式教学或商业系统，请确认试卷版权与使用授权。
