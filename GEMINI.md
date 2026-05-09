# EcoScan AI: Label Intelligence

## Project Overview
EcoScan AI is a smart Telegram assistant designed to decode complex food labels using Computer Vision and AI. It provides consumers with instant, health-focused clarity and environmental impact assessments during their grocery shopping.

## Core Features
- **Instant Photographic Capture:** Users send a photo of a food label via Telegram.
- **AI-Powered OCR & Analysis:** Utilizes Gemini 3.1 (Flash/Pro) to extract raw data and cross-reference ingredients against nutritional science.
- **Safety & Health Scoring:** Generates safety scores (1-10) and health warnings directly within the Gemini 3.1 context.
- **Environmental Impact:** Detects packaging materials and provides eco-tips using Gemini's multimodal capabilities.
- **Interactive Exploration:** Suggests alternatives and allows deep dives into specific ingredients.

## Technical Architecture
- **Interface:** Telegram Bot.
- **Orchestration:** Python.
- **AI Engine:** Google Gemini 3.1.
- **Output:** Curated UI messages in Telegram with safety scores, warnings, and eco-tips.

## Tech Stack
- **Language:** Python 3.12+
- **Libraries:** `python-telegram-bot`, `google-genai`, `python-dotenv`.
- **Environment Management:** `.env` for API keys (TELEGRAM_TOKEN, GEMINI_API_KEY).

## Development Guidelines
- Follow a modular approach: separate modules for Telegram bot handling, OCR, and AI analysis.
- Ensure robust error handling for image processing and API calls.
- Prioritize clear, concise, and visually appealing Telegram responses (using emojis and formatting).
