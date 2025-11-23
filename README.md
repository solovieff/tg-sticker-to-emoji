# 🎨 Telegram Sticker to Emoji Converter

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Convert any Telegram sticker pack into a custom emoji pack with **one simple command**! Supports static, animated (TGS), and video (WEBM) stickers with **full animation preservation**.

## ✨ Features

- 🚀 **One-Command Conversion** - Just provide the sticker pack name
- 🎭 **Full Animation Support** - Handles WEBP, PNG, TGS (Lottie), and WEBM formats
- ✨ **Animated Emojis** - Converts TGS to WEBM for animated emoji reactions
- 🤖 **Fully Automated** - Downloads, converts, and creates emoji pack automatically
- 💎 **High Quality** - Preserves transparency, animation, and image quality
- 🔗 **Instant Sharing** - Get a shareable `t.me/addemoji/` link immediately
- 💾 **Save Locally** - Optional flag to keep converted files
- 🧹 **Clean** - Automatic cleanup of temporary files

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Quick Start

```bash
# Install
pip install -r requirements.txt

# Setup credentials (one-time)
cp .env.example .env
# Edit .env with your Telegram API credentials

# Convert!
python -m sticker_to_emoji YourStickerPackName
```

**That's it!** You'll get a link like `https://t.me/addemoji/your_pack` ready to use. 🎉

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Telegram account
- Telegram Premium (to use custom emojis as reactions)
- ffmpeg (for animated emoji support) - install with `brew install ffmpeg` on macOS

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/tg-sticker-to-emoji.git
cd tg-sticker-to-emoji
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Get Telegram Credentials

You need 4 credentials in your `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add:

#### 1. **TELEGRAM_API_ID** & **TELEGRAM_API_HASH**
- Go to https://my.telegram.org
- Click "API development tools"
- Create an application
- Copy your `api_id` and `api_hash`

#### 2. **TELEGRAM_BOT_TOKEN**
- Open [@BotFather](https://t.me/BotFather) in Telegram
- Send `/newbot`
- Follow instructions to create a bot
- Copy the bot token

#### 3. **TELEGRAM_USER_ID**
- Open [@userinfobot](https://t.me/userinfobot) in Telegram
- Send `/start`
- Copy your numeric user ID

Your `.env` should look like:
```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_USER_ID=987654321
```

## 💻 Usage

### Basic Usage

```bash
python -m sticker_to_emoji <sticker_pack_name>
```

### With Options

```bash
# Custom name for emoji pack
python -m sticker_to_emoji MyStickerPack -n "My Cool Emojis"

# Limit number of emojis (default: 50)
python -m sticker_to_emoji MyStickerPack -l 30

# Save converted files locally
python -m sticker_to_emoji MyStickerPack --save-local

# Save to specific directory
python -m sticker_to_emoji MyStickerPack --save-local -o ./my_emojis

# Combined
python -m sticker_to_emoji MyStickerPack -n "Custom Pack" -l 25 --save-local
```

### Finding Sticker Pack Names

1. Open any sticker from the pack in Telegram
2. Right-click → "View Sticker Set" (or tap pack name on mobile)
3. Look at the URL: `t.me/addstickers/NAME`
4. Use `NAME` as the pack name

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_API_ID` | Your Telegram API ID | Yes |
| `TELEGRAM_API_HASH` | Your Telegram API hash | Yes |
| `TELEGRAM_BOT_TOKEN` | Your bot token from @BotFather | Yes |
| `TELEGRAM_USER_ID` | Your Telegram user ID | Yes |

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--name` | `-n` | Custom name for emoji pack | Pack title |
| `--limit` | `-l` | Max number of emojis | 50 |
| `--help` | `-h` | Show help message | - |
| `--save-local` | - | Save converted files locally | False |
| `--output` | `-o` | Output directory for saved files | ./emojis |

## 📸 Examples

### Convert Static Stickers
```bash
python -m sticker_to_emoji YourStickerPack
```

Output:
```
🎨 Sticker to Emoji Converter

📦 Fetching sticker pack: YourStickerPack
📊 Found 50 stickers in 'Cool Stickers'
  1/50: 😕 ✓
  2/50: 🎸 ✓
  ...
  50/50: 📞 ✓

✅ Converted 50 stickers

🚀 Creating emoji pack...
📝 Creating pack with 50 emojis...

✅ Success! Emoji pack created!
🔗 https://t.me/addemoji/YourPack_by_YourBot

💡 Add this pack in Telegram and use emojis as reactions!
```

### Convert Animated Stickers (TGS)
```bash
python -m sticker_to_emoji AnimatedPack -l 10
```

Animated (TGS) stickers are converted to **WEBM animated emojis** automatically! If ffmpeg is not available or conversion fails, the tool falls back to rendering the first frame as PNG.

### Save Converted Files Locally
```bash
python -m sticker_to_emoji MyStickerPack --save-local -o ./my_collection
```

This keeps all converted emoji files on your disk while still creating the Telegram pack.

## 🛠 How It Works

1. **Fetch** - Downloads sticker pack from Telegram using Telethon
2. **Convert** - Processes stickers:
   - Static (WEBP/PNG): Resizes and centers on transparent background
   - Animated (TGS): Converts Lottie to WEBM with VP9 codec (max 3s, ~64KB)
   - Video (WEBM): Passes through directly
   - Fallback: Renders first frame as PNG if WEBM conversion fails
3. **Upload** - Uploads converted files to Telegram Bot API
4. **Create** - Creates custom emoji pack with Bot API (supports animated emojis!)
5. **Save** - Optionally saves files locally with `--save-local`
6. **Cleanup** - Removes temporary files (unless saved locally)

## 🐛 Troubleshooting

### "Could not retrieve sticker pack"
- Check that the pack name is correct
- Make sure the pack is public
- Try the full URL: `t.me/addstickers/packname`

### "Missing environment variables"
- Make sure `.env` file exists in project root
- Check that all 4 variables are set
- Ensure no quotes around values in `.env`

### "SSL Certificate Error"
- The tool automatically handles SSL issues
- If problems persist, try updating Python

### "No emojis to upload"
- Check if pack has static stickers (animated ones are converted to first frame)
- Try a different sticker pack
- Check console output for specific errors

### Authentication Issues
- Delete `*.session` files
- Run again and re-authenticate

## 🎯 Use Cases

- **Personal Collections** - Convert favorite sticker packs to emojis
- **Team Branding** - Create custom emoji packs for communities
- **Reaction Packs** - Build emoji sets for specific purposes
- **Backup** - Save sticker packs as portable emoji format

## 🌟 Why Use This?

- ✅ Custom emojis work in **any chat** (with Premium)
- ✅ Use as **reactions** on messages
- ✅ **Smaller** than full sticker packs
- ✅ **Share** easily with friends
- ✅ Works with **group emoji sets**

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Telethon](https://github.com/LonamiWebs/Telethon) - Telegram client library
- [rlottie-python](https://github.com/laggykiller/rlottie-python) - TGS rendering
- [Pillow](https://python-pillow.org/) - Image processing

## 📞 Support

- 🐛 Found a bug? [Open an issue](https://github.com/yourusername/tg-sticker-to-emoji/issues)
- 💡 Have an idea? [Start a discussion](https://github.com/yourusername/tg-sticker-to-emoji/discussions)
- ❓ Questions? Check [existing issues](https://github.com/yourusername/tg-sticker-to-emoji/issues)

---

Made with ❤️ by the Telegram community
