try:
    from selenium import webdriver
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.keys import Keys as keys
    from selenium.webdriver.common.by import By as by
    from VisionAlpha import constant
except ImportError:
    from selenium import webdriver
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.common.keys import Keys as keys
    from selenium.webdriver.common.by import By as by
    from VisionAlpha import constant



b = webdriver.Firefox()
b.get('https://www.investing.com/currencies/eur-usd-technical')
wait = WebDriverWait(b,90)

span = '//div[id="techStudiesInnerWrap"]/div[class="summary"]/span[class="neutral uppercaseText"]'

box = wait.until(EC.presence_of_element_located((by.XPATH,span)))
print(box.text)
