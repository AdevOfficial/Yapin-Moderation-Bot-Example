"""Moderation commands.

Beginner note:
- A "cog" is just a class that groups related commands.
- We use @command(...) from pyyapper.ext.commands instead of @bot.command(...).
- Each command method takes (self, ctx, ...) because it lives inside a class.
- Permission checks are done with a small helper, require_moderator.
"""

from pyyapper.ext.commands import Cog, command, listener
from pyyapper import Embed

from utils.checks import require_moderator
from utils.embeds import mod_log_embed


def _reason(parts):
    return " ".join(parts).strip() or "No reason given"


class Moderation(Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @property
    def settings(self):
        return self.bot.settings

    @property
    def store(self):
        return self.bot.warnings_store

    async def _log(self, action, moderator, target, reason=""):
        channel_id = self.settings.get("mod_log_channel")
        if not channel_id:
            return
        embed = mod_log_embed(action, moderator, target, reason)
        try:
            await self.bot.send(channel_id, "", embeds=[embed])
        except Exception:
            pass

    @command(description="Kick a member from the server")
    async def kick(self, ctx, user: int, *reason_parts):
        if not await require_moderator(ctx, self.settings):
            return
        reason = _reason(reason_parts)
        try:
            await self.bot.kick(ctx.server_id, str(user))
        except Exception as e:
            await ctx.reply(f"Could not kick that user: {e}")
            return
        await ctx.reply(f"Kicked <@{user}>. Reason: {reason}")
        await self._log("Kick", ctx.author_id, user, reason)

    @command(description="Ban a member from the server")
    async def ban(self, ctx, user: int, *reason_parts):
        if not await require_moderator(ctx, self.settings):
            return
        reason = _reason(reason_parts)
        try:
            await self.bot.ban(ctx.server_id, str(user))
        except Exception as e:
            await ctx.reply(f"Could not ban that user: {e}")
            return
        await ctx.reply(f"Banned <@{user}>. Reason: {reason}")
        await self._log("Ban", ctx.author_id, user, reason)

    @command(description="Remove a ban from a user")
    async def unban(self, ctx, user: int):
        if not await require_moderator(ctx, self.settings):
            return
        try:
            await self.bot.unban(ctx.server_id, str(user))
        except Exception as e:
            await ctx.reply(f"Could not unban that user: {e}")
            return
        await ctx.reply(f"Unbanned <@{user}>.")
        await self._log("Unban", ctx.author_id, user)

    @command(description="Time out (mute) a member for some minutes")
    async def timeout(self, ctx, user: int, minutes: int, *reason_parts):
        if not await require_moderator(ctx, self.settings):
            return
        reason = _reason(reason_parts)
        try:
            await self.bot.timeout(ctx.server_id, str(user), minutes, reason=reason)
        except Exception as e:
            await ctx.reply(f"Could not time out that user: {e}")
            return
        await ctx.reply(f"Timed out <@{user}> for {minutes} minute(s). Reason: {reason}")
        await self._log("Timeout", ctx.author_id, user, reason)

    @command(description="Warn a member (stored by the bot)")
    async def warn(self, ctx, user: int, *reason_parts):
        if not await require_moderator(ctx, self.settings):
            return
        reason = _reason(reason_parts)
        key = str(user)
        warnings = self.store.get(key, [])
        warnings.append({"moderator": str(ctx.author_id), "reason": reason})
        self.store.set(key, warnings)
        await ctx.reply(f"Warned <@{user}>. They now have {len(warnings)} warning(s). Reason: {reason}")
        await self._log("Warn", ctx.author_id, user, reason)

    @command(description="Show warnings for a member")
    async def warnings(self, ctx, user: int):
        if not await require_moderator(ctx, self.settings):
            return
        key = str(user)
        warnings = self.store.get(key, [])
        if not warnings:
            await ctx.reply(f"<@{user}> has no warnings.")
            return
        lines = [f"{i + 1}. {w.get('reason', '')} (by <@{w.get('moderator', '?')}>)" for i, w in enumerate(warnings)]
        await ctx.reply(f"Warnings for <@{user}> ({len(warnings)} total):\n" + "\n".join(lines))

    @command(description="Clear all warnings for a member")
    async def clearwarnings(self, ctx, user: int):
        if not await require_moderator(ctx, self.settings):
            return
        self.store.delete(str(user))
        await ctx.reply(f"Cleared warnings for <@{user}>.")
        await self._log("Clear warnings", ctx.author_id, user)

    @command(description="Delete the last N messages in this channel")
    async def purge(self, ctx, amount: int):
        if not await require_moderator(ctx, self.settings):
            return
        limit = min(max(amount, 1), int(self.settings.get("purge_limit", 25)))
        try:
            msgs = await self.bot.messages(ctx.channel_id, limit=limit + 1)
        except Exception as e:
            await ctx.reply(f"Could not fetch messages: {e}")
            return
        ids = [m.id for m in msgs if m.id != ctx.id][:limit]
        if not ids:
            await ctx.reply("Nothing to delete.")
            return
        try:
            await self.bot.bulk_delete(ctx.channel_id, ids)
        except Exception as e:
            await ctx.reply(f"Could not delete messages: {e}")
            return
        await ctx.reply(f"Deleted {len(ids)} message(s).")
        await self._log("Purge", ctx.author_id, ctx.channel_id, f"{len(ids)} messages")

    @command(description="Set slowmode (seconds) for this channel, 0 to disable")
    async def slowmode(self, ctx, seconds: int):
        if not await require_moderator(ctx, self.settings):
            return
        try:
            await self.bot.edit_channel(ctx.channel_id, slowmode=seconds)
        except Exception as e:
            await ctx.reply(f"Could not set slowmode: {e}")
            return
        await ctx.reply(f"Slowmode set to {seconds} second(s).")
        await self._log("Slowmode", ctx.author_id, ctx.channel_id, str(seconds))
def setup(bot):
    bot.add_cog(Moderation(bot))
