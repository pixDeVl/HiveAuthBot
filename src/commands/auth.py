import discord
from discord import app_commands
from discord.ext import commands
from mwoauth import ConsumerToken, Handshaker
from src.config import Configuration as config


class AuthCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command(name="auth")
    async def auth(self, interaction: discord.Interaction) -> None:
        consumer_token = ConsumerToken(config.CONSUMER_KEY, config.CONSUMER_SECRET)
        # Construct handshaker with wiki URI and consumer
        handshaker = Handshaker("https://meta.mirabeta.org/w/index.php",
                                consumer_token,
                                callback='http://localhost/oauth-callback')
        # Step 1: Initialize -- ask MediaWiki for a temporary key/secret for user
        redirect_url, request_token = handshaker.initiate()
        await interaction.response.send_message(f"[bwap]({redirect_url})", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AuthCommands(bot))
    bot.log.info('Loaded Auth Commands')
