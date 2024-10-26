import os
import logging
import asyncio
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from nutritionistAgent import Nutritionist
from concurrent.futures import ThreadPoolExecutor


load_dotenv()

class TelegramBot:
    def __init__(self) -> None:
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        self.logger = logging.getLogger(__name__)
        self.app = Client(
            "NutriAI",
            api_id=int(os.getenv("TELEGRAM_API_ID")),
            api_hash=os.getenv("TELEGRAM_API_HASH"),
            bot_token=os.getenv("TELEGRAM_TOKEN")
        )
        self.setup_handlers()
        self.executor = ThreadPoolExecutor(max_workers=3)

    def setup_handlers(self):
        start_handler = MessageHandler(self.start, filters.command("start") & filters.private)
        self.app.add_handler(start_handler)

        text_filter = filters.text & filters.private
        message_handler = MessageHandler(self.handle_message, text_filter)
        self.app.add_handler(message_handler)

        photo_filter = filters.photo & filters.private
        photo_handler = MessageHandler(self.handle_photo, photo_filter)
        self.app.add_handler(photo_handler)
    
    async def start(self, client: Client, message: Message):
        await message.reply_text("Olá! Eu sou a NutriAI. Como posso te ajudar hoje?")
        self.logger.info(f"Received start command from {message.from_user.username}")

    async def handle_message(self, client: Client, message: Message):
        user_id = message.from_user.id
        user_input = message.text

        await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

        self.agent = Nutritionist(session_id=str(user_id))

        try:
            response = await asyncio.get_event_loop().run_in_executor(self.executor, self.agent.run, user_input)
        except Exception as error:
            response = f"Ocorreu um erro ao processar sua mensagem: {str(error)}"
            self.logger.error(response, exc_info=True)
        
        await message.reply_text(response)
        self.logger.info(f"Response sent to user {user_id}.")

    async def handle_photo(self, client: Client, message: Message):
        user_id = message.from_user.id
        photo_id = message.photo.file_id
        
        await client.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

        storage_path = os.path.join(os.getcwd(), "images")
        os.makedirs(storage_path, exist_ok=True)

        file_name = f"{user_id}_{photo_id}.jpg";
        photo_path = os.path.join(storage_path, file_name)
        await message.download(file_name=photo_path)

        self.agent = Nutritionist(session_id=str(user_id))

        try:
            response = await asyncio.get_event_loop().run_in_executor(self.executor, self.agent.run, photo_path)
        except Exception as error:
            response = f"Ocorreu um erro ao processar sua imagem: {str(error)}"
            self.logger.error(response, exc_info=True)
        
        await message.reply_text(response)
        self.logger.info(f"Response sent to user {user_id}.")

    def run(self):
        self.logger.info(f"Starting bot...")
        self.app.run()