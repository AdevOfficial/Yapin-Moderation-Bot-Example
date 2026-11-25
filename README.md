# Moderation Bot Example (PyYapper)

A small, friendly example of a Discord-style moderation bot built with
[PyYapper](https://pypi.org/project/pyyapper/). It is written for beginners:
every file has comments, and the commands are simple to read.

## What it can do

- `kick`, `ban`, `unban`, `timeout` (mute) members
- `warn`, `warnings`, `clearwarnings` (stored in `warnings.json`)
- `purge` to delete recent messages
- `slowmode` to set channel slowmode
- Auto-mod: deletes messages that contain banned words
- Welcome message when someone joins
- Logs every action to a mod-log channel (optional)

## Project layout

```
moderation-bot-example/
  main.py              # starts the bot
  config.py            # reads settings from .env
  cogs/
    moderation.py      # moderation commands
    events.py          # event listeners (auto-mod, welcome, errors)
  utils/
    checks.py          # "is this user a moderator?" helper
    embeds.py          # builds the mod-log card
  .env.example         # copy to .env and fill in
  requirements.txt
```

## Setup

1. Install Python 3.10 or newer.
2. Install PyYapper:

   ```bash
   pip install pyyapper
   ```

3. Copy `.env.example` to `.env` and fill in your bot token:

   ```bash
   cp .env.example .env
   ```

   On Windows you can just rename the file in Explorer.

4. Open `.env` and set at least `YAPPER_BOT_TOKEN`. You can also set:
   - `OWNER_ID` - your user id (owner can always moderate)
   - `MOD_LOG_CHANNEL_ID` - channel id for the mod log
   - `MOD_ROLE_IDS` - comma separated role ids that count as moderators
   - `BAD_WORDS` - comma separated words the auto-mod removes

5. Run the bot:

   ```bash
   python main.py
   ```

## How the code works (for beginners)

- `main.py` loads settings, creates the `Bot`, stores shared data
  (`bot.settings`, `bot.warnings_store`), loads the cogs, and starts.
- A **cog** is a class that groups commands. `cogs/moderation.py` defines
  `Moderation(Cog)` with one method per command.
- Commands use `@command(description="...")`. The method signature uses type
  hints like `user: int`, and PyYapper converts the text argument for you.
- Permission checks live in `utils/checks.py`. `require_moderator` replies
  with an error and returns `False` when the user is not allowed.
- `JSONStore("warnings.json")` saves warnings to a file, so they survive
  restarts.
- `utils/embeds.py` builds a small `Embed` card for the mod log.

## Notes

- This is an example for learning. Read the code before using it in a real
  server, and adjust permissions to fit your needs.
- The bot needs permission to kick, ban, and manage messages in your server.
