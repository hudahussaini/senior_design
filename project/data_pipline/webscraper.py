from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time



# Function to download PDFs on the current page
def download_pdfs(driver: webdriver):
    time.sleep(4)  # Wait for the page to load
    buttons = driver.find_elements(By.CLASS_NAME, 'readcube__pdfButton')
    for button in buttons:
        time.sleep(4)  # Wait to ensure download starts
        button.click()

def get_all_pdfs_from_experts_for_one_author(author_name: str):
    # Set up the Selenium WebDriver (this example uses Chrome)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
    "download.default_directory": f'/Users/hudahussaini/senior_design/data/downloads/{author_name}', #Change default directory for downloads
    "download.prompt_for_download": False, #To auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
    })

    driver = webdriver.Chrome(options=options)

    # Open the webpage
    driver.get('https://experts.umich.edu')
    time.sleep(2)

    # Locate the search input field
    search_box = driver.find_element(By.CSS_SELECTOR, 'input[type="search"][placeholder="Search by name or keyword"]')
    # Enter the search query
    search_query = author_name
    search_box.send_keys(search_query)

    # Press Enter to initiate the search
    search_box.send_keys(Keys.RETURN)
    time.sleep(4)
    try:    
        result_link = driver.find_element(By.XPATH, f'//a[contains(text(), "{author_name}")]')
    except:
        try:
            first_name, middle_name, last_name = author_name.split()
            result_link = driver.find_element(By.XPATH, f'//a[contains(text(), "{first_name} {last_name}")]')
        except:
            #tried without middle name and still cant find
            return print(f"Cannot find {author_name} on michigan experts")

    # Extract the href attribute
    href_value = result_link.get_attribute('href')


    #EXAMPLE: href="/6646-james-wagner"
    driver.get(f'{href_value}/publications')

    download_pdfs(driver=driver)
    count = 1
    time.sleep(4)  # Wait for the next page to load
    while True:
        try:
            # Try to find the next page button
            next_button = driver.find_element(By.CSS_SELECTOR, f'button[aria-label="Move to page {count+1}, the next page"]')
            next_button.click()
            download_pdfs(driver=driver)
            count += 1# Increment the counter to move to the next page
        except:
            try:
                # Try to find the last page button if the next page button is not found
                last_page_button = driver.find_element(By.CSS_SELECTOR, f'button[aria-label="Move to page {count+1}, the last page"]')
                last_page_button.click()
                time.sleep(4)  # Wait for the last page to load
                download_pdfs(driver=driver)
                break# Exit the loop after the last page is processed
            except:
                print("No more pages or unable to find the next page button.")
                break# Exit the loop if neither button is found# Optionally, close the browser after all pages are processed
    driver.quit()