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
        # تشغيل المتصفح مع إعدادات لتجاوز الحجب
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
        # استخدام domcontentloaded لتفادي التعليق في networkidle
        page.goto("https://smartone-iptv.com/plugin/smart_one/main_generate", wait_until="domcontentloaded", timeout=60000)

        print("انتظار تحميل عناصر الصفحة...")
        # استهداف المدخلات الدقيقة بناءً على الـ class والـ id
        mac_input = page.locator("input#mac, input.mac-1").first
        mac_input.wait_for(state="visible", timeout=30000)

        print("تعبئة البيانات...")
        mac_input.fill(mac_address)

        # تعبئة اسم القائمة والرابط
        page.locator("input[name='name'], input[placeholder*='Vip']").first.fill(playlist_name)
        page.locator("input[name='url'], input[placeholder*='http']").first.fill(m3u_url)

        print("انتظار التحقق وإمكانية الضغط على الزر...")
        page.wait_for_timeout(5000) # مهلة لضمان استقرار التحقق من Cloudflare

        submit_btn = page.locator("button:has-text('Add Playlist')").first
        submit_btn.scroll_into_view_if_needed()
        submit_btn.click()

        print("تم إرسال الطلب بنجاح!")
        page.wait_for_timeout(5000)
        browser.close()

if __name__ == "__main__":
    main()
