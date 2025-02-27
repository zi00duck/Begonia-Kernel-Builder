import asyncio
import os
import sys
from telethon import TelegramClient

# Environment Variables
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
COMMIT_URL = os.environ.get("COMMIT_URL")
COMMIT_MESSAGE = os.environ.get("COMMIT_MESSAGE")
RUN_URL = os.environ.get("RUN_URL")
TITLE = os.environ.get("TITLE")
VERSION = os.environ.get("VERSION")
KERNEL_NAME = os.environ.get("KERNEL_NAME")
KERNEL_DEVICE = os.environ.get("KERNEL_DEVICE")
BUILD_DATE = os.environ.get("builddate")
KERNELSU_VERSION = os.environ.get("KERNELSU_NEXT_VERSION", "Unknown")

# Mesaj Şablonu
MSG_TEMPLATE = """
**{title} - {version}**
```
{commit_message}
```
[Commit]({commit_url}) | [Workflow]({run_url})

**Build Details:**
- Kernel Name: {kernel_name}
- Device: {device}
- Build Date: {build_date}
- KernelSU-Next Version: {ksu_version}
- SUSFS: Supported
- Mountify: Supported

**Download KSU-Next Manager:**
[Stable](https://github.com/KernelSU-Next/KernelSU-Next/releases/latest) || [Nightly](https://nightly.link/KernelSU-Next/KernelSU-Next/workflows/build-manager/next/manager)

Build With [Begonia-Kernel-Builder](https://github.com/cvnertnc/Begonia-Kernel-Builder)

By @the_CEHunter | [cvnertnc](https://github.com/cvnertnc)
""".strip()

def get_caption():
    msg = MSG_TEMPLATE.format(
        title=TITLE,
        version=VERSION,
        commit_message=COMMIT_MESSAGE,
        commit_url=COMMIT_URL,
        run_url=RUN_URL,
        kernel_name=KERNEL_NAME,
        device=KERNEL_DEVICE,
        build_date=BUILD_DATE,
        ksu_version=KERNELSU_VERSION
    )
    return msg[:1024] if len(msg) > 1024 else msg

def check_environ():
    required_vars = {
        "BOT_TOKEN": BOT_TOKEN,
        "CHAT_ID": CHAT_ID,
        "COMMIT_URL": COMMIT_URL,
        "COMMIT_MESSAGE": COMMIT_MESSAGE,
        "RUN_URL": RUN_URL,
        "TITLE": TITLE,
        "VERSION": VERSION,
        "KERNEL_NAME": KERNEL_NAME,
        "KERNEL_DEVICE": KERNEL_DEVICE,
        "builddate": BUILD_DATE
    }
    
    for var, value in required_vars.items():
        if value is None:
            print(f"[-] Missing {var}")
            exit(1)
    
    try:
        int(CHAT_ID)
    except ValueError:
        print("[-] Invalid CHAT_ID")
        exit(1)

async def main():
    print("[+] Starting Telegram upload")
    check_environ()
    
    files = sys.argv[1:]
    if not files:
        print("[-] No kernel files found")
        exit(1)
    
    print(f"[+] Found {len(files)} kernel files")
    
    caption = get_caption()
    
    print("[+] Final caption:\n---")
    print(caption)
    print("---")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    session_dir = os.path.join(script_dir, "ksunextbot.session")
    
    async with TelegramClient(session_dir, API_ID, API_HASH).start(bot_token=BOT_TOKEN) as bot:
        await bot.send_file(
            entity=int(CHAT_ID),
            file=files,
            caption=caption,
            parse_mode="markdown",
            supports_streaming=True
        )
        print("[+] Upload completed successfully")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"[-] Critical error: {str(e)}")
        exit(1)