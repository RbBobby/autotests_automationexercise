# Automation Exercise — UI + API Tests

![Tests](https://github.com/RbBobby/autotests_automationexercise/actions/workflows/tests.yml/badge.svg)

Автотесты для [Automation Exercise](https://automationexercise.com): страница продуктов и REST API из [списка API](https://automationexercise.com/api_list).

> Замените `RbBobby/autotests_automationexercise` в badge на ваш `логин/репозиторий`, если fork другой.

| Набор | Технологии | Паттерн | Запуск |
|-------|------------|---------|--------|
| **API** (24 теста) | pytest, requests | API Client + Service Object, AAA | `pytest -m api` — браузер не нужен |
| **UI** (~20 тестов) | pytest, selenium | Page Object Model | `pytest -m ui --headless` — нужен Chrome |

Тесты ходят на **живой** сайт `automationexercise.com` — нужен интернет.

---

## Быстрый старт (первый запуск)

Выполните команды из корня репозитория `autotests_automationexercise`:

```bash
# 1. Виртуальное окружение
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1

# 2. Зависимости
pip install --upgrade pip
pip install -r requirements.txt

# 3. API-тесты (рекомендуется начать с них — без Chrome)
pytest -m api -v

# 4. UI smoke (один тест)
pytest tests/test_products_page.py::TestPageLoad::test_page_title -v --headless

# 5. Все UI-тесты
pytest -m ui -v --headless
```

Опционально — для **всех** API-тестов, включая логин (API 7–8):

```bash
cp .env.example .env
# отредактируйте .env: TEST_USER_EMAIL и TEST_USER_PASSWORD — учётная запись,
# зарегистрированная на https://automationexercise.com (Signup/Login)
pytest -m api -v
```

Без `.env` пройдут 22 API-теста, 2 теста логина будут `skipped`.

---

## Стек

- Python 3.9+ (проверено на 3.14)
- pytest, pytest-html
- **API:** requests, python-dotenv, faker
- **UI:** selenium + Selenium Manager (chromedriver вручную не ставится)

---

## Что проверяют тесты

### API (14 сценариев с api_list)

- список товаров и брендов (GET)
- неподдерживаемые методы (POST/PUT/DELETE → `responseCode` 405)
- поиск товара и ошибка без параметра `search_product`
- verify login: валидный / невалидный / без email / DELETE
- жизненный цикл пользователя: create → update → get by email → delete

### UI (страница `/products`)

- загрузка страницы, URL, title, заголовок `All Products`
- поиск, карточки товаров (имя, цена, изображение, `View Product`)
- модальное окно корзины после `Add to cart`
- сайдбар: категории, бренды (в т.ч. ожидаемый список)
- переход на страницу деталей товара

---

## Структура проекта

```text
autotests_automationexercise/
├── api/
│   ├── client/api_client.py       # HTTP transport
│   ├── config/settings.py         # .env → BASE_URL, credentials
│   ├── models/user_factory.py
│   └── services/                    # Products, Brands, Search, Auth, User
├── tests/
│   ├── api/                       # @pytest.mark.api
│   └── test_products_page.py      # @pytest.mark.ui
├── ui/pages/                      # base_page, products_page
├── conftest.py                    # UI: driver, --headless
├── tests/api/conftest.py          # API: api_client, services, registered_user
├── pytest.ini
├── .env.example
└── requirements.txt
```

---

## Архитектура

### API: Client → Service → Test (AAA)

```text
test  →  products_service.get_products()  →  ApiClient  →  automationexercise.com/api
         ↑ fixture (DI)
```

- **Arrange** — fixtures (`registered_user`, `valid_user_payload`)
- **Act** — один вызов метода Service
- **Assert** — `response.json["responseCode"]`, `message`, структура JSON

> Сайт часто отвечает **HTTP 200** при ошибке; смотрите `responseCode` в теле JSON.

### UI: Page Object Model

- `ui/pages/products_page.py` — локаторы и действия
- `tests/test_products_page.py` — сценарии
- `conftest.py` — `driver`, опция `--headless`

---

## Переменные окружения

Скопируйте шаблон и при необходимости измените значения:

```bash
cp .env.example .env
```

| Переменная | Назначение | По умолчанию |
|------------|------------|--------------|
| `API_BASE_URL` | Базовый URL API | `https://automationexercise.com/api` |
| `API_TIMEOUT` | Таймаут запросов (сек) | `30` |
| `TEST_USER_EMAIL` | Email для API 7–8 | — (тесты skip) |
| `TEST_USER_PASSWORD` | Пароль для API 7–8 | — (тесты skip) |

---

## Запуск тестов

### API

```bash
pytest -m api -v
pytest tests/api/test_products_list.py -v
```

### UI

```bash
pytest -m ui -v --headless
pytest tests/test_products_page.py::TestPageLoad::test_page_title -v --headless
```

### Всё сразу

```bash
pytest tests/ -v --headless
```

### HTML-отчёт

```bash
pytest tests/ -v --headless --html=report.html --self-contained-html
```

---

## Системные требования

| Набор | Требования |
|-------|------------|
| API | Python 3.9+, интернет |
| UI | + Google Chrome, интернет (первый раз — Selenium Manager скачает driver) |

Проверка:

```bash
python3 --version
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version   # macOS
```

---

## Установка с нуля (подробно)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/RbBobby/autotests_automationexercise.git
cd autotests_automationexercise
```

### 2–4. venv и зависимости

См. [Быстрый старт](#быстрый-старт-первый-запуск).

### 5. `.env` (опционально)

Нужен только если хотите запускать API 7–8 без `skipped`. Учётная запись должна быть создана на сайте через **Signup/Login**.

---

## Типовые проблемы

### API: 2 теста skipped

Не заданы `TEST_USER_EMAIL` / `TEST_USER_PASSWORD` в `.env`. Остальные API-тесты это не блокирует.

### UI: `SessionNotCreatedException` — ChromeDriver vs Chrome

Сообщение вида *«ChromeDriver only supports Chrome version 146», Current browser version is 148* значит, что в `PATH` лежит **устаревший** `chromedriver` (часто `/usr/local/bin/chromedriver`).

**Решение 1 (в проекте уже учтено):** `conftest.py` временно убирает такой driver из `PATH` и использует Selenium Manager.

**Решение 2 (на машине):** удалить или переименовать старый драйвер:

```bash
sudo mv /usr/local/bin/chromedriver /usr/local/bin/chromedriver.bak
```

Затем снова: `pytest -m ui -v --headless`

### UI: браузер не стартует

Установите Google Chrome. Первый запуск UI может быть долгим — Selenium Manager подбирает chromedriver.

### Нестабильные падения

Сайт недоступен, медленный ответ или изменился DOM/API. Повторите прогон; для UI используйте `--headless`.

### `NotOpenSSLWarning` (macOS)

Предупреждение urllib3 на системном Python. Для стабильности используйте Python из [python.org](https://www.python.org/) или pyenv.

---

## Что не коммитить

`.venv/`, `.pytest_cache/`, `.env`, `report.html`, `*.log`, `.DS_Store` — уже в `.gitignore`.

---

## CI (GitHub Actions)

В репозитории есть workflow [`.github/workflows/tests.yml`](.github/workflows/tests.yml) с двумя job:

| Job | Команда | Нужен Chrome |
|-----|---------|--------------|
| `api-tests` | `pytest -m api` | нет |
| `ui-tests` | `pytest -m ui --headless` | да (ставится автоматически) |

### Badge в README

В начале README уже есть статус workflow:

```markdown
![Tests](https://github.com/ВАШ_ЛОГИН/ВАШ_РЕПО/actions/workflows/tests.yml/badge.svg)
```

После push badge станет зелёным, если последний прогон CI успешен.

### Настройка один раз

1. Закоммитьте и запушьте код на GitHub (ветка `main` или `master`).
2. На GitHub: **Settings → Secrets and variables → Actions → New repository secret**:
   - `TEST_USER_EMAIL` — email с automationexercise.com
   - `TEST_USER_PASSWORD` — пароль
3. Без secrets API 7–8 в CI будут `skipped` (как локально без `.env`).
4. Проверка: вкладка **Actions** → workflow **Tests** → зелёные `api-tests` и `ui-tests`.

Запуск вручную: **Actions → Tests → Run workflow**.

### Артефакты CI (HTML-отчёты и скриншоты)

После каждого прогона (даже при падении тестов) в **Actions → выберите run → Artifacts**:

| Артефакт | Содержимое |
|----------|------------|
| `api-test-report` | `api-report.html` — отчёт pytest-html по API |
| `ui-test-artifacts` | `ui-report.html` + папка `screenshots/` |

Скачайте zip, откройте `ui-report.html` в браузере. При падении UI-теста в `screenshots/` будет PNG с экраном в момент ошибки.

Локально те же отчёты:

```bash
mkdir -p reports/screenshots
pytest -m api -v --html=reports/api-report.html --self-contained-html
pytest -m ui -v --headless --html=reports/ui-report.html --self-contained-html
```

Папка `reports/` в `.gitignore` — в репозиторий не коммитится.

---

## Дальнейшее развитие

- jsonschema для ответов API
- smoke E2E: сравнение `productsList` (API) и UI-страницы
- страницы product details / cart / login
