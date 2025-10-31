#!/bin/bash
# Run frontend dev server in new Alacritty window (non-blocking)
(alacritty -e bash -c "cd frontend && npm run dev" &)

# Run backend server in new Alacritty window (non-blocking)
(alacritty -e bash -c "cd backend && source ./.venv/bin/activate && python main.py" &)

# Script continues immediately
echo "Successfully Launched Application"
