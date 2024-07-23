from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib3
import certifi
import ssl

# URL of the Selenium Grid hub
grid_url = "https://localhost:4444/wd/hub"

# Path to the self-signed certificate
cert_path = "path/to/your/selenium_grid_cert.crt"

# Add the certificate to the certifi trust store
with open(certifi.where(), 'a') as cert_file:
    with open(cert_path, 'r') as my_cert:
        cert_file.write(my_cert.read())

# Create a custom HTTPS connection that uses the updated certifi trust store
class VerifiedHTTPSConnection(urllib3.connection.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        kwargs['ssl_context'] = ssl.create_default_context(cafile=certifi.where())
        super().__init__(*args, **kwargs)

# Create a custom HTTPSConnectionPool that uses VerifiedHTTPSConnection
class VerifiedHTTPSConnectionPool(urllib3.connectionpool.HTTPSConnectionPool):
    ConnectionCls = VerifiedHTTPSConnection

# Create a custom PoolManager that uses VerifiedHTTPSConnectionPool
class VerifiedPoolManager(urllib3.PoolManager):
    def __init__(self, *args, **kwargs):
        kwargs['connection_pool_kw'] = kwargs.get('connection_pool_kw', {})
        kwargs['connection_pool_kw']['ConnectionCls'] = VerifiedHTTPSConnectionPool.ConnectionCls
        super().__init__(*args, **kwargs)

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-insecure-localhost')

# Create a new instance of the Remote WebDriver with Chrome options
driver = webdriver.Remote(
    command_executor=grid_url,
    options=chrome_options,
    http_client=VerifiedPoolManager()
)

# Open a website (example: Google)
driver.get("https://www.google.com")

# Print the title of the webpage
print(driver.title)

# Close the browser
driver.quit()
