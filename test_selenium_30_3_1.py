from selenium.webdriver.common.by import By
from selenium import webdriver
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('./driver/chromedriver.exe')
   pytest.driver.implicitly_wait(10)
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()

def test_show_my_pets():
   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys('valid_email')
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys('valid_pass')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Нажимаем кнопку Мои питомцы
   pytest.driver.find_element(By.XPATH, '//a[@href="/my_pets"]').click()

   # Просматриваем статистику пользователя
   stats = pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split()

   # Ставим ожидание загрузки таблицы с карточками питомев
   table_present = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "//table"))
   )
   assert table_present

   # Просматриваем таблицу с карточками питомцев
   number_of_str = pytest.driver.find_elements(By.XPATH, '//table/tbody/tr')

   # Сравниваем число из статистики с количеством питомцев в таблице
   assert int(stats [2]) == len(number_of_str)

   # Собираем массив с "ячейками" для фото
   number_of_img = pytest.driver.find_elements(By.XPATH, '//table//img')

   # Собираем массив из фото питомцев
   pets_with_photo = 0
   for el in number_of_img:
      src = el.get_attribute('src')
      if src:
         pets_with_photo += 1

   # Проверяем, что заполненных ячеек для фото больше половины
   if int(stats [2]) % 2 == 0:
      assert pets_with_photo >= int(stats [2]) / 2
   else:
      assert pets_with_photo >= (int(stats [2])+1) / 2

   # Собираем массив из текста в ячеках таблицы
   pet_details_td = pytest.driver.find_elements(By.XPATH, '//table//tr//td')
   pet_details_text = []
   for el in pet_details_td:
         pet_details_text.append(el.text)

   # Проверяем, что длина массива из заполненных ячеек равна количеству ячеек таблицы
   assert len(pet_details_text) == len(number_of_str) * 4
   names = []
   for el in pet_details_text[0::4]:
      names.append(el)

   assert len(set(names)) == len(names)















