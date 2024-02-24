import discord
from discord import app_commands
from discord.ext import commands
from mwoauth import ConsumerToken, Handshaker
from src.config import Configuration as config
from src.db.sessionmaker import Session
from src.db.database import TokenBind

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
                                callback=f'http://localhost/oauth-callback/{interaction.user.id}')
        # Step 1: Initialize -- ask MediaWiki for a temporary key/secret for user
        redirect_url, request_token = handshaker.initiate()

        session = Session()
        session.add(TokenBind(token=request_token.key, secret=request_token.secret, discord_id=interaction.user.id))
        session.commit()
        await interaction.response.send_message(f"[bwap]({redirect_url})", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AuthCommands(bot))
    bot.log.info('Loaded Auth Commands')
