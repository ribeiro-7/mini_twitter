FROM python:3.13-alpine

RUN apk add --no-cache gcc musl-dev libpq postgresql-dev

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]