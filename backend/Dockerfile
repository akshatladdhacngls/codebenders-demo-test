FROM python:3.10
WORKDIR /app
RUN python -m venv .venv
RUN /bin/bash -c "source .venv/bin/activate"
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
