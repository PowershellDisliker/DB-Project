#!/bin/bash
# Run frontend dev server in new Alacritty window (non-blocking)
(alacritty -e bash -c "cd frontend && npm run dev" &)

# Run backend server in new Alacritty window (non-blocking)
(alacritty -e bash -c "source ./backend-venv/bin/activate && fastapi dev ./backend/app/app.py" &)

# Script continues immediately
echo "Successfully Launched Application"