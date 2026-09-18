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
            viewport={"width": 1280, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print("جاري فتح الصفحة...")
        page.goto("https://smartone-iptv.com/plugin/smart_one/main_generate", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)

        print("تحديد واختيار قسم M3u Playlist...")
        # الضغط الفعلي على أيقونة M3u Playlist لتنشيط النموذج الخاص بها
        m3u_tab = page.locator("div, p, span, a").filter(has_text="M3u Playlist").last
        m3u_tab.click()
        page.wait_for_timeout(2000)

        print("تعبئة البيانات في النموذج النشط...")
        
        # اختيار العناصر المرئية حصراً (.filter(has_not_class="hidden") أو إيجاد الحقل المرئي)
        visible_mac_input = page.locator("input#mac:visible, input[name='mac']:visible").first
        visible_mac_input.fill(mac_address)

        visible_name_input = page.locator("input[placeholder*='Vip']:visible, input[name='name']:visible").first
        visible_name_input.fill(playlist_name)

        visible_url_input = page.locator("input[placeholder*='http']:visible, input[name='url']:visible").first
        visible_url_input.fill(m3u_url)

        print("انتظار التحقق من الكابتشا والجاهزية...")
        page.wait_for_timeout(5000)

        print("الضغط على زر Add Playlist المرئي...")
        submit_btn = page.locator("button:has-text('Add Playlist'):visible").first
        submit_btn.scroll_into_view_if_needed()
        submit_btn.click()

        print("تم إرسال البيانات بنجاح!")
        page.wait_for_timeout(5000)
        browser.close()

if __name__ == "__main__":
    main()
