# Literature Manager MVP

一个最小可运行的文献管理系统，支持：
- 文献元数据 CRUD
- 标题/作者/关键词/DOI 搜索
- PDF 上传并存储到 `data/pdfs/`
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

## API

- `GET /api/literatures?query=...`
- `GET /api/literatures/{id}`
- `POST /api/literatures` (multipart/form-data, 可带 `pdf`)
- `PUT /api/literatures/{id}`
- `DELETE /api/literatures/{id}`
