FROM python:3.12-slim
WORKDIR /app

COPY pyproject.toml README.md .

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev --no-interaction --no-root

# 复制源码
COPY src ./src

# ← 新增：把 src 目录加入模块搜索路径
ENV PYTHONPATH="/app/src"

EXPOSE 8080
CMD ["uvicorn", "hybrid_scheduler.main:app", "--host", "0.0.0.0", "--port", "8080"]
