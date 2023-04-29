FROM python:3.11

WORKDIR /app

RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false
RUN make install


EXPOSE 8000

CMD ["make", "start"]