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
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print("جاري فتح الصفحة...")
        page.goto("https://smartone-iptv.com/plugin/smart_one/main_generate", wait_until="networkidle")

        print("انتظار ظهور حقل الـ MAC...")
        # الانتظار والتفاعل باستخدام الـ ID المحدد بشكل دقيق
        mac_input = page.locator("#mac")
        mac_input.wait_for(state="visible", timeout=30000)
        
        # التمرير للحقل للتأكد من رؤيته
        mac_input.scroll_into_view_if_needed()

        print("تعبئة البيانات...")
        mac_input.fill(mac_address)

        # استهداف باقي الحقول إما بالـ ID أو بالـ Placeholder المباشر
        page.locator("input[placeholder='Vip List']").fill(playlist_name)
        page.locator("input[placeholder='http://my-server.com/playlist_file.m3u']").fill(m3u_url)

        print("انتظار التحقق من الكابتشا (Cloudflare/Turnstile)...")
        try:
            # الانتظار حتى يصبح زر الإرسال نشطًا وقابلاً للضغط
            submit_btn = page.locator("button:has-text('Add Playlist')")
            submit_btn.wait_for(state="visible", timeout=20000)
            submit_btn.click()
            print("تم الضغط على زر الإرسال بنجاح.")
        except Exception as e:
            print(f"حدث خطأ أثناء الضغط على الزر: {e}")

        page.wait_for_timeout(5000)
        browser.close()

if __name__ == "__main__":
    main()
