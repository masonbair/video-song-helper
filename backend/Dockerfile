# Dockerfile
FROM mcr.microsoft.com/playwright:focal

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Install playwright browsers
RUN playwright install

# Copy your application
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]