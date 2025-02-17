# Image Generation Project

This project is a full-stack application for image generation using Vue 3 and Flask.

## Project Structure
```
imagegeneration/
├── frontend/         # Vue 3 frontend
├── backend/         # Flask backend
├── ARCHITECTURE.pdf
└── NEWARCHITECTURE_FOCUSED.pdf
```

## Frontend Setup
1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

## Backend Setup
1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
- Copy `.env.example` to `.env`
- Update the values in `.env` with your credentials

5. Run the development server:
```bash
flask run
```

## Technologies Used
- Frontend:
  - Vue 3
  - Tailwind CSS
  - Pinia (State Management)
  - FontAwesome
- Backend:
  - Flask
  - SQLAlchemy
  - OpenAI API
