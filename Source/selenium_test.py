from selenium import webdriver


#TODO: This needs to be automated and downloaded into application 
browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver_win32\chromedriver.exe')


browser.get('http://seleniumhq.org/')