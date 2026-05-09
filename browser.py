import os
import unittest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://selenium.dev/"
REPORT_DIR = os.path.dirname(os.path.abspath(__file__))


class SeleniumDevSiteTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.results = []

    @classmethod
    def tearDownClass(cls):
        cls._save_reports()
        input("\nBrowser is still open. Press Enter to close...")
        cls.driver.quit()

    def record(self, name, passed, detail=""):
        self.results.append({"name": name, "passed": passed, "detail": detail})

    def test_01_page_title(self):
        self.driver.get(BASE_URL)
        title = self.driver.title
        passed = "Selenium" in title
        self.record("Page title contains 'Selenium'", passed, f"Title: {title}")
        self.assertIn("Selenium", title)

    def test_02_page_loads(self):
        self.driver.get(BASE_URL)
        wait = WebDriverWait(self.driver, 10)
        body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        passed = body is not None
        self.record("Page body loads successfully", passed)
        self.assertTrue(passed)

    def test_03_navigation_links_present(self):
        self.driver.get(BASE_URL)
        links = self.driver.find_elements(By.TAG_NAME, "a")
        passed = len(links) > 0
        self.record("Navigation links are present", passed, f"Found {len(links)} links")
        self.assertGreater(len(links), 0)

    def test_04_no_broken_page(self):
        self.driver.get(BASE_URL)
        source = self.driver.page_source
        passed = "404" not in self.driver.title and len(source) > 100
        self.record("Page is not a 404 or empty", passed)
        self.assertTrue(passed)

    def test_05_screenshot_and_source_saved(self):
        self.driver.get(BASE_URL)
        screenshot_path = os.path.join(REPORT_DIR, "report_screenshot.png")
        source_path = os.path.join(REPORT_DIR, "report_page.html")

        self.driver.save_screenshot(screenshot_path)
        with open(source_path, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)

        passed = os.path.exists(screenshot_path) and os.path.exists(source_path)
        self.record("Screenshot and page source saved", passed,
                    f"Screenshot: {screenshot_path} | Source: {source_path}")
        self.assertTrue(passed)

    def test_06_url_is_correct(self):
        self.driver.get(BASE_URL)
        current_url = self.driver.current_url
        passed = current_url.startswith("https://selenium.dev")
        self.record("URL matches expected base URL", passed, f"URL: {current_url}")
        self.assertTrue(passed)

    def test_07_page_has_images(self):
        self.driver.get(BASE_URL)
        images = self.driver.find_elements(By.TAG_NAME, "img")
        passed = len(images) > 0
        self.record("Page contains images", passed, f"Found {len(images)} image(s)")
        self.assertGreater(len(images), 0)

    def test_08_page_has_headings(self):
        self.driver.get(BASE_URL)
        headings = self.driver.find_elements(By.XPATH, "//h1 | //h2 | //h3")
        passed = len(headings) > 0
        texts = [h.text.strip() for h in headings if h.text.strip()][:3]
        self.record("Page contains headings (h1/h2/h3)", passed,
                    f"Found {len(headings)} heading(s). First: {texts}")
        self.assertGreater(len(headings), 0)

    def test_09_page_has_favicon(self):
        self.driver.get(BASE_URL)
        favicons = self.driver.find_elements(
            By.XPATH, "//link[contains(@rel,'icon')]"
        )
        passed = len(favicons) > 0
        self.record("Page has a favicon link", passed,
                    f"Found {len(favicons)} favicon link(s)")
        self.assertGreater(len(favicons), 0)

    def test_10_docs_link_exists(self):
        self.driver.get(BASE_URL)
        links = self.driver.find_elements(By.TAG_NAME, "a")
        hrefs = [l.get_attribute("href") or "" for l in links]
        docs_links = [h for h in hrefs if "docs" in h.lower() or "documentation" in h.lower()]
        passed = len(docs_links) > 0
        self.record("Docs/Documentation link is present", passed,
                    f"Found {len(docs_links)} docs link(s)")
        self.assertGreater(len(docs_links), 0)

    def test_11_page_has_meta_description(self):
        self.driver.get(BASE_URL)
        metas = self.driver.find_elements(
            By.XPATH, "//meta[@name='description']"
        )
        passed = len(metas) > 0 and bool(metas[0].get_attribute("content"))
        content = metas[0].get_attribute("content") if metas else "Not found"
        self.record("Page has meta description", passed, f"Content: {content[:80]}")
        self.assertTrue(passed)

    def test_12_page_responsive_viewport(self):
        self.driver.get(BASE_URL)
        self.driver.set_window_size(375, 812)  # iPhone viewport
        body = self.driver.find_element(By.TAG_NAME, "body")
        passed = body.is_displayed()
        self.record("Page is visible at mobile viewport (375x812)", passed)
        self.driver.maximize_window()
        self.assertTrue(passed)

    def test_13_no_js_errors_in_console(self):
        self.driver.get(BASE_URL)
        logs = self.driver.get_log("browser")
        severe_errors = [l for l in logs if l.get("level") == "SEVERE"]
        passed = len(severe_errors) == 0
        detail = "; ".join(e["message"][:80] for e in severe_errors) if severe_errors else "None"
        self.record("No SEVERE JavaScript console errors", passed,
                    f"Errors: {detail}")
        self.assertEqual(len(severe_errors), 0,
                         f"SEVERE console errors found: {severe_errors}")

    def test_14_download_page_reachable(self):
        download_url = "https://selenium.dev/downloads/"
        self.driver.get(download_url)
        wait = WebDriverWait(self.driver, 10)
        body = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        passed = body is not None and "404" not in self.driver.title
        self.record("Downloads page is reachable", passed,
                    f"Title: {self.driver.title}")
        self.assertTrue(passed)

    def test_15_back_navigation_works(self):
        self.driver.get(BASE_URL)
        links = self.driver.find_elements(By.TAG_NAME, "a")
        internal = [l for l in links if (l.get_attribute("href") or "").startswith("https://selenium.dev/")]
        if not internal:
            self.record("Back navigation after following link", False, "No internal links found")
            self.fail("No internal links found")
        internal[0].click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        self.driver.back()
        WebDriverWait(self.driver, 10).until(EC.url_to_be(BASE_URL))
        passed = self.driver.current_url == BASE_URL
        self.record("Back navigation returns to home page", passed,
                    f"URL after back: {self.driver.current_url}")
        self.assertTrue(passed)

    @classmethod
    def _save_reports(cls):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        passed = sum(1 for r in cls.results if r["passed"])
        failed = len(cls.results) - passed

        rows = ""
        for r in cls.results:
            status = "PASS" if r["passed"] else "FAIL"
            color = "#2ecc71" if r["passed"] else "#e74c3c"
            rows += (
                f"<tr>"
                f"<td>{r['name']}</td>"
                f"<td style='color:{color};font-weight:bold'>{status}</td>"
                f"<td>{r['detail']}</td>"
                f"</tr>\n"
            )

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Selenium Test Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 30px; background: #f4f4f4; }}
    h1 {{ color: #333; }}
    .summary {{ margin: 10px 0 20px; font-size: 1.1em; }}
    table {{ border-collapse: collapse; width: 100%; background: #fff; }}
    th, td {{ border: 1px solid #ccc; padding: 10px 14px; text-align: left; }}
    th {{ background: #3a3a3a; color: #fff; }}
    tr:nth-child(even) {{ background: #f9f9f9; }}
  </style>
</head>
<body>
  <h1>Selenium Test Report</h1>
  <div class="summary">
    Run at: <strong>{timestamp}</strong> &nbsp;|&nbsp;
    Total: <strong>{len(cls.results)}</strong> &nbsp;|&nbsp;
    <span style="color:#2ecc71">Passed: <strong>{passed}</strong></span> &nbsp;|&nbsp;
    <span style="color:#e74c3c">Failed: <strong>{failed}</strong></span>
  </div>
  <table>
    <thead><tr><th>Test Case</th><th>Result</th><th>Detail</th></tr></thead>
    <tbody>
{rows}    </tbody>
  </table>
</body>
</html>"""

        report_path = os.path.join(REPORT_DIR, "report_page.html")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\nHTML report saved: {report_path}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
