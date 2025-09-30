
from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright
import threading, time

app = Flask(__name__)
LOCK = threading.Lock()

PLAYWRIGHT_BROWSER = None
PLAYWRIGHT_CONTEXT = None

def startup_playwright():
    global PLAYWRIGHT_BROWSER, PLAYWRIGHT_CONTEXT
    pw = sync_playwright().start()
    PLAYWRIGHT_BROWSER = pw.chromium.launch(
        headless=True, args=["--no-sandbox","--disable-dev-shm-usage"]
    )
    PLAYWRIGHT_CONTEXT = PLAYWRIGHT_BROWSER.new_context(
        storage_state="storage_state.json"
    )
    print("Playwright đã sẵn sàng.")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    if "message" not in data:
        return jsonify({"error": "Missing 'message'"}), 400
    message = data["message"]

    with LOCK:
        page = PLAYWRIGHT_CONTEXT.new_page()
        page.goto("https://chat.openai.com/chat")
        textarea = page.locator("textarea")
        textarea.wait_for(state="visible", timeout=15000)

        md = page.locator("div.markdown")
        before = md.count()

        textarea.fill(message)
        textarea.press("Enter")

        # Đợi message mới
        start = time.time()
        reply = None
        while time.time() - start < 30:
            time.sleep(0.5)
            after = md.count()
            if after > before:
                reply = md.nth(after-1).inner_text()
                if reply.strip() != "":
                    break

        page.close()
        if not reply:
            return jsonify({"error": "Timeout"}), 504
        return jsonify({"reply": reply})

if __name__ == "__main__":
    startup_playwright()
    app.run(host="0.0.0.0", port=5000)
