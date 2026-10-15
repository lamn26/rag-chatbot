
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY FE/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY FE/ ./FE/

EXPOSE 8501

CMD ["streamlit", "run", "FE/app.py", "--server.address=0.0.0.0", "--server.port=8501"]
