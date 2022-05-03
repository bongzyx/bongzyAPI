FROM python:3.9

WORKDIR /api

ENV FLASK_ENV=development

COPY ./requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 4656

CMD [ "python", "api/run.py" ]