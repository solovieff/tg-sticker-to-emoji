#!/usr/bin/env python3
"""
One-command sticker pack to emoji pack converter.
Just run: python sticker_to_emoji.py <sticker_pack_name>
"""

import os
import sys
import asyncio
import argparse
from pathlib import Path
from dotenv import load_dotenv
import aiohttp
import ssl
from telethon import TelegramClient
from telethon.tl.types import Document, DocumentAttributeSticker, InputStickerSetShortName, DocumentAttributeFilename
from telethon.tl.functions.messages import GetStickerSetRequest
from PIL import Image
import io
import gzip
import json
from rlottie_python import LottieAnimation


class StickerToEmojiConverter:
    """Convert Telegram sticker packs to emoji packs."""
    
    def __init__(self, api_id: int, api_hash: str, bot_token: str, user_id: int):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.user_id = user_id
        self.bot_api_url = f"https://api.telegram.org/bot{bot_token}"
        self.bot_username = None
        self.client = None
        
    async def __aenter__(self):
        """Setup Telegram client."""
        self.client = TelegramClient("sticker_session", self.api_id, self.api_hash)
        await self.client.start()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup."""
        if self.client:
            await self.client.disconnect()
    
    def is_animated_sticker(self, sticker: Document) -> bool:
        """Check if sticker is animated (TGS format)."""
        for attr in sticker.attributes:
            if isinstance(attr, DocumentAttributeFilename):
                if attr.file_name.endswith('.tgs'):
                    return True
        return sticker.mime_type == 'application/x-tgsticker'
    
    def render_tgs_to_png(self, tgs_bytes: bytes, output_path: Path, size: int = 100):
        """Render TGS (Lottie) animation to PNG (first frame)."""
        try:
            # Decompress gzip
            decompressed = gzip.decompress(tgs_bytes)
            
            # Load animation with rlottie
            anim = LottieAnimation.from_data(decompressed.decode('utf-8'))
            
            # Render first frame using Pillow
            img = anim.render_pillow_frame(0, width=size, height=size)
            
            # Ensure RGBA
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Center and save
            emoji_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            emoji_img.paste(img, (0, 0), img)
            emoji_img.save(output_path, format='PNG', optimize=True)
            
            return True
            
        except Exception as e:
            # Fallback: if rendering fails, skip
            return False
    
    async def get_sticker_pack(self, pack_name: str):
        """Download sticker pack from Telegram."""
        if not self.client:
            raise RuntimeError("Client not initialized")
        
        # Extract pack name from URL if needed
        pack_name = pack_name.split('/')[-1]
        if pack_name.startswith('addemoji?set='):
            pack_name = pack_name.split('=')[-1]
        
        print(f"📦 Fetching sticker pack: {pack_name}")
        
        try:
            sticker_set = await self.client(GetStickerSetRequest(
                stickerset=InputStickerSetShortName(short_name=pack_name),
                hash=0
            ))
            return sticker_set
        except Exception as e:
            raise ValueError(f"Could not retrieve sticker pack: {e}")
    
    async def download_and_convert_stickers(self, sticker_set, output_dir: Path, limit: int = 50):
        """Download stickers and convert to emoji format."""
        stickers = sticker_set.documents
        pack_title = sticker_set.set.title
        
        print(f"📊 Found {len(stickers)} stickers in '{pack_title}'")
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        converted = []
        skipped = 0
        
        for i, sticker in enumerate(stickers, 1):
            if len(converted) >= limit:
                print(f"⚠️  Reached limit of {limit} emojis")
                break
            
            try:
                # Get emoji
                emoji = '😀'
                for attr in sticker.attributes:
                    if isinstance(attr, DocumentAttributeSticker):
                        emoji = attr.alt or '😀'
                        break
                
                filename = f"emoji_{len(converted)+1:03d}_{emoji}.png"
                filepath = output_dir / filename
                
                print(f"  {len(converted)+1}/{limit}: {emoji}", end=' ')
                
                # Download sticker
                file_bytes = await self.client.download_media(sticker, file=bytes)
                
                # Check if animated (TGS)
                is_animated = self.is_animated_sticker(sticker)
                
                if is_animated:
                    # Render TGS to PNG
                    success = self.render_tgs_to_png(file_bytes, filepath, size=100)
                    if not success:
                        print("✗ (TGS render failed)")
                        skipped += 1
                        continue
                else:
                    # Convert static sticker to emoji format
                    with Image.open(io.BytesIO(file_bytes)) as img:
                        if img.mode != 'RGBA':
                            img = img.convert('RGBA')
                        
                        img.thumbnail((100, 100), Image.Resampling.LANCZOS)
                        
                        emoji_img = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
                        offset = ((100 - img.width) // 2, (100 - img.height) // 2)
                        emoji_img.paste(img, offset, img)
                        
                        emoji_img.save(filepath, format='PNG', optimize=True)
                
                converted.append((filepath, emoji))
                print("✓")
                
            except Exception as e:
                print(f"✗ Error: {e}")
                continue
        
        print(f"\n✅ Converted {len(converted)} stickers")
        if skipped > 0:
            print(f"⏭️  Skipped {skipped} animated stickers")
        
        return converted, pack_title
    
    async def get_bot_info(self, session: aiohttp.ClientSession) -> str:
        """Get bot username."""
        if self.bot_username:
            return self.bot_username
        
        url = f"{self.bot_api_url}/getMe"
        async with session.get(url) as response:
            result = await response.json()
            if result.get('ok'):
                self.bot_username = result['result']['username']
                return self.bot_username
            raise ValueError(f"Failed to get bot info: {result.get('description')}")
    
    async def upload_and_create_emoji_pack(
        self, 
        emoji_files: list, 
        pack_name: str, 
        pack_title: str,
        session: aiohttp.ClientSession
    ):
        """Upload emojis and create Telegram emoji pack."""
        
        # Get bot username and fix pack name
        bot_username = await self.get_bot_info(session)
        if not pack_name.endswith(f"_by_{bot_username}"):
            pack_name = f"{pack_name}_by_{bot_username}"
        
        print(f"\n🚀 Creating emoji pack...")
        print(f"   Name: {pack_title}")
        print(f"   URL name: {pack_name}")
        
        # Upload files
        stickers = []
        for i, (filepath, emoji) in enumerate(emoji_files, 1):
            try:
                print(f"   Uploading {i}/{len(emoji_files)}: {emoji}", end=' ')
                
                # Upload file
                url = f"{self.bot_api_url}/uploadStickerFile"
                data = aiohttp.FormData()
                data.add_field('user_id', str(self.user_id))
                data.add_field('sticker_format', 'static')
                
                with open(filepath, 'rb') as f:
                    data.add_field('sticker', f, filename=filepath.name, content_type='image/png')
                    
                    async with session.post(url, data=data) as response:
                        result = await response.json()
                        
                        if not result.get('ok'):
                            print(f"✗ {result.get('description')}")
                            continue
                        
                        file_id = result['result']['file_id']
                
                stickers.append({
                    'sticker': file_id,
                    'emoji_list': [emoji],
                    'format': 'static'
                })
                
                print("✓")
                
            except Exception as e:
                print(f"✗ {e}")
                continue
        
        if not stickers:
            raise ValueError("No stickers uploaded successfully")
        
        # Create sticker set
        print(f"\n📝 Creating pack with {len(stickers)} emojis...")
        
        url = f"{self.bot_api_url}/createNewStickerSet"
        data = {
            'user_id': self.user_id,
            'name': pack_name,
            'title': pack_title,
            'stickers': stickers,
            'sticker_type': 'custom_emoji'
        }
        
        async with session.post(url, json=data) as response:
            result = await response.json()
            
            if not result.get('ok'):
                raise ValueError(f"Failed to create pack: {result.get('description')}")
        
        pack_url = f"https://t.me/addemoji/{pack_name}"
        return pack_url


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Convert Telegram sticker pack to emoji pack",
        epilog="Example: python sticker_to_emoji.py Opa4958"
    )
    parser.add_argument("sticker_pack", help="Sticker pack name or URL")
    parser.add_argument("-n", "--name", help="Custom name for emoji pack (optional)")
    parser.add_argument("-l", "--limit", type=int, default=50, help="Max emojis (default: 50)")
    args = parser.parse_args()
    
    # Load environment
    load_dotenv()
    
    # Get credentials
    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    user_id = os.getenv("TELEGRAM_USER_ID")
    
    # Validate
    missing = []
    if not api_id: missing.append("TELEGRAM_API_ID")
    if not api_hash: missing.append("TELEGRAM_API_HASH")
    if not bot_token: missing.append("TELEGRAM_BOT_TOKEN")
    if not user_id: missing.append("TELEGRAM_USER_ID")
    
    if missing:
        print(f"❌ Error: Missing required environment variables:", file=sys.stderr)
        for var in missing:
            print(f"   - {var}", file=sys.stderr)
        print("\nSet them in .env file or as environment variables", file=sys.stderr)
        sys.exit(1)
    
    try:
        api_id = int(api_id)
        user_id = int(user_id)
    except (ValueError, TypeError):
        print("❌ Error: API_ID and USER_ID must be numbers", file=sys.stderr)
        sys.exit(1)
    
    print("🎨 Sticker to Emoji Converter\n")
    
    # Create temporary directory
    temp_dir = Path("temp_emojis")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Setup SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        
        async with aiohttp.ClientSession(connector=connector) as session:
            async with StickerToEmojiConverter(api_id, api_hash, bot_token, user_id) as converter:
                # Download and convert stickers
                sticker_set = await converter.get_sticker_pack(args.sticker_pack)
                emoji_files, pack_title = await converter.download_and_convert_stickers(
                    sticker_set, 
                    temp_dir, 
                    limit=args.limit
                )
                
                if not emoji_files:
                    print("❌ No emojis to upload", file=sys.stderr)
                    sys.exit(1)
                
                # Use custom name or generate from pack title
                pack_name = args.name or pack_title.replace(" ", "_")
                
                # Create emoji pack
                pack_url = await converter.upload_and_create_emoji_pack(
                    emoji_files,
                    pack_name,
                    pack_title,
                    session
                )
                
                print(f"\n✅ Success! Emoji pack created!")
                print(f"🔗 {pack_url}")
                print(f"\n💡 Add this pack in Telegram and use emojis as reactions!")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Cleanup temp files
        import shutil
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


if __name__ == "__main__":
    asyncio.run(main())
