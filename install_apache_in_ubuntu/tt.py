from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# URL of the Selenium Grid hub
grid_url = "https://localhost:4444/wd/hub"

# Path to the self-signed certificate
cert_path = "path/to/your/selenium_grid_cert.crt"

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-insecure-localhost')

# Use --ignore-certificate-errors-spki-list to ignore the certificate
with open(cert_path, "r") as cert_file:
    cert_data = cert_file.read()

# Add the certificate to Chrome's trust store using the --ignore-certificate-errors-spki-list flag
import base64
import hashlib

cert_hash = hashlib.sha256(base64.b64decode(cert_data.strip())).digest()
chrome_options.add_argument(f'--ignore-certificate-errors-spki-list={base64.b64encode(cert_hash).decode()}')

# Create a new instance of the Remote WebDriver with Chrome options
driver = webdriver.Remote(
    command_executor=grid_url,
    options=chrome_options
)

# Open a website (example: Google)
driver.get("https://www.google.com")

# Print the title of the webpage
print(driver.title)

# Close the browser
driver.quit()
