# Song Recommendation API

A FastAPI backend application that provides an API for managing song recommendations with TikTok integration.

## Features

- Fetch song recommendations from TikTok
- Add new song recommendations
- CORS support
- Environment configuration

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

To start the development server:

```bash
uvicorn src.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. 
Interactive API documentation is available at `http://localhost:8000/docs`.

## API Endpoints

- GET `/api/test` - Test endpoint
- GET `/api/recommendations` - Get song recommendations
- POST `/api/recommendations` - Add a new recommendation

## Directory Structure

```
backend/
├── src/
│   ├── main.py           # Main application entry point
│   ├── models/           # Pydantic models
│   └── services/         # Business logic
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
└── README.md           # Documentation
```

## License

This project is licensed under the MIT License.