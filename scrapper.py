#source .venv/bin/activate
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

#Crome Options /suppress pop-up
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (sometimes needed)
chrome_options.add_argument("--no-sandbox")

def body():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://nvd.nist.gov/vuln/detail/CVE-2026-32711")
    #page = requests.get(URL)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    #print(soup)
    #body = soup.find("div", class_="container", id="body-section")
    body = soup.find(attrs={"data-testid": "vuln-description"})
    return body.get_text(strip=True)

def exploits():
    driver = webdriver.Chrome(options=chrome_options)  # Add your options if needed
    driver.get("https://nvd.nist.gov/vuln/detail/CVE-2026-32711")
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", {
        "class": "table table-striped table-condensed table-bordered detail-table",
        "data-testid": "vuln-hyperlinks-table"
    })
    
    text = table.get_text(separator="\n")  # Use separator to keep lines
    driver.quit()
    
    # Normalize whitespace
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    
    # Parse into structured records
    records = []
    i = 0
    while i < len(lines):
        if re.match(r'https?://', lines[i]):  # URL detected
            record = {"URL": lines[i]}
            i += 1
            # Source(s)
            record["Source(s)"] = lines[i] if i < len(lines) else ""
            i += 1
            # Tags: consume until next URL or end
            tags = []
            while i < len(lines) and not re.match(r'https?://', lines[i]):
                tags.append(lines[i])
                i += 1
            record["Tag(s)"] = tags
            records.append(record)
        else:
            i += 1
    
    return records

#print(exploits())