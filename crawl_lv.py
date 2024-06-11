from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Cài đặt và khởi chạy trình điều khiển Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Mở trang web
driver.get('https://map.busmap.vn/hn/route/12')

# Đợi trang web tải xong (có thể điều chỉnh thời gian này tùy thuộc vào tốc độ mạng)
time.sleep(5)  # Đợi 5 giây

# Tìm và nhấp vào nút "Xem lượt về" dựa trên văn bản của nó
backward_trip_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Xem lượt về')]")
backward_trip_button.click()

# Đợi trang web tải xong dữ liệu lượt về
time.sleep(5)  # Đợi 5 giây

# Tìm kiếm và trích xuất dữ liệu từ trang web
stations = driver.find_elements(By.CLASS_NAME, 'name')

# In ra các tên trạm
for station in stations:
    print(station.text)

# Đóng trình duyệt
driver.quit()
