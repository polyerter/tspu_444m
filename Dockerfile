FROM python:3.10-alpine
WORKDIR /code

COPY req.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 80

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]