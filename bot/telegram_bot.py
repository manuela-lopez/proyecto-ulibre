import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from app.config import get_settings
from app.database import SessionLocal, init_db
from app.search import search_medicines

DISCLAIMER = "Esta informacion es orientativa y no reemplaza la consulta con un profesional de salud."


def format_medicine_response(query: str, results) -> str:
    if not results:
        return f"No encontre resultados para '{query}'.\n\n{DISCLAIMER}"

    medicine = results[0]
    vigente = "Si" if (medicine.estado_registro or "").lower() == "vigente" else "No confirmado"
    return "\n".join(
        [
            f"Medicamento: {medicine.nombre_medicamento}",
            f"Vigente: {vigente}",
            f"Registro INVIMA: {medicine.registro_invima or 'No disponible'}",
            f"Para que sirve: {medicine.para_que_sirve or 'No disponible en la fuente curada'}",
            f"Efectos secundarios: {medicine.efectos_secundarios or 'No disponible en la fuente curada'}",
            "",
            DISCLAIMER,
        ]
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Escribe el nombre de un medicamento para consultar su registro e informacion basica.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Ejemplo: acetaminofen. La respuesta no reemplaza la consulta medica.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text or ""
    with SessionLocal() as db:
        results = search_medicines(db, query)
    await update.message.reply_text(format_medicine_response(query, results))


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise RuntimeError("Configura TELEGRAM_BOT_TOKEN en .env")

    init_db()
    application = Application.builder().token(settings.telegram_bot_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()


if __name__ == "__main__":
    main()
