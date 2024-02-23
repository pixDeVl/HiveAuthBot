import discord
from discord.ext.commands import Bot, when_mentioned
from os import listdir
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from src.config import Configuration as Config

GUILD = discord.Object(id=Config.GUILD_ID)

log = logging.getLogger('discord')


class BaseBot(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = log
        self.log.setLevel(logging.DEBUG)
        # if Config.LOG_WRITES:
        #     file_handler = TimedRotatingFileHandler(filename='./' + Config.LOG_FILE_DIR + '/' + Config.LOG_FILE_NAME,
        #                                             when=Config.LOG_ROLLOVER,
        #                                             backupCount=Config.LOG_BACKUP_COUNT)
        #     file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        #     self.log.addHandler(file_handler)
        self.start_time = datetime.datetime.now()

    async def setup_hook(self):
        for filename in listdir("./src/commands"):
            if filename.endswith(".py"):
                # cut off the .py from the file name
                await self.load_extension(f"src.commands.{filename[:-3]}")
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)

        log.info('Loaded Commands')

    async def on_ready(self):
        await self.change_presence(status=discord.Status.online, activity=discord.Game(name='beat the Job Queue'))


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
bot = BaseBot(when_mentioned, intents=intents)

def main():
    bot.run(Config.BOT_TOKEN)
