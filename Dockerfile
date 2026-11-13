FROM python:3.13-slim

WORKDIR /app

COPY app.py status.txt ./

USER 10001:10001

EXPOSE 8000

HEALTHCHECK --interval=10s \
  --timeout=3s \
  --start-period=5s \
  --retries=3 \
  CMD python -c \
  "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/health', timeout=2).read()" \
  || exit 1

CMD ["python", "app.py"]
