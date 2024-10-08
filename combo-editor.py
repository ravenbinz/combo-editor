from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Document
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import logging

# Enable logging for easier debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

combo_data = []

# Function to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to Combo Editor Bot!\nPlease upload your combo file to start editing.")

# Function to handle the uploaded file and display inline buttons
def handle_file(update: Update, context: CallbackContext) -> None:
    document: Document = update.message.document

    if document.mime_type == 'text/plain':
        file = document.get_file()
        content = file.download_as_bytearray().decode('utf-8')

        global combo_data
        combo_data = content.splitlines()

        # Show inline keyboard options after uploading the combo
        keyboard = [
            [InlineKeyboardButton("Remove Captures", callback_data='remove_captures')],
            [InlineKeyboardButton("Remove URLs", callback_data='remove_urls')],
            [InlineKeyboardButton("Remove Duplicates", callback_data='remove_duplicates')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(
            "Combo file uploaded successfully! Select what you want to remove:",
            reply_markup=reply_markup
        )
    else:
        update.message.reply_text("Please upload a valid .txt file.")

# Function to handle the callback queries (button clicks)
def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()  # Acknowledge the button press

    if query.data == 'remove_captures':
        remove_captures(query, context)
    elif query.data == 'remove_urls':
        remove_urls(query, context)
    elif query.data == 'remove_duplicates':
        remove_duplicates(query, context)

# Function to remove captures (text after '|')
def remove_captures(update: Update, context: CallbackContext) -> None:
    global combo_data
    if combo_data:
        # Remove everything after '|'
        cleaned_combo = [line.split('|')[0].strip() for line in combo_data]

        # Save the cleaned data
        with open("removed_cap.txt", "w") as f:
            f.write("\n".join(cleaned_combo))

        update.message.reply_document(open("removed_cap.txt", "rb"), filename="removed_cap.txt")
        update.message.reply_text("Captures removed and saved as 'removed_cap.txt'.")
    else:
        update.message.reply_text("Please upload a combo file first.")

# Function to remove URLs (remove 'url:' from 'url:email:pass')
def remove_urls(update: Update, context: CallbackContext) -> None:
    global combo_data
    if combo_data:
        # Remove URLs
        cleaned_combo = [":".join(line.split(":")[1:]).strip() for line in combo_data if line.count(':') >= 2]

        # Save the cleaned data
        with open("removed_url.txt", "w") as f:
            f.write("\n".join(cleaned_combo))

        update.message.reply_document(open("removed_url.txt", "rb"), filename="removed_url.txt")
        update.message.reply_text("URLs removed and saved as 'removed_url.txt'.")
    else:
        update.message.reply_text("Please upload a combo file first.")

# Function to remove duplicate accounts
def remove_duplicates(update: Update, context: CallbackContext) -> None:
    global combo_data
    if combo_data:
        # Remove duplicates using a set
        cleaned_combo = list(set(combo_data))

        # Save the cleaned data
        with open("removed_duplicates.txt", "w") as f:
            f.write("\n".join(cleaned_combo))

        update.message.reply_document(open("removed_duplicates.txt", "rb"), filename="removed_duplicates.txt")
        update.message.reply_text("Duplicates removed and saved as 'removed_duplicates.txt'.")
    else:
        update.message.reply_text("Please upload a combo file first.")

# Main function to run the bot
def main() -> None:
    # Set your Telegram Bot Token
    updater = Updater("8188996092:AAH0UMcil8hmj8Aw_x-hWkEy5SoXvMhnsPQ", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, handle_file))
    
    # Handle button clicks (Inline keyboard)
    dp.add_handler(CallbackQueryHandler(button_click))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
