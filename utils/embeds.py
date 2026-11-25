"""Embed builders for the moderation log.

Beginner note:
- An Embed is a rich message card. We build one for every moderation action
  so the mod-log channel keeps a nice history.
"""

from pyyapper import Embed


def mod_log_embed(action, moderator, target, reason=""):
    e = Embed()
    e.title(f"Moderation: {action}")
    e.description(f"**Moderator:** <@{moderator}>\n**Target:** <@{target}>")
    if reason:
        e.field("Reason", reason, inline=False)
    e.color("#ff6b4a")
    return e
