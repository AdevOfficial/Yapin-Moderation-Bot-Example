"""Event listeners: auto-mod, welcome, error handling."""

from pyyapper.ext.commands import Cog, listener

from utils.checks import is_moderator


class Events(Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @property
    def settings(self):
        return self.bot.settings

    @listener("ready")
    async def on_ready(self, me):
        print(f"Moderation bot online as {me.username}")

    @listener("member_join")
    async def on_member_join(self, ev):
        # Send a welcome message to the first text channel we can find.
        try:
            channels = await self.bot.channels(ev.server_id, type="text")
        except Exception:
            channels = []
        if channels:
            await self.bot.send(channels[0].id, f"Welcome <@{ev.user_id}> to the server!")

    @listener("message")
    async def on_message(self, ctx):
        # Skip commands and messages from moderators.
        if ctx.command:
            return
        if await is_moderator(ctx, self.settings):
            return

        content = (ctx.content or "").lower()
        bad_words = self.settings.get("bad_words", [])
        for word in bad_words:
            if word and word in content:
                try:
                    await ctx.delete()
                except Exception:
                    pass
                await ctx.say(f"<@{ctx.author_id}>, that word is not allowed here.")
                return

    @listener("command_error")
    async def on_command_error(self, payload):
        ctx = payload.get("ctx")
        error = payload.get("error")
        if ctx is None:
            return
        try:
            await ctx.reply(f"Something went wrong: {error}")
        except Exception:
            pass


def setup(bot):
    bot.add_cog(Events(bot))
