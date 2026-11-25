"""Moderation permission helpers.

Beginner note:
- PyYapper gives you the author id and server id on every command (ctx).
- We fetch the member to read their role ids, then compare against the
  configured moderator roles or the bot owner.
"""


async def is_moderator(ctx, settings):
    """Return True when ctx.author is allowed to run moderation commands."""
    bot = ctx._bot
    author_id = str(ctx.author_id)

    # The bot owner can always moderate.
    if settings.get("owner_id") and author_id == str(settings["owner_id"]):
        return True

    # DMs have no server, so no moderation there.
    if not ctx.server_id:
        return False

    # Fetch the member so we can read their roles.
    try:
        member = await bot.member(ctx.server_id, ctx.author_id)
    except Exception:
        return False

    roles = [str(r) for r in (getattr(member, "roles", None) or [])]
    mod_roles = [str(r) for r in settings.get("mod_role_ids", [])]
    return any(r in mod_roles for r in roles)


async def require_moderator(ctx, settings):
    """Reply with an error and return False if the user is not a moderator."""
    if await is_moderator(ctx, settings):
        return True
    await ctx.reply("You do not have permission to use this command.")
    return False
