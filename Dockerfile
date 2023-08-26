FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD [ "python", "-m", "flask", "run", "-h", "0.0.0.0", "-p", "5001"]
