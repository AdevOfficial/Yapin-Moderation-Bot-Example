"""Small config helper for the moderation bot example.

Beginner note:
- We keep all settings in one place so it is easy to change them.
- Secrets (token, owner id) come from environment variables or a .env file.
"""

import os

from pyyapper import load_env_file


def load_settings():
    # Read .env if present (safe to call even if the file does not exist).
    load_env_file(".env")

    token = os.getenv("YAPPER_BOT_TOKEN", "").strip()
    owner_id = os.getenv("OWNER_ID", "").strip()
    mod_log_channel = os.getenv("MOD_LOG_CHANNEL_ID", "").strip()
    mod_role_ids = [x.strip() for x in os.getenv("MOD_ROLE_IDS", "").split(",") if x.strip()]

    # Words that the auto-mod will remove. Keep this list short for the demo.
    bad_words = [w.strip().lower() for w in os.getenv("BAD_WORDS", "spam,scam").split(",") if w.strip()]

    # How many messages /purge can delete at once.
    purge_limit = int(os.getenv("PURGE_LIMIT", "25"))

    return {
        "token": token,
        "owner_id": owner_id,
        "mod_log_channel": mod_log_channel,
        "mod_role_ids": mod_role_ids,
        "bad_words": bad_words,
        "purge_limit": purge_limit,
    }
