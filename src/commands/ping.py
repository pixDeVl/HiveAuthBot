import discord
import datetime
class Ping(discord.ext.commands.Cog, name='ping'):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @discord.ext.commands.command()
    async def ping(self, interaction: discord.Interaction):
        async def ping(self, interaction: discord.Interaction):
            """Sents a Pong! back to the caller with the current latency

            Args:
                interaction (discord.Interaction): The interaction from the app commands
            """
            await interaction.response.send_message(
                f'**Pong!** `{str(round(self.bot.latency * 1000))}` ms\n **Current Uptime:** `{str(datetime.now() - self.bot.start_time)}`.')

async def setup(bot):
    await bot.add_cog(Ping(bot))