FROM python:3.9-slim

WORKDIR /app

COPY requirements_app.txt requirements.txt
RUN pip install -r requirements.txt

COPY validator/ validator/
COPY dataset/ dataset/
COPY outputs/ outputs/

EXPOSE 8501

CMD ["streamlit", "run", "validator/app.py", "--server.port=8501", "--server.address=0.0.0.0"]