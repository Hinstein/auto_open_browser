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

    # 登陆小狐狸钱包
    login_metamask(driver, password)

    # 打开网页
    open_page(driver, input_value)


def open_page(driver, input_value):
    if len(input_value) != 0:
        page_list = input_value.split(',')
        for page in page_list:
            print('正在打开：', page)
            driver.execute_cdp_cmd('Target.createTarget', {'url': page})


def login_metamask(driver, password):
    # 在新窗口中打开网页
    driver.execute_cdp_cmd('Target.createTarget', {'url': metamask_url})
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


# metamask 路径
metamask_url = "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#"
