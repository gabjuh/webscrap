```markdown
# TerminCheckerBot

A Python-based Discord bot + appointment checker script to monitor appointment availability at the Bremen city website for converting EU/EEA driver's licenses. If an earlier appointment becomes available, it sends a Discord message. You can also reject dates via Discord commands, which prevents future alerts for those dates.

---

## 📦 Features

- ✅ Checks appointment availability via headless browser automation (Playwright)
- 📢 Sends Discord notifications when earlier dates appear
- 🛑 Supports blacklisting dates (`!reject`)
- ✅ View current blacklist (`!blacklist`)
- 🔄 Unblock blacklisted dates (`!unreject`)
- 🔐 Uses `.env` file to securely manage tokens and config

---

## 🚀 Installation

1. **Clone the repository** and navigate into the project folder:
   ```bash
   git clone https://github.com/yourname/TerminCheckerBot.git
   cd TerminCheckerBot
   ```

2. **Create virtual environment** and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Create a `.env` file** in the project root with the following content:
   ```env
   DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
   DISCORD_BOT_TOKEN=your-discord-bot-token
   DISCORD_CHANNEL_ID=123456789012345678
   TARGET_URL=https://termin.bremen.de/termine/select2?md=2
   ```

5. **Make sure `blacklist.json` exists** (optional but recommended):
   ```bash
   echo "[]" > blacklist.json
   ```

---

## 🔧 Project Files

| File              | Description                                     |
|-------------------|-------------------------------------------------|
| `check_termin.py` | Periodically checks for new appointments        |
| `listener.py`     | Discord bot that listens to commands            |
| `blacklist.json`  | Stores blocked appointment dates                |
| `.env`            | Stores API tokens and config securely           |
| `run.sh`          | Shortcut script to run `check_termin.py`        |
| `setup.sh`        | Script to set up environment & install deps     |

---

## 💬 Discord Bot Commands

| Command                | Description                              |
|------------------------|------------------------------------------|
| `!reject YYYY-MM-DD`   | Adds the date to the blacklist           |
| `!unreject YYYY-MM-DD` | Removes the date from the blacklist      |
| `!blacklist`           | Lists all currently blacklisted dates    |

Only messages in the channel specified by `DISCORD_CHANNEL_ID` will be processed.

---

## 🔁 Automation with `pm2`

If running on a server (e.g. Raspberry Pi), use `pm2` to keep the scripts running:

```bash
pm2 start check_termin.py --interpreter python3 --name termin-checker
pm2 start listener.py --interpreter python3 --name termin-listener
pm2 save
pm2 startup
```

---

## ✅ Usage

### Manual run:
```bash
source venv/bin/activate
python check_termin.py   # to test scraping
python listener.py       # to launch Discord bot
```

### Scheduled run with cron (alternative to pm2):
```cron
*/15 * * * * /full/path/to/run.sh >> /full/path/to/log.txt 2>&1
```

---

## 🔐 Security

- Never commit your `.env` file to Git!
- `.env` and `blacklist.json` are listed in `.gitignore` by default

---

## 🧩 Dependencies

- Python 3.9+
- Playwright
- Discord.py
- python-dotenv
- requests

Install with:

```bash
pip install -r requirements.txt
```

---

## 💡 Tips

- You can modify the `TARGET_DATE` in `check_termin.py` to define the date cutoff
- The system supports extension (e.g. `!clearblacklist`, per-user control)

---

## 📬 Support

Made with ❤️ by Gabesz

Feel free to fork, contribute, or suggest improvements.
```
