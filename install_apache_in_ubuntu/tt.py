from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import urllib3
import certifi

# URL of the Selenium Grid hub
grid_url = "https://localhost:4444/wd/hub"

# Path to the self-signed certificate
cert_path = "path/to/your/selenium_grid_cert.crt"

# Add the certificate to the certifi trust store
with open(certifi.where(), 'a') as cert_file:
    with open(cert_path, 'r') as my_cert:
        cert_file.write(my_cert.read())

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-insecure-localhost')

# Create a custom HTTP request with the updated certifi trust store
class MyRemoteConnection(RemoteConnection):
    def __init__(self, remote_server_addr, keep_alive=True, resolve_ip=True):
        super().__init__(remote_server_addr, keep_alive=keep_alive, resolve_ip=resolve_ip)
        self._conn = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where()
        )

# Use the custom remote connection to create the Remote WebDriver
driver = webdriver.Remote(
    command_executor=MyRemoteConnection(grid_url),
    options=chrome_options
)

# Open a website (example: Google)
driver.get("https://www.google.com")

# Print the title of the webpage
print(driver.title)

# Close the browser
driver.quit()
