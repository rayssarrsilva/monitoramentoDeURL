FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

WORKDIR /code/monitoria  

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
