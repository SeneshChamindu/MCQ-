# Senesh A/L MCQ Bot

## Features
- Sinhala and English language menu
- MCQ Target and Past Paper MCQ modes
- Subject selection and multiple-choice answers
- Per-user score for the current bot session
- Flask health-check endpoint for Render

## Deploy on Render
1. Upload these files to a GitHub repository.
2. In Render, create a **Web Service** and connect the repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `python main.py`
5. In Render → Environment, add `TELEGRAM_BOT_TOKEN` with your *newly rotated* BotFather token.
6. Deploy and open your Telegram bot, then send `/start`.

## Commands
- `/start` — menu
- `/mcq` — choose subject and answer a question
- `/target` — MCQ Target mode
- `/pastpaper` — Past Paper MCQ mode
- `/subjects` — choose subject
- `/language` — change language
- `/score` — see current session score
- `/help` — commands

## Important notes
- Never commit your bot token to GitHub or share it in chats.
- The included questions are starter examples, not a complete verified A/L or official past-paper database. Add questions you have permission to use to `QUESTIONS` in `main.py`.
- This starter version uses Telegram polling; keep only one deployed instance running with this token.
