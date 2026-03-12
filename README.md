# UI Tests for Automation Exercise Products Page

Автотесты для страницы продуктов сайта https://automationexercise.com/products.

Проект реализован на `pytest + selenium` с использованием паттерна `Page Object Model`.
Тесты покрывают базовые проверки страницы продуктов: загрузку страницы, поиск, карточки товаров, ссылки `View Product`, модальное окно корзины, категории и бренды в сайдбаре.

## Стек проекта

- Python 3.9+
- pytest
- selenium
- pytest-html
- Selenium Manager для автоматического поиска и запуска ChromeDriver

## Что проверяют тесты

Набор тестов покрывает следующие сценарии:

- доступность страницы `/products`
- корректность URL и title страницы
- наличие заголовка `All Products`
- отображение строки поиска и кнопки поиска
- наличие карточек товаров
- наличие имени, цены и изображения у товаров
- наличие ссылок `View Product`
- работу поиска по товарам
- открытие модального окна после `Add to cart`
- закрытие модального окна
- отображение блока категорий
- отображение блока брендов
- наличие ожидаемых брендов в сайдбаре
- переход на страницу деталей товара

## Структура проекта

```text
UI-tests/
├── conftest.py
├── requirements.txt
├── README.md
├── tests/
│   ├── __init__.py
│   └── test_products_page.py
└── ui/
	├── __init__.py
	└── pages/
		├── __init__.py
		├── base_page.py
		└── products_page.py
```

## Архитектура

Проект использует `Page Object Model`:

- `ui/pages/base_page.py` содержит базовые методы работы с Selenium WebDriver
- `ui/pages/products_page.py` описывает локаторы и действия для страницы продуктов
- `tests/test_products_page.py` содержит тестовые сценарии
- `conftest.py` содержит фикстуры pytest и настройки браузера

## Системные требования

Перед запуском на машине должны быть установлены:

- Python 3.9 или выше
- Google Chrome актуальной версии
- доступ в интернет для первого запуска Selenium Manager

Проверить версии можно так:

```bash
python3 --version
google-chrome --version
```

Для macOS команда проверки Chrome может отличаться. Можно использовать:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

Если команда недоступна, достаточно убедиться, что браузер Google Chrome установлен через Applications.

## Установка проекта с нуля

### 1. Клонировать репозиторий

```bash
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
cd UI-tests
```

### 2. Создать виртуальное окружение

```bash
python3 -m venv .venv
```

### 3. Активировать виртуальное окружение

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows cmd:

```cmd
.venv\Scripts\activate.bat
```

### 4. Установить зависимости

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Запуск тестов

### Запустить все тесты

```bash
pytest tests/ -v
```

### Запустить все тесты в headless-режиме

```bash
pytest tests/ -v --headless
```

### Запустить один тестовый файл

```bash
pytest tests/test_products_page.py -v --headless
```

### Запустить один конкретный тест

```bash
pytest tests/test_products_page.py::TestPageLoad::test_page_title -v --headless
```

### Сформировать HTML-отчёт

```bash
pytest tests/ -v --headless --html=report.html --self-contained-html
```

После выполнения будет создан файл `report.html`.

## Как работает запуск браузера

Проект использует Selenium 4 со встроенным `Selenium Manager`.

Это значит:

- не нужно вручную скачивать `chromedriver`
- не нужно хранить `chromedriver` в репозитории
- при первом запуске Selenium сам подбирает подходящий драйвер под установленный Chrome

Если на машине установлен Google Chrome, то в большинстве случаев дополнительная настройка не требуется.

## Настройки браузера

В `conftest.py` используются такие параметры Chrome:

- `--headless=new` при передаче флага `--headless`
- `--no-sandbox`
- `--disable-dev-shm-usage`
- размер окна `1920x1080`

Также для драйвера включен `implicitly_wait(10)`.

## Описание ключевых файлов

### `conftest.py`

Содержит:

- pytest-опцию `--headless`
- фикстуру `browser_options`
- фикстуру `driver`

### `ui/pages/base_page.py`

Содержит базовые методы:

- открытие страницы
- ожидание элементов
- клик по элементам
- ввод текста
- получение текста
- проверки видимости и наличия элементов

### `ui/pages/products_page.py`

Содержит:

- URL страницы продуктов
- локаторы навигации
- локаторы поиска
- локаторы карточек товаров
- локаторы блока категорий
- локаторы блока брендов
- методы поиска, открытия товара, работы с корзиной и сайдбаром

### `tests/test_products_page.py`

Содержит базовые UI тесты для страницы продуктов.

## Рекомендованный порядок первого запуска

Если вы поднимаете проект впервые, используйте такой порядок:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pytest tests/test_products_page.py::TestPageLoad::test_page_title -v --headless
pytest tests/ -v --headless
```

Сначала запускается один smoke-тест, затем весь набор.

## Типовые проблемы и решения

### 1. Браузер не запускается

Проверьте, что установлен Google Chrome.

Для macOS:

- откройте Applications
- убедитесь, что Google Chrome установлен

### 2. Selenium не может подобрать драйвер

Обычно это связано с:

- отсутствием интернета при первом запуске
- ограничениями прокси или корпоративной сети
- нестандартной установкой браузера

Что сделать:

- проверить интернет
- повторить запуск ещё раз
- обновить Selenium до актуальной версии при необходимости

### 3. Тесты падают нестабильно

Причины могут быть такими:

- сайт временно недоступен
- сайт отвечает медленно
- на странице изменились локаторы
- браузер открылся не в headless-режиме и выполнение мешает внешнее окружение

Что сделать:

- повторить запуск
- запустить в headless-режиме
- проверить актуальность локаторов в `products_page.py`

### 4. Ошибка SSL / предупреждение `NotOpenSSLWarning`

На macOS с системным Python может появляться предупреждение от `urllib3` о `LibreSSL`.

Это предупреждение не обязательно ломает тесты, но для более стабильной среды рекомендуется:

- использовать Python из `pyenv`, `asdf` или официального дистрибутива Python
- обновить локальную Python-среду при необходимости

### 5. Долгий первый запуск

Первый запуск может идти дольше обычного, потому что Selenium Manager подбирает и подготавливает драйвер.

## Что важно для GitHub

Тесты в этом репозитории обращаются к внешнему сайту `https://automationexercise.com`.
Это значит, что результат прогона зависит не только от кода проекта, но и от:

- доступности сайта
- скорости ответа сайта
- возможных изменений в DOM страницы
- сетевых ограничений на стороне запускающей машины

При публикации проекта в GitHub это важно указать, если вы будете подключать CI.

## Что не коммитить в репозиторий

При публикации проекта в GitHub рекомендуется не загружать в репозиторий:

- `.venv/`
- `.pytest_cache/`
- `report.html`
- `console_log.log`
- `.DS_Store`

Для этого обычно добавляют `.gitignore`.

## Команды для быстрого старта

```bash
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ>
cd UI-tests
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pytest tests/ -v --headless
```

## Дальнейшее развитие проекта

Проект можно расширить следующими направлениями:

- добавить фикстуры для разных браузеров
- добавить поддержку `pytest.ini`
- добавить скриншоты при падении тестов
- добавить логирование шагов
- добавить запуск в CI, например GitHub Actions
- покрыть тестами страницу деталей товара и корзину

## Автор

Проект подготовлен как учебный UI automation проект для Selenium и pytest.# autotests_automationexercise
# autotests_automationexercise
# autotests_automationexercise
# autotests_automationexercise
# autotests_automationexercise
