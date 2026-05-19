import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from gemini_engine import analyze_label

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming images from users."""
    user = update.effective_user
    message = update.message
    
    if not message.photo:
        return

    await message.reply_text(f"Analyzing your food label, {user.first_name}... 🔍")

    # Get the largest photo
    photo_file = await message.photo[-1].get_file()
    
    # Save photo locally
    os.makedirs("temp", exist_ok=True)
    photo_path = f"temp/{photo_file.file_id}.jpg"
    await photo_file.download_to_drive(photo_path)

    try:
        # Process with Gemini
        report = analyze_label(photo_path)
        
        # Telegram has a 4096 character limit per message.
        # We split the report if it's too long.
        max_length = 4096
        if len(report) <= max_length:
            await message.reply_text(report)
        else:
            chunks = []
            while len(report) > max_length:
                # Find the last newline within the limit to avoid breaking formatting
                split_index = report.rfind('\n', 0, max_length)
                if split_index == -1: # No newline found, just split at max_length
                    split_index = max_length
                
                chunks.append(report[:split_index])
                report = report[split_index:].lstrip()
            
            if report:
                chunks.append(report)
            
            for chunk in chunks:
                await message.reply_text(chunk)
                
    except Exception as e:
        logging.error(f"Error analyzing label: {e}")
        await message.reply_text("Sorry, I encountered an error while analyzing the image. Please try again with a clearer photo.")
    finally:
        # Clean up
        if os.path.exists(photo_path):
            os.remove(photo_path)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Welcome to EcoScan AI, {user.first_name}! 🥗\n\n"
        "Send me a clear photo of any food label, and I'll use Google Gemini 3.1 to decode its ingredients, "
        "safety, and environmental impact."
    )

if __name__ == '__main__':
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("Error: TELEGRAM_TOKEN not found in .env file.")
    else:
        application = ApplicationBuilder().token(token).build()
        
        # Handlers
        start_handler = MessageHandler(filters.COMMAND & filters.Regex('^/start$'), start)
        image_handler = MessageHandler(filters.PHOTO, handle_image)
        
        application.add_handler(start_handler)
        application.add_handler(image_handler)
        
        print("EcoScan AI Bot (Gemini 3.1 Edition) is starting...")
        application.run_polling()
