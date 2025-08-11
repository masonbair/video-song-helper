FROM python:3.12-bookworm

RUN apt update && apt install -y \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# # Create the pwuser user and home directory
# RUN useradd -m pwuser
WORKDIR /app

# Install Python dependencies as root
COPY requirements.txt .
RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
RUN /app/venv/bin/pip install --upgrade pip
RUN /app/venv/bin/pip install -r requirements.txt

RUN python -m playwright install-deps webkit
RUN python -m playwright install webkit

ENV ms_token="IVyWCKuAKYABY6WLR64Xi-worKGJRvJB2KMtMw-qAdEuXZgb7YOV6rLkaipLAJKA1pSURMebyYbc-lsVmz6uoT7ot2qY7nC8EOdfbzVc96lsETn8lnoBVu0ah2dYXa9-V7ov3MgABGF2kdyHcZW-"
# USER pwuser

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
