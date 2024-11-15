# handlers.py
import telebot
from utils import is_valid_url
from link_generator import LinkGenerator

class BotHandlers:
    def __init__(self, bot):
        self.bot = bot
        self.register_handlers()

    def register_handlers(self):
        self.bot.message_handler(commands=['start'])(self.start_message)
        self.bot.message_handler(commands=['generate_links'])(self.generate_links)
        self.bot.message_handler(commands=['help'])(self.help_message)

    def start_message(self, message):
        welcome_text = (
            "<b>Welcome to the Link Generator Bot!</b>\n\n"
            "To use this bot, send a command in the following format:\n"
            "<blockquote> <code>/generate_links &lt;base_url&gt; &lt;start_number&gt; &lt;end_number&gt;</code> </blockquote>\n\n"
            "Example:\n"
            "<blockquote> <code>/generate_links https://t.me/Manager_Kim_Manhwa 198 201</code> </blockquote>"
            "Use /help to learn more about how to use the bot."
        )
        self.bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')

    def help_message(self, message):
        help_text = (
            "<b>📚 Link Generator Bot User Guide 📚</b>\n\n"
            "<blockquote>This bot helps you generate downloadable links for content (e.g., manga, anime, Hindi content, or custom files) with specific numbering.</blockquote>\n\n"
            "<blockquote>Here's how you can use the bot effectively:</blockquote>\n\n"
            "<b>1. Generating Links:</b>\n"
            "<blockquote>Use the <code>/generate_links</code> command with the following format:\n"
            "<code>/generate_links &lt;base_url&gt; &lt;start_number&gt; &lt;end_number&gt;</code>\n"
            "<code>&lt;base_url&gt;:</code> The base URL for the links.\n"
            "<code>&lt;start_number&gt;:</code> The starting number for the links.\n"
            "<code>&lt;end_number&gt;:</code> The ending number for the links.</blockquote>\n\n"
            "<blockquote>Example:\n"
            "<code>/generate_links https://t.me/Manager_Kim_Manhwa 198 201</code></blockquote>\n\n"
            "<b>2. After running the command:</b>\n"
            "<blockquote>The bot will ask you to provide the <i>anime/manga name</i>.</blockquote>\n"
            "<blockquote>Next, you will be asked to specify the <i>content type</i>. You can choose from the following options:\n"
            "   <code>manga</code>: For manga files.\n"
            "   <code>anime</code>: For anime video files.\n"
            "   <code>hindi</code>: For Hindi content.\n"
            "   <code>custom</code>: For custom file links.</blockquote>\n\n"
            "<blockquote>For custom files, you will also be asked to provide a <i>prefix</i> and <i>file extension</i> (e.g., <code>.mp4</code> or <code>.pdf</code>).</blockquote>\n\n"
            "<b>3. Season and Episode Numbering (Anime/Hindi):</b>\n"
            "<blockquote>If you select <code>anime</code> or <code>hindi</code>, the bot will ask for the <i>season number</i> (e.g., 1) and then for the <i>starting episode number</i>.</blockquote>\n\n"
            "<b>4. Manga Numbering:</b>\n"
            "<blockquote>If you select <code>manga</code>, the bot will prompt you to enter the <i>starting filename number</i> (e.g., 001).</blockquote>\n\n"
            "<b>5. Custom Numbering:</b>\n"
            "<blockquote>For <code>custom</code> content, you will need to provide a <i>custom prefix</i> and <i>file extension</i>, followed by the starting number for the filenames.</blockquote>\n\n"
            "<blockquote>At the end, the bot will generate and send the downloadable links based on your input.</blockquote>\n\n"
            "<blockquote>Feel free to experiment with different content types!</blockquote>"
        )
        self.bot.send_message(message.chat.id, help_text, parse_mode='HTML')







    def generate_links(self, message):
        parts = message.text.split()

        if len(parts) != 4:
            self.bot.send_message(message.chat.id, "Invalid command format. Please provide exactly 3 parameters.")
            return

        base_url, start_number, end_number = parts[1], parts[2], parts[3]
        
        if not is_valid_url(base_url):
            self.bot.send_message(message.chat.id, "Invalid URL format. Please provide a valid base URL.")
            return

        try:
            start_number = int(start_number)
            end_number = int(end_number)

            self.bot.send_message(message.chat.id, "Enter the anime/manga name (you can include spaces):")
            self.bot.register_next_step_handler(message, self.handle_anime_name_input, base_url, start_number, end_number)

        except ValueError:
            self.bot.send_message(message.chat.id, "Invalid number format. Please ensure start and end numbers are valid integers.")

    def handle_anime_name_input(self, message, base_url, start_number, end_number):
        anime_manga_name = message.text.strip()
        self.bot.send_message(message.chat.id, "What type of content is this? (manga/anime/hindi/custom):")
        self.bot.register_next_step_handler(message, self.handle_content_type_input, base_url, start_number, end_number, anime_manga_name)

    def handle_content_type_input(self, message, base_url, start_number, end_number, anime_manga_name):
        content_type = message.text.strip().lower()
        if content_type not in ['manga', 'anime', 'hindi', 'custom']:
            self.bot.send_message(message.chat.id, "Invalid type. Please enter 'manga', 'anime', 'hindi', or 'custom'.")
            return

        if content_type == 'custom':
            self.bot.send_message(message.chat.id, "Enter the custom prefix:")
            self.bot.register_next_step_handler(message, self.handle_custom_prefix_input, base_url, start_number, end_number, anime_manga_name)
        elif content_type in ['anime', 'hindi']:
            self.bot.send_message(message.chat.id, "Enter the season number (e.g., 1):")
            self.bot.register_next_step_handler(message, self.handle_season_input, base_url, start_number, end_number, anime_manga_name, content_type)
        else:
            self.bot.send_message(message.chat.id, "Enter the starting number for the filename (e.g., 001):")
            self.bot.register_next_step_handler(message, self.handle_filename_input, base_url, start_number, end_number, anime_manga_name, content_type)

    def handle_custom_prefix_input(self, message, base_url, start_number, end_number, anime_manga_name):
        custom_prefix = message.text.strip()
        self.bot.send_message(message.chat.id, "Enter the custom file extension (e.g., .mp4, .pdf):")
        self.bot.register_next_step_handler(message, self.handle_custom_extension_input, base_url, start_number, end_number, anime_manga_name, custom_prefix)

    def handle_custom_extension_input(self, message, base_url, start_number, end_number, anime_manga_name, custom_prefix):
        custom_extension = message.text.strip()
        self.bot.send_message(message.chat.id, "Enter the starting number for the filename (e.g., 001):")
        self.bot.register_next_step_handler(message, self.handle_filename_input, base_url, start_number, end_number, anime_manga_name, 'custom', custom_prefix, custom_extension)

    def handle_season_input(self, message, base_url, start_number, end_number, anime_manga_name, content_type):
        try:
            season_number = int(message.text)
            self.bot.send_message(message.chat.id, "Enter the episode number to start from (e.g., 1):")
            self.bot.register_next_step_handler(message, self.handle_filename_input, base_url, start_number, end_number, anime_manga_name, content_type, season_number)
        except ValueError:
            self.bot.send_message(message.chat.id, "Invalid season number. Please enter a valid integer for the season.")

    def handle_filename_input(self, message, base_url, start_number, end_number, anime_manga_name, content_type, season_number=None, custom_prefix=None, custom_extension=None):
        try:
            filename_number = int(message.text)
            link_gen = LinkGenerator(base_url, start_number, end_number, anime_manga_name, content_type, custom_prefix, custom_extension, season_number, filename_number)
            download_links = link_gen.generate_links()
            self.send_long_message(message.chat.id, "\n\n".join(download_links))
        except ValueError:
            self.bot.send_message(message.chat.id, "Invalid input. Please enter a valid number for the filename.")

    def send_long_message(self, chat_id, message):
        max_length = 4096
        for i in range(0, len(message), max_length):
            self.bot.send_message(chat_id, message[i:i + max_length])
