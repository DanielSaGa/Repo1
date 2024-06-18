import logging
import re

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Expresión regular para detectar números de teléfono con prefijo de 1 o 2 dígitos y 10 dígitos siguientes
telefono_regex = re.compile(r"^\+?(\d{1,2})(\d{10})$")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hola {user.mention_html()}! Estoy aquí para ayudarte a saber si el número de telefono que ingresaste es de lada nacional o internacional :D",
        reply_markup=ForceReply(selective=True),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Ingresa un número de teléfono con el formato adecuado para saber si es nacional o internacional. Ejemplo: +521234567890")

async def analyze_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Analyze the phone number to determine if it's national or international."""
    message_text = update.message.text.strip()
    match = telefono_regex.match(message_text)
    
    if match:
        prefijo = match.group(1)
        if prefijo == "52":
            await update.message.reply_text("El número es nacional.")
        else:
            await update.message.reply_text("El número es internacional.")
    else:
        await update.message.reply_text("El formato del número es incorrecto. Asegúrate de incluir el prefijo y 10 dígitos siguientes. Ejemplo: +521234567890")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token("7036403450:AAE90aq9VXFja8_5DZ9gXNB_pCUwt-IcTUY").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, analyze_phone_number))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
