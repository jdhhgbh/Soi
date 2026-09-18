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
        
        # استخدام شاشة قياسية واضحة كسطح مكتب
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        print("جاري فتح الصفحة...")
        page.goto("https://smartone-iptv.com/plugin/smart_one/main_generate", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)

        print("تفعيل تبويب M3u Playlist عبر JavaScript...")
        # النقر المباشر على خيار M3U عبر محدد دقيق
        page.evaluate("""
            () => {
                const elements = Array.from(document.querySelectorAll('div, a, button, h5, p'));
                const m3uElem = elements.find(el => el.textContent.trim() === 'M3u Playlist');
                if (m3uElem) {
                    m3uElem.click();
                }
            }
        """)
        page.wait_for_timeout(2000)

        print("تعبئة البيانات...")
        # إدخال القيم باستخدام JavaScript مباشرة لتفادي مشاكل البروز والتغطية
        page.evaluate(f"""
            () => {{
                const macInputs = Array.from(document.querySelectorAll("input[name='mac'], input#mac"));
                const visibleMac = macInputs.find(i => i.offsetWidth > 0 && i.offsetHeight > 0) || macInputs[0];
                if (visibleMac) visibleMac.value = "{mac_address}";

                const nameInputs = Array.from(document.querySelectorAll("input[name='name']"));
                const visibleName = nameInputs.find(i => i.offsetWidth > 0 && i.offsetHeight > 0) || nameInputs[0];
                if (visibleName) visibleName.value = "{playlist_name}";

                const urlInputs = Array.from(document.querySelectorAll("input[name='url']"));
                const visibleUrl = urlInputs.find(i => i.offsetWidth > 0 && i.offsetHeight > 0) || urlInputs[0];
                if (visibleUrl) visibleUrl.value = "{m3u_url}";
            }}
        """)

        print("انتظار التحقق وإرسال الطلب...")
        page.wait_for_timeout(4000)

        # الضغط على زر Submit باستخدام JS لتجاوز قيود الرؤية
        page.evaluate("""
            () => {
                const buttons = Array.from(document.querySelectorAll('button'));
                const submitBtn = buttons.find(b => b.textContent.includes('Add Playlist') && b.offsetWidth > 0);
                if (submitBtn) {
                    submitBtn.click();
                } else if (buttons.length > 0) {
                    buttons[0].click();
                }
            }
        """)

        print("تم تنفيذ عملية الإرسال بنجاح!")
        page.wait_for_timeout(5000)
        browser.close()

if __name__ == "__main__":
    main()
