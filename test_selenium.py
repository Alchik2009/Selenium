import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from settings import email, password



# Run test
# pytest -v --driver Chrome --driver-path C:\\Users\\Admin\\PycharmProjects\\chromedriver.exe tests\test_selenium.py

@pytest.fixture(autouse=True)
def test_login():
    pytest.driver = webdriver.Chrome('C:\\Users\\Admin\\PycharmProjects\\chromedriver.exe')
    pytest.driver.get('http://petfriends1.herokuapp.com/login')

    yield

    pytest.driver.quit()


def test_all_pets():
    # вводим логин и пароль
    pytest.driver.find_element_by_id("email").send_keys(email)
    pytest.driver.find_element_by_id("pass").send_keys(password)

    # нажимаем на кнопку Войти
    pytest.driver.find_element_by_xpath("//button[@type='submit']").click()

    pytest.driver.implicitly_wait(10)

    #переходим на страницу со списком питомцев пользователя
    pytest.driver.find_element_by_xpath('//a[contains(text(), "Мои питомцы")]').click()

    #получаем количество питомцев из статистики
    a = pytest.driver.find_element_by_css_selector('div.\\.col-sm-4.left').text
    count_of_my_pets = a.split()

    #получаем количество строк из таблицы Все мои питомцы
    all_my_pets = pytest.driver.find_elements_by_tag_name('tbody\\tr')

    # получаем количество питомцев с фото
    images = pytest.driver.find_elements_by_tag_name('img')

    #получаем имена, возраст, породу через список питомцев
    value_of_my_pets = pytest.driver.find_elements_by_tag_name('td') # получаем данные из таблицы

    names = value_of_my_pets[::4] # извлекаем имена
    breed = value_of_my_pets[1:-1:4] # извлекаем породу
    age = value_of_my_pets[2:-1:4] # извлекаем возраст
    

    # Проверки:
    # Присутствуют все питомцы,
    # у половины питомцев есть фото,
    # У всех питомцев есть имя, возраст и порода,
    # У всех питомцев разные имена,
    # В списке нет повторяющихся питомцев
    for i in range(len(all_my_pets)):
        assert len(all_my_pets) is int(count_of_my_pets[(2)])
        assert len(images[i].get_attribute('src') != '') / len(all_my_pets) > 0,5
        assert '' not in value_of_my_pets
        assert len(names) is len(set(names))
        assert set.intersection(list(names + breed + age)) == 0




