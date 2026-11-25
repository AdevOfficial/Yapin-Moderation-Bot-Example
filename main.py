"""Entry point for the moderation bot.

Beginner note:
- We load settings, create the Bot, store shared data on the bot object,
  then load our cogs (command groups) and start the bot.
"""

import asyncio

from pyyapper import Bot, JSONStore

from config import load_settings


async def main():
    settings = load_settings()

    if not settings["token"]:
        raise SystemExit(
            "Missing YAPPER_BOT_TOKEN. Copy .env.example to .env and fill it in."
        )

    bot = Bot(settings["token"], ignore_bots=True)

    # Shared state that cogs can reach through bot.
    bot.settings = settings
    bot.warnings_store = JSONStore("warnings.json")

    # Optional: make yourself the owner so is_owner checks pass.
    if settings["owner_id"]:
        bot.owner_id = settings["owner_id"]

    # Load cogs. load_extension imports the module and calls its setup(bot).
    await bot.load_extensions("cogs")

    # on_ready is also handled inside the Events cog.
    @bot.event
    async def on_ready(me):
        print(f"Logged in as {me.username}")

    await bot.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
