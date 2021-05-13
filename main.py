from selenium import webdriver

driver = webdriver.Chrome(executable_path="C:\\New Softwares\\NewBrowserEXE\\chromedriver.exe")
driver.get("http://www.youtube.com")
PageTitle=driver.title
print(PageTitle)
assert "YouTube" in PageTitle
driver.quit()