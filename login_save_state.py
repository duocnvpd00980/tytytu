
from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://chat.openai.com/")
    print("Vui lòng đăng nhập ChatGPT trên trình duyệt.")
    input("Nhấn Enter khi đã login xong...")
    context.storage_state(path="storage_state.json")
    print("Đã lưu storage_state.json")
    browser.close()
