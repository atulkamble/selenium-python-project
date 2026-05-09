# Selenium Project Setup on WSL (Ubuntu)

## 📌 Install Required Packages

```bash
sudo apt update -y

sudo apt install git python3 python3-pip -y
```

---

## 📌 Verify Installation

```bash
python3 --version
pip3 --version
git --version
```

---

## 📌 Install Google Chrome

### Add Google Chrome Repository

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

### Install Chrome

```bash
sudo apt install ./google-chrome-stable_current_amd64.deb -y
```

---

## 📌 Verify Chrome Installation

```bash
google-chrome --version
```

---

## 📌 Install Selenium Python Package

```bash
pip3 install -U selenium
```

---

## 📌 Clone Project Repository

```bash
git clone https://github.com/atulkamble/azure-test-plans.git
```

---

## 📌 Navigate to Selenium Project

```bash
cd azure-test-plans/selenium
```

---

# 📌 Create Selenium Python Script

## Create File

```bash
touch browser.py
```

## Open File

```bash
nano browser.py
```

---

# 📌 Add Selenium Code

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.selenium.dev/")

print(driver.title)

driver.quit()
```

---

# 📌 View File Content

```bash
cat browser.py
```

---

# 📌 Run Selenium Script

```bash
python3 browser.py
```

---

# 📌 Expected Output

```bash
Selenium
```

---

# 📌 Important Corrections & Fixes

## ❌ Incorrect Commands

```bash
sudo apt install python3-pip3 -y
```

✅ Correct:

```bash
sudo apt install python3-pip -y
```

---

```bash
sudo apt serach chrome-browser
```

✅ Correct:

```bash
sudo apt search google-chrome
```

---

```bash
sudo apt instal chrome-browser
```

✅ Correct:

```bash
sudo apt install ./google-chrome-stable_current_amd64.deb -y
```

---

```bash
nano browser .py
```

✅ Correct:

```bash
nano browser.py
```

---

```bash
cat brrowser.py
```

✅ Correct:

```bash
cat browser.py
```

---

# 📌 Why Headless Mode?

WSL normally does not have a GUI browser environment.
Using:

```python
chrome_options.add_argument("--headless")
```

allows Chrome to run in background mode without opening a browser window.

---

# 📌 Recommended Project Structure

```text
azure-test-plans/
└── selenium/
    ├── browser.py
    ├── requirements.txt
    └── README.md
```

---

# 📌 Create requirements.txt

```bash
pip3 freeze > requirements.txt
```

---

# 📌 Install Dependencies Later

```bash
pip3 install -r requirements.txt
```

---

# 📌 Common Selenium Issues in WSL

## Chrome Not Opening

Install Chrome correctly and use headless mode.

---

## Driver Version Mismatch

Latest Selenium automatically manages ChromeDriver.

Upgrade Selenium:

```bash
pip3 install -U selenium
```

---

## Permission Issues

```bash
chmod +x browser.py
```

---
