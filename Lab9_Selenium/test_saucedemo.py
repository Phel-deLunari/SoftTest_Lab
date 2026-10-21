import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest

@pytest.fixture(scope="function")
def driver():
    # Khởi tạo ChromeDriver tự động
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# TC01: Đăng nhập thành công với tài khoản chuẩn
def test_tc01_login_success(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # Xác minh chuyển hướng đến trang kho hàng và có tiêu đề "Products"
    assert "inventory.html" in driver.current_url
    title_text = driver.find_element(By.CLASS_NAME, "title").text
    assert title_text == "Products"
    time.sleep(1)

# TC02: Đăng nhập thất bại do sai mật khẩu
def test_tc02_login_failed_wrong_password(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()
    
    # Xác minh hiển thị thông báo lỗi
    error_elem = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
    assert "Username and password do not match any user in this service" in error_elem.text
    time.sleep(1)

# TC03: Thêm sản phẩm đầu tiên vào giỏ hàng
def test_tc03_add_product_to_cart(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # Bấm nút Add to cart của sản phẩm đầu tiên
    add_btn = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    add_btn.click()
    
    # Xác minh badge giỏ hàng hiển thị số 1
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_badge.text == "1"
    time.sleep(1)

# TC04: Kiểm tra chi tiết sản phẩm hiển thị trong giỏ hàng
def test_tc04_verify_item_in_cart(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # Thêm sản phẩm và click vào biểu tượng giỏ hàng
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    # Xác minh đúng URL giỏ hàng và tên sản phẩm "Sauce Labs Backpack"
    assert "cart.html" in driver.current_url
    item_name = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
    assert item_name == "Sauce Labs Backpack"
    time.sleep(1)

# TC05: Đăng xuất khỏi hệ thống
def test_tc05_logout(driver):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # 1. Bấm mở menu bằng JavaScript click
    burger_btn = driver.find_element(By.ID, "react-burger-menu-btn")
    driver.execute_script("arguments[0].click();", burger_btn)
    time.sleep(1)
    
    # 2. Bấm Logout cũng bằng JavaScript click để bỏ qua animation overlay
    logout_link = driver.find_element(By.ID, "logout_sidebar_link")
    driver.execute_script("arguments[0].click();", logout_link)
    time.sleep(1)
    
    # 3. Xác minh đã về trang đăng nhập
    login_btn = driver.find_element(By.ID, "login-button")
    assert login_btn.is_displayed()