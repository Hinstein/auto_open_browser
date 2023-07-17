from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def login(driver_path, debugger_address, password, input_value):
    options = Options()

    options.add_experimental_option("debuggerAddress", debugger_address)

    # 创建Chrome浏览器驱动程序的Service对象
    service = Service(driver_path)

    # 创建Chrome浏览器实例
    driver = webdriver.Chrome(service=service, options=options)

    # 在新窗口中打开网页
    driver.execute_cdp_cmd('Target.createTarget', {'url': url})

    # 获取打开的多个窗口句柄
    windows = driver.window_handles
    # 切换到当前最新打开的窗口
    driver.switch_to.window(windows[-1])

    # 打印当前页面的标题和URL，以及是否成功定位到输入框元素
    print("Page Title:", driver.title)
    print("Page URL:", driver.current_url)

    # 等待输入框加载完成
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='password']")))

    # 输入要填充的值
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

    page_list = input_value.split(',')

    for page in page_list:
        print('正在打开：', page)
        driver.execute_cdp_cmd('Target.createTarget', {'url': page})


# 自定义驱动路径和调试地址
driver_path = "/Users/lilinhai/Library/Application Support/bitbrowser/chromedriver/112/chromedriver"
debugger_address = "127.0.0.1:55602"
url = "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#"
input_locator = ("css selector", "#password")
input_text = "1233333"
