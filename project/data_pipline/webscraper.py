from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Set up the Selenium WebDriver (this example uses Chrome)
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
"download.default_directory": "/Users/hudahussaini/senior_design/data/downloads", #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})
driver = webdriver.Chrome(options=options)
# Open the webpage (replace with the actual URL)
driver.get('https://experts.umich.edu/6646-james-wagner/publications')

time.sleep(4)
# Find the button by its class name or other attributes and click it
buttons = driver.find_elements(By.CLASS_NAME, 'readcube__pdfButton')

for button in buttons:
    time.sleep(4)
    button.click()

time.sleep(4)

# Optionally, close the browser after the click
driver.quit()
