import discord
from redbot.core import commands, Config
import aiohttp
import asyncio

class TebexClaim(commands.Cog):
    """Rolle basierend auf Tebex-Kauf abholen"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=987654321)
        default_guild = {
            "api_token": None,
            "product_roles": {}  # {"Produktname": "Rollenname"}
        }
        self.config.register_guild(**default_guild)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def settoken(self, ctx, token: str):
        """Setzt den Tebex API Public Token"""
        await self.config.guild(ctx.guild).api_token.set(token)
        await ctx.send("✅ API Token gespeichert.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def mapproduct(self, ctx, produktname: str, rollenname: str):
        """Mappt ein Produkt auf eine Discord-Rolle"""
        async with self.config.guild(ctx.guild).product_roles() as mapping:
            mapping[produktname] = rollenname
        await ctx.send(f"✅ Produkt '{produktname}' → Rolle '{rollenname}' gespeichert.")

    @commands.command()
    @commands.guild_only()
    async def claim(self, ctx):
        """Erhalte deine Rolle basierend auf deinem Tebex-Kauf"""
        user = ctx.author
        guild = ctx.guild

        api_token = await self.config.guild(guild).api_token()
        if not api_token:
            await ctx.send("❌ API Token wurde noch nicht gesetzt.")
            return

        # Anfrage an Tebex API
        async with aiohttp.ClientSession() as session:
            headers = {
                "X-Tebex-Store": api_token
            }
            url = "https://plugin.tebex.io/payments"
            try:
                async with session.get(url, headers=headers) as resp:
                    if resp.status != 200:
                        await ctx.send("❌ Fehler beim Abrufen der Käufe von Tebex.")
                        return
                    data = await resp.json()
            except Exception as e:
                await ctx.send(f"Fehler bei API-Anfrage: {e}")
                return

        # Käufe nach Discord-ID durchsuchen
        purchases = data.get("payments", [])
        matched = None
        for p in purchases:
            if str(user.id) in p.get("player", {}).get("meta", {}).get("discord_id", ""):
                matched = p
                break

        if not matched:
            await ctx.send("❌ Kein Kauf mit deiner Discord-ID gefunden.")
            return

        # Produkt-zu-Rollen-Mapping
        product_roles = await self.config.guild(guild).product_roles()
        product_name = matched["package"]["name"]

        role_name = product_roles.get(product_name)
        if not role_name:
            await ctx.send(f"❌ Keine Rolle für Produkt '{product_name}' konfiguriert.")
            return

        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            await ctx.send(f"❌ Die Rolle '{role_name}' existiert nicht.")
            return

        await user.add_roles(role)
        await ctx.send(f"✅ Du hast die Rolle **{role.name}** für deinen Kauf erhalten!")
