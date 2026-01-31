# Traffic Violation Detection System

An AI-powered system for detecting traffic violations (specifically helmetless riding) and extracting number plates from video or image inputs.

## 🚀 Features

- **Object Detection**: Detects persons, motorcycles, and helmets using YOLO (Ultralytics).
- **Violation Logic**: Identifies riders without helmets.
- **OCR Integration**: Extracts license plate text using EasyOCR.
- **Cloud Storage**: Uploads violation evidence to Supabase Storage.
- **Database**: logs violation details to Supabase Database.
- **Web Interface**: User-friendly React frontend for file uploads and result viewing.

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **ML/AI**: PyTorch, Ultralytics YOLOv8, EasyOCR, OpenCV
- **Database/Storage**: Supabase
- **Environment**: Python 3.x

### Frontend
- **Framework**: React.js
- **Build Tool**: Vite
- **Styling**: CSS Modules / Vanilla CSS

## 📋 Prerequisites

- **Python**: 3.8+
- **Node.js**: 16+ (and npm)
- **Supabase Account**: For database and storage keys.

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/anwithpulijala/Traffic-Violation.git
cd Traffic-Violation
```

### 2. Backend Setup
Navigate to the backend directory and set up the Python environment.

```bash
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Environment Variables**:
Create a `.env` file in the `backend/` directory with your Supabase credentials:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_role_key
```

### 3. Frontend Setup
Open a new terminal, navigate to the frontend directory, and install dependencies.

```bash
cd frontend

# Install dependencies
npm install
```

## ▶️ Running the Application

### Start the Backend
From the `backend/` directory (with venv activated):
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

### Start the Frontend
From the `frontend/` directory:
```bash
npm run dev
```
The application will run at `http://localhost:5173`.

## 📂 Project Structure

```
Traffic-Violation/
├── backend/
│   ├── app/                # FastAPI application code
│   ├── models/             # YOLO model files (.pt)
│   ├── requirements.txt    # Python dependencies
│   └── ...
├── frontend/
│   ├── src/                # React source code
│   ├── package.json        # Node dependencies
│   └── ...
└── README.md
```
