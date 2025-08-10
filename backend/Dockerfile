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

ENV ms_token="chCOfEp6uVitgiLLrA9_nVDDNay_cD51gI6fkg1LvFlPmQghTjgUOWrDZZZ1ev3odzdwFIqT6RHcciqTc-ucsB9_5f7dgjQZPIdtSktEZFTHw5kTJayE0xtVKJ_gb8w8_obJUGUGYDQ="
# USER pwuser

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]