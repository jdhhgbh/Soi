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
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print("جاري فتح الصفحة...")
        page.goto("https://smartone-iptv.com/plugin/smart_one/main_generate", wait_until="domcontentloaded", timeout=60000)

        page.wait_for_timeout(3000)

        print("محاولة إظهار قسم M3U Playlist...")
        # النقر على تبويب M3U في حال وجود تبويبات مفعلة
        try:
            tab_btn = page.locator("a:has-text('M3u Playlist'), button:has-text('M3u Playlist'), :text('M3u Playlist')").first
            if tab_btn.is_visible():
                tab_btn.click()
                page.wait_for_timeout(1000)
        except Exception as e:
            print(f"تخطي اختيار التبويب: {e}")

        print("تعبئة البيانات...")
        # استخدام force=True لتعبئة الحقول حتى لو كانت مخفية بحيل CSS
        mac_input = page.locator("input#mac, input.mac-1").first
        mac_input.fill(mac_address, force=True)

        name_input = page.locator("input[name='name'], input[placeholder*='Vip']").first
        name_input.fill(playlist_name, force=True)

        url_input = page.locator("input[name='url'], input[placeholder*='http']").first
        url_input.fill(m3u_url, force=True)

        print("انتظار التحقق وإرسال النموذج...")
        page.wait_for_timeout(4000)

        submit_btn = page.locator("button:has-text('Add Playlist')").first
        submit_btn.click(force=True)

        print("تم إرسال الطلب بنجاح!")
        page.wait_for_timeout(5000)
        browser.close()

if __name__ == "__main__":
    main()
