from playwright.sync_api import sync_playwright
from datetime import datetime
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

TARGET_DATE = datetime.strptime("2025-09-01", "%Y-%m-%d")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
target_url = os.getenv("TARGET_URL")
BLACKLIST_FILE = "blacklist.json"

def load_blacklist():
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, "r") as f:
            return json.load(f)
    return []

def send_discord_notification(slot_text, slot_date_str):
    message = {
        "content": f"📢 **New appointment available!**\n"
                  f"🗓️ `{slot_text}`\n"
                  f"🔗 To accept: `{target_url}`\n"
                  f"🛑 To blacklist: `!reject {slot_date_str}`"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=message)
    print("📨 Discord response status:", response.status_code)

def check_appointment():
    print("💡 Starting Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = browser.new_page()

        print("🌍 Opening the appointment page...")
        page.goto(os.getenv("TARGET_URL"), wait_until="networkidle")

        print("🖱️ Clicking the appropriate label...")
        page.locator("//b[text()='Ausländischen Führerschein umschreiben - EU/EWR']").click()
        page.keyboard.type("1")
        page.keyboard.press("Enter")

        print("⏳ Waiting for redirected page to load...")
        page.wait_for_selector("dt:text('Nächster Termin')")

        label = page.locator("dt:text('Nächster Termin')")
        date_value = label.locator("xpath=following-sibling::dd[1]")
        slot_text = date_value.inner_text()
        print(f"📅 Appointment text: {slot_text}")

        date_str = slot_text.replace("ab ", "").split(",")[0].strip()
        slot_date = datetime.strptime(date_str, "%d.%m.%Y")
        slot_date_str = slot_date.strftime('%Y-%m-%d')

        print(f"📆 Parsed date: {slot_date_str}")

        if slot_date < TARGET_DATE:
            blacklist = load_blacklist()
            if slot_date_str in blacklist:
                print(f"⚠️ {slot_date_str} is in the blacklist. Skipping notification.")
            else:
                print("🚨 Earlier appointment available!")
                send_discord_notification(slot_text, slot_date_str)
        else:
            print("🕓 No earlier appointment found.")

        browser.close()
        print("✅ Browser closed.")

if __name__ == "__main__":
    check_appointment()
