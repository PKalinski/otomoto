
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# opts = Options()
# opts.headless = True
# assert opts.headless  # Operating in headless mode
# browser = Firefox(options=opts)
# browser.implicitly_wait(10)
# browser.get('https://www.otomoto.pl/')




#
# browser.get("https://www.otomoto.pl/osobowe/od-2017/warszawa/?search%5Bfilter_enum_fuel_type%5D%5B0%5D=petrol&search%5Border%5D=created_at_first%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bdist%5D=50&search%5Bcountry%5D=")
# browser.save_full_page_screenshot("screenshot.png")
#
#
# with open ('website.html', 'w', encoding="utf-8") as file:
#     file.write (browser.page_source)
#
# try:
#     browser.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()
#     browser.save_full_page_screenshot("screenshot_2.png")
#
#     html_string = browser.page_source
#     with open ('website.html', 'w', encoding="utf-8") as file:
#         file.write (browser.page_source)
#
# finally:
#     browser.close()
#     browser.quit()