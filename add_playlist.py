import os
import sys
from playwright.sync_api import sync_playwright

def main():
    m3u_url = os.environ.get("M3U_URL")
    mac_address = os.environ.get("MAC_ADDRESS", "F8:01:B4:8C:AF:20")
    playlist_name = os.environ.get("PLAYLIST_NAME", "My Playlist")

    if not m3u_url:
        print("خطأ: لم يتم تزويد رابط M3U!")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # استخدام المتصفح مع ضبط الأبعاد
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        print("جاري فتح الصفحة...")
        page.goto("https://smartone-iptv.com/plugin/smart_one/main_generate")

        print("تعبئة البيانات...")
        page.fill("input[name='mac']", mac_address)
        page.fill("input[name='name']", playlist_name)
        page.fill("input[name='url']", m3u_url)

        # التعامل مع حماية Cloudflare / Turnstile
        print("انتظار التحقق من الكابتشا (Cloudflare/Turnstile)...")
        try:
            # الانتظار حتى يتم حل الكابتشا تلقائيًا أو إتاحة زر الإرسال
            page.wait_for_selector("button:has-text('Add Playlist'):not([disabled])", timeout=20000)
        except Exception:
            print("تنبيه: الكابتشا تتطلب حلًا تفاعليًا أو انتظر وقتًا إضافيًا.")

        print("الضغط على زر الإرسال...")
        page.click("button:has-text('Add Playlist')")
        
        page.wait_for_timeout(5000)
        print("تمت العملية بنجاح!")
        browser.close()

if __name__ == "__main__":
    main()
