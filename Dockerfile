FROM python:3.12-slim

WORKDIR /app

# moviebox-api's own docs specify installing it with --no-deps, then
# manually installing this exact dependency set (including throttlebuster,
# which isn't pulled in by default resolution but may matter for the
# more heavily-protected download-resolution endpoint specifically).
RUN pip install --no-cache-dir moviebox-api==0.5.4 --no-deps && \
    pip install --no-cache-dir "pydantic==2.9.2" rich click beautifulsoup4 httpx throttlebuster

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
