FROM python:3.12-slim

# making directory of app
WORKDIR /mdz_ausschreibung_llm 
COPY . .

# pip install packages
RUN pip install -r requirements.txt

# exposing default port for streamlit
EXPOSE 8501

# entrypoint to launch app when container is run
ENTRYPOINT ["python", "-m", "streamlit", "run", "main.py"]