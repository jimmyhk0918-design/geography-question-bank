# 初中会考地理刷题题库

这是从《海口市2025年初中学业水平考试地理模拟试题（一）》扫描试卷和答案卷整理出的题库，并带有一个纯前端刷题页面。

## 内容

- `index.html`：刷题页面入口。
- `styles.css`：页面样式。
- `app.js`：刷题交互逻辑。
- `cloud-sync.js`：学生账号与云端答题记录同步。
- `supabase-config.js`：Supabase 项目公开配置。
- `supabase/schema.sql`：云端答题记录数据表与访问权限。
- `geography_bank/question_banks.json`：刷题页面加载的题库清单。
- `geography_bank/haikou_2025_geography_mock1_question_bank.json`：程序导入用题库。
- `geography_bank/hainan_2024_exam/hainan_2024_geography_exam_question_bank.json`：2024年海南省中考地理真题题库。
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

## 跨设备保存答题记录

网页支持使用学生邮箱账号登录。学生登录后，每次选择答案、提交、自评或清除记录都会先保存在当前设备，并自动同步到 Supabase 数据库。以后在另一台电脑使用同一账号登录，会恢复之前各套题的答题进度。

未登录时仍可刷题，但记录只保存在当前浏览器。

### 1. 创建 Supabase 项目

在 Supabase 创建一个项目，然后进入 SQL Editor，执行：

```text
supabase/schema.sql
```

该脚本会创建 `student_progress` 表并启用行级安全策略，每个学生只能访问自己的答题记录。

### 2. 配置学生邮箱登录

在 Supabase 的 Authentication 设置中启用 Email 登录。课堂使用时，可按需要关闭邮箱确认；若保留邮箱确认，学生注册后需要先点击验证邮件才能登录。

在 `Authentication → URL Configuration` 中，将 `Site URL` 设置为：

```text
https://jimmyhk0918-design.github.io/geography-question-bank/
```

这样启用邮箱确认后，验证邮件才能正确返回刷题网页。

### 3. 填写网页配置

在 Supabase 项目设置的 API 页面复制 Project URL 和公开的 anon/publishable key，填入：

```javascript
// supabase-config.js
window.GEO_CLOUD_CONFIG = {
  supabaseUrl: "https://你的项目.supabase.co",
  supabaseAnonKey: "你的公开 anon 或 publishable key",
};
```

`anon/publishable key` 可以放在前端网页中，数据安全由 `supabase/schema.sql` 中的行级安全策略保证。不要把 `service_role` 密钥写入本项目。

### 4. 重新部署

提交并推送 `index.html`、`app.js`、`cloud-sync.js`、`supabase-config.js`、`supabase/schema.sql` 和 `styles.css`。GitHub Pages 更新后，左侧题库选择器下方会出现“学生账号”登录区域。

旧版保存在本机的答题记录，会在该学生第一次登录时自动合并到他的云端账号。

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

- 选择题已录入答案，可自动判分。
- 非选择题已录入参考答案，提交后可对照参考答案自评正确/错误。
- 2024年海南省中考地理真题当前只提供试题，答案字段暂为空；页面会按自评模式记录正确/错误。
- 图片路径为相对路径，适合直接导入刷题系统。
- 若用于正式教学或商业系统，请确认试卷版权与使用授权。
