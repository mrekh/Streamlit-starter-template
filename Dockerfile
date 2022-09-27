FROM python:3.9.10
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
CMD ["streamlit", "run", "streamlit_app.py"]
EXPOSE 8501