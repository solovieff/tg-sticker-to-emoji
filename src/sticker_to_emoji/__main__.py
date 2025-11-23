"""CLI entry point for sticker_to_emoji package."""

import asyncio
from .converter import main

if __name__ == "__main__":
    asyncio.run(main())
