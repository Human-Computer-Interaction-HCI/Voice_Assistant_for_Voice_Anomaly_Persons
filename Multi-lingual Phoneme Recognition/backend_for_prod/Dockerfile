FROM python:3.11
WORKDIR /app
COPY requirements.txt requirements
RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt
COPY entrypoint.sh entrypoint.sh
COPY src src
CMD [ "./entrypoint.sh" ]