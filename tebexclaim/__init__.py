import discord
from redbot.core import commands, Config
import aiohttp

class TebexClaim(commands.Cog):
    """Erlaube Nutzern, ihre Tebex-Käufe mit !claim einzulösen."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.config.register_global(api_key=None, used_ids=[])

    @commands.command()
    async def setapikey(self, ctx, key: str):
        """Setzt den Tebex Secret API Key."""
        await self.config.api_key.set(key)
        await ctx.send("API Key wurde gesetzt.")

    @commands.command()
    async def claim(self, ctx, transaction_id: str):
        """Löst eine Tebex-Kauf-ID ein und vergibt Rollen basierend auf dem Produktnamen."""
        api_key = await self.config.api_key()
        used_ids = await self.config.used_ids()

        if not api_key:
            await ctx.send("API Key wurde noch nicht gesetzt. Nutze !setapikey <key>")
            return

        if transaction_id in used_ids:
            await ctx.send("Diese Kauf-ID wurde bereits eingelöst.")
            return

        headers = {"X-Tebex-Secret": api_key}
        url = f"https://plugin.tebex.io/payments/{transaction_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status != 200:
                    await ctx.send("Kauf-ID ungültig oder nicht gefunden.")
                    return
                data = await resp.json()

        try:
            packages = data["packages"]
            if not packages:
                await ctx.send("Kein Produkt in der Transaktion gefunden.")
                return

            granted_roles = []
            for product in packages:
                role_name = product["name"]
                role = discord.utils.get(ctx.guild.roles, name=role_name)
                if role:
                    await ctx.author.add_roles(role)
                    granted_roles.append(role.name)

            if granted_roles:
                await self.config.used_ids.set(used_ids + [transaction_id])
                await ctx.send(f"Rollen vergeben: {', '.join(granted_roles)}")
            else:
                await ctx.send("Keine passenden Rollen auf dem Server gefunden.")
        except Exception as e:
            await ctx.send(f"Fehler beim Verarbeiten: {e}")

def setup(bot):
    bot.add_cog(TebexClaim(bot))
