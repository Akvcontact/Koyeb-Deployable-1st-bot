from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.enums import ChatMemberStatus
from pyrogram.handlers import MessageHandler
import logging
import traceback

# Custom get_peer_type function
def get_peer_type(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"

# Monkey patching the function
import pyrogram.utils as utils
utils.get_peer_type = get_peer_type

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceBot:
    def __init__(self, api_id, api_hash, bot_token, channel_id, invite_link):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.channel_id = channel_id
        self.invite_link = invite_link
        self.bot = Client("voice_bot", api_id=self.api_id, api_hash=self.api_hash, bot_token=self.bot_token)

      #initialize the dictionary to store voice media type
        self.Dict = {'voice_msg': None}
       








        # Add handlers
        self.add_handlers()
        
    def start(self):
        self.bot.run()

    def add_handlers(self):
        self.bot.add_handler(MessageHandler(self.force_join_check, filters.group & ~filters.service))
        self.bot.add_handler(MessageHandler(self.voice_reply, filters.voice & filters.group))
        self.bot.add_handler(MessageHandler(self.voice_command, filters.command(['voice']) & (filters.private | filters.group)))
        self.bot.add_handler(MessageHandler(self.help_command, filters.command(['help']) & (filters.private | filters.group)))













    async def force_join_check(self, client, message):
        # Your existing logic to check if the user has joined the channel
        pass

        user_id = message.from_user.id
        chat_id = message.chat.id
        try:
            # Fetch the user's status in the channel
            member = await client.get_chat_member(self.channel_id, user_id)
            if member.status not in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                logger.warning(f"User {user_id} is not a participant in the channel.")
                await message.reply(f"Please join our channel first to send messages: {self.invite_link}")
                return  # Ensure no further processing if the user is not a member
        except UserNotParticipant:
            logger.warning(f"User {user_id} is not a participant in the channel.")
            await message.reply(f"Please join our channel first to send messages: {self.invite_link}")
            return  # Ensure no further processing if the user is not a participant
        except Exception as e:
            logger.error(f"Error in force_join_check for user {user_id} in chat {chat_id}: {traceback.format_exc()}")

        # If the user is a participant, log the message and let the processing continue
        logger.info(f"User {user_id} is a participant in the channel. Processing further.")
        await self.process_message_handlers(client, message)


#Receiver-compatible codes
    async def process_message_handlers(self, client, message):
        if message is None:
            logger.error("Received a None message object.")
            return

        logger.info(f"Received message: {message}")
        logger.info(f"Message text: {message.text}")

        if message.voice:
            logger.info("Received a voice message.")
            await self.voice_reply(client, message)




















    #Command processing logic
        command = self.extract_command(message)
        if command == '/help':
            await self.help_command(client, message)
        elif command == '/voice':
            await self.voice_command(client, message)
















    def extract_command(self, message):
        command = message.text.split()[0] if message.text else None
        if command and "@" in command:
            command = command.split("@")[0]
        return command if command else ""  # Return an empty string if command is None

    async def voice_reply(self, client, message):
        # Your existing logic to handle voice messages
        self.Dict['voice_msg'] = message.voice.file_id
        await client.send_message(message.chat.id, f"Hey {message.from_user.first_name}! Your voice message is saved.")

    async def voice_command(self, client, message):
        try:
            if 'voice_msg' in self.Dict and self.Dict['voice_msg']:
                await client.send_voice(message.chat.id, self.Dict['voice_msg'])
                logging.info(f"Handled /voice command from user {message.from_user.id} in chat {message.chat.id}")
            else:
                await message.reply("No voice message is available.\nPlease send a voice message to save.")
        except Exception as e:
            logging.error(f"Error handling /voice command: {e}")

    async def help_command(self, client, message):
        # Your existing logic for the /help command
        await client.send_message(message.chat.id, "How can I help you?")

    def run(self):
        self.bot.run()

# Instantiate and run the bot
if __name__ == "__main__":
    API_ID = '19341831'
    API_HASH = 'd5dd7d867fc35ae9fa59c54e54d218ad'
    BOT_TOKEN = '7167823797:AAHnrBgaWCWnSQ7F838QRAQO2auiboiJby0'
    CHANNEL_ID = -1002218288744  # Replace with your actual channel ID
    CHANNEL_INVITE_LINK = 'https://t.me/+d5YjipSLU-0wMDg1'  # Replace with your channel invite link

    voice_bot = VoiceBot(API_ID, API_HASH, BOT_TOKEN, CHANNEL_ID, CHANNEL_INVITE_LINK)
    voice_bot.run()
