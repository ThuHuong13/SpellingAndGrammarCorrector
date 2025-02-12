FROM python:3.10-slim

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
