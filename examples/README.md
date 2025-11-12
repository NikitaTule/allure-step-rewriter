# Examples - allure-step-rewriter

Эта директория содержит примеры использования `allure-step-rewriter`.

## Запуск примеров

### Установка зависимостей

```bash
pip install allure-step-rewriter[allure]
pip install pytest
```

### Запуск примеров

```bash
# Запустить все примеры
pytest examples/ -v

# Запустить конкретный пример
pytest examples/basic_usage.py -v

# Сгенерировать Allure отчет
pytest examples/ --alluredir=allure-results
allure serve allure-results
```

## Описание примеров

### 1. `basic_usage.py` - Базовое использование

**Что демонстрирует:**
- Использование `@rewrite_step` как декоратор
- Динамическое переопределение title с `step_title`
- Использование `with rewrite_step()` как контекстный менеджер
- Декоратор без скобок (использует имя функции)
- Группировка нескольких действий в один шаг

**Ключевые примеры:**
```python
@rewrite_step("Get user data")
def get_user_data(user_id):
    return {"id": user_id}

# Override title dynamically
data = get_user_data(123, step_title="Fetch admin user")

# Use as context manager
with rewrite_step("Custom step"):
    get_user_data(456)
```

---

### 2. `multiple_overrides.py` - Множественное переопределение

**Что демонстрирует:**
- Переопределение **неограниченного количества** шагов в одном контексте
- Группировка сложных флоу в один логический шаг
- Практические примеры E2E тестов
- API тестирование с множественными запросами

**Ключевые примеры:**
```python
with rewrite_step("User Registration Flow"):
    open_browser()
    navigate("https://example.com/register")
    fill_field("username", "john")
    fill_field("email", "john@example.com")
    click_button("Register")
    close_browser()
# Результат: ТОЛЬКО ОДИН шаг "User Registration Flow"
```

**Важно:** Все вложенные вызовы декорированных функций "схлопываются" в один шаг.

---

### 3. `nested_steps.py` - Вложенные шаги

**Что демонстрирует:**
- Комбинирование `rewrite_step` и `allure.step`
- Создание иерархической структуры шагов
- Когда использовать `rewrite_step` vs `allure.step`
- Сложные многоуровневые структуры

**Ключевые примеры:**
```python
with rewrite_step("Test Scenario"):
    api_call("/setup")  # Переопределяется

    # Создать вложенный шаг
    with allure.step("Preparation"):
        api_call("/init")

    with allure.step("Execution"):
        api_call("/execute")

# Результат:
# ✓ Test Scenario
#   ✓ Preparation
#   ✓ Execution
```

**Правила:**
- `rewrite_step` контекст = схлопывает декорированные функции
- `allure.step` внутри `rewrite_step` = создает вложенный шаг
- `rewrite_step` внутри `rewrite_step` = **НЕ создает** вложенный шаг!

---

### 4. `pytest_integration.py` - Интеграция с pytest

**Что демонстрирует:**
- Использование с pytest fixtures
- Параметризованные тесты (`@pytest.mark.parametrize`)
- Pytest markers и Allure decorators
- Session-scoped fixtures
- Обработка исключений (`pytest.raises`)
- Test classes и методы
- Реальные сценарии использования

**Ключевые примеры:**
```python
@pytest.fixture
def browser():
    with rewrite_step("Initialize browser"):
        browser_instance = setup_browser()
    yield browser_instance
    with rewrite_step("Close browser"):
        teardown_browser()

@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user(user_id):
    with rewrite_step(f"Test GET /users/{user_id}"):
        response = get_user(user_id)
        assert validate(response)
```

---

## Общие принципы

### Когда использовать `rewrite_step`

✅ **Используйте `rewrite_step` когда:**
- Нужно сгруппировать несколько низкоуровневых операций в один логический шаг
- Хотите избежать глубокой вложенности в Allure отчете
- Нужно динамически изменять title шага
- Множество однотипных операций нужно представить как одно действие

❌ **НЕ используйте `rewrite_step` когда:**
- Нужна иерархическая структура шагов (используйте `allure.step`)
- Каждый шаг важен и должен быть виден отдельно
- Вложенные `with rewrite_step()` (не работает как переопределение!)

### Когда использовать `allure.step`

✅ **Используйте `allure.step` когда:**
- Нужно создать вложенные шаги внутри `rewrite_step` контекста
- Важна иерархическая структура (Given/When/Then)
- Каждый шаг должен быть виден отдельно в отчете

### Комбинирование

**Лучшая практика:**
```python
with rewrite_step("Test Case"):
    # Множественные низкоуровневые операции
    setup_operation_1()
    setup_operation_2()

    # Важный блок - вложенный шаг
    with allure.step("Critical Section"):
        critical_operation()

    # Снова множественные операции
    cleanup_operation_1()
    cleanup_operation_2()
```

---

## Структура Allure отчетов

### Пример 1: Только `rewrite_step`
```python
with rewrite_step("Parent"):
    func_a()
    func_b()
    func_c()
```
**Результат:**
```
✓ Parent
```

### Пример 2: `rewrite_step` + `allure.step`
```python
with rewrite_step("Parent"):
    func_a()
    with allure.step("Child"):
        func_b()
    func_c()
```
**Результат:**
```
✓ Parent
  ✓ Child
```

### Пример 3: Вложенные `rewrite_step` (НЕ РАБОТАЕТ!)
```python
with rewrite_step("Level 1"):
    with rewrite_step("Level 2"):
        func_a()
```
**Результат:**
```
✓ Level 1
(Level 2 НЕ появляется!)
```

---

## Советы по отладке

1. **Включите verbose вывод pytest:**
   ```bash
   pytest examples/basic_usage.py -v -s
   ```

2. **Проверьте Allure отчет:**
   ```bash
   pytest examples/ --alluredir=allure-results
   allure serve allure-results
   ```

3. **Используйте print для отладки:**
   ```python
   @rewrite_step("My step")
   def my_func():
       print("DEBUG: function called")
       return "result"
   ```

---

## Дополнительные ресурсы

- [Основной README](../README.md)
- [GitHub репозиторий](https://github.com/NikitaTule/allure-step-rewriter)
- [Документация Allure](https://docs.qameta.io/allure/)
- [Документация pytest](https://docs.pytest.org/)

---

## Контакты

Если у вас есть вопросы или предложения по примерам:
- GitHub Issues: https://github.com/NikitaTule/allure-step-rewriter/issues
- Email: tulenckov.nikita@gmail.com
