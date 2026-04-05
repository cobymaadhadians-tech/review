# Literature Manager MVP

一个最小可运行的文献管理系统，支持：
- 文献元数据 CRUD
- 标题/作者/关键词/DOI 搜索
- 单文件 PDF 上传并存储到 `data/pdfs/`
- 批量 PDF 导入并自动创建文献记录
- 列表中直接打开 PDF

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./run.sh
```

访问：`http://127.0.0.1:8000/`

## 数据与存储

- SQLite: `data/literature.db`
- PDF: `data/pdfs/`

## 自动解析策略（MVP）

批量导入时：
1. 默认从文件名提取标题（去除 `.pdf`，并尝试提取年份）
2. 作者先留空
3. DOI 为可选（可在批量导入时统一填写）
4. 若环境已安装 `pypdf`，会尝试从 PDF 元信息/第一页文本提取标题（失败自动回退到文件名）

## API

- `GET /api/literatures?query=...`
- `GET /api/literatures/{id}`
- `POST /api/literatures` (multipart/form-data, 可带 `pdf`)
- `POST /api/literatures/batch-import` (multipart/form-data, `files` 支持多个 PDF, `doi` 可选)
- `PUT /api/literatures/{id}`
- `DELETE /api/literatures/{id}`
