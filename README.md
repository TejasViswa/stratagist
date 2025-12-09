# StrataGist

A modern task extraction and management web application. Journal your thoughts and let AI automatically extract actionable tasks.

![StrataGist](https://via.placeholder.com/800x400/0A0F23/FF00FF?text=StrataGist)

## Features

- 📝 **Journal your thoughts** - Record your ideas, plans, and notes
- 🤖 **AI Task Extraction** - Automatically extract tasks from your thoughts using AI or rule-based analysis
- ✅ **Task Management** - View, edit, complete, and organize your tasks
- 📅 **Calendar View** - Browse through months and dates
- 🌙 **Beautiful Dark Theme** - Neon-accented dark UI for comfortable viewing

## Tech Stack

### Frontend
- **Next.js 16** - React framework with App Router
- **React 19** - Latest React with concurrent features
- **Tailwind CSS 4** - Utility-first CSS framework
- **Framer Motion** - Smooth animations
- **Lucide React** - Beautiful icons
- **date-fns** - Date formatting utilities

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **OpenAI API** (optional) - AI-powered task extraction
- **File-based storage** - JSON file storage for simplicity

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. (Optional) Set up OpenAI for AI-powered task extraction:
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```
   
   If not set, the app will use rule-based task extraction.

5. Start the backend server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the web directory:
   ```bash
   cd web
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
stratagist/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI routes
│   │   ├── models.py         # Pydantic models
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── storage.py    # JSON file storage
│   │       └── ai_extraction.py  # Task extraction logic
│   ├── data/                 # JSON data files (auto-created)
│   └── requirements.txt
│
└── web/
    ├── app/
    │   ├── components/       # React components
    │   │   ├── BottomNav.tsx
    │   │   ├── CalendarScreen.tsx
    │   │   ├── InputModal.tsx
    │   │   ├── JournalScreen.tsx
    │   │   ├── LandingPage.tsx
    │   │   ├── TaskExtractionDialog.tsx
    │   │   └── TasksScreen.tsx
    │   ├── lib/
    │   │   └── api.ts        # API client
    │   ├── globals.css       # Global styles
    │   ├── layout.tsx        # Root layout
    │   └── page.tsx          # Main page
    └── package.json
```

## API Endpoints

### Thoughts

- `GET /api/thoughts` - Get all thoughts
- `GET /api/thoughts/dates` - Get dates with thoughts
- `GET /api/thoughts/date/{date}` - Get thoughts for a specific date
- `POST /api/thoughts` - Create a thought (with task extraction)
- `PUT /api/thoughts/{id}` - Update a thought
- `DELETE /api/thoughts/{id}` - Delete a thought
- `DELETE /api/thoughts/date/{date}` - Clear thoughts for a date

### Tasks

- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a task
- `POST /api/tasks/bulk` - Create multiple tasks
- `PUT /api/tasks/{id}` - Update a task
- `PATCH /api/tasks/{id}/toggle` - Toggle task completion
- `DELETE /api/tasks/{id}` - Delete a task

## Environment Variables

### Backend
| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for AI task extraction | No |

### Frontend
| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |

## Color Theme

The app uses a dark neon theme:

- **Background Primary**: `#0A0F23`
- **Background Secondary**: `#1A1F33`
- **Accent Pink**: `#FF00FF`
- **Accent Purple**: `#9F00FF`

## License

MIT License - feel free to use this project for learning or personal use.

## Credits

Inspired by the StrataGist Flutter app, recreated as a web application with React and Python.

