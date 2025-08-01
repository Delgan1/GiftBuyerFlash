# Telegram Fash Gift Buyer 🎁⚡

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Kurigram](https://img.shields.io/badge/Kurigram-2.2.6-green)
![Kurigram](https://img.shields.io/badge/loguru-0.7.3-green)

Скрипт автоматизирует покупку лимитированных подарков в Telegram, используя несколько аккаунтов. Покупка начинается с самых редких подарков и продолжается до исчерпания баланса или доступности.
<p align="center">
  <img src="img/img.png" height="300"/>
  <img src="img/img_2.png" height="300"/>
</p>

## ✨ Особенности

- **Мультиаккаунтинг** - Поддержка мультиаккаунтной стратегии для управления Telegram Stars
- **Индивидуальная настройка** — Для каждого аккаунта можно указать собственного получателя подарков
- **Умные фильтры** - Гибкая система правил по ограничению покупок в зависимости от количества и цены подарков
- **Регулируемая скорость** — Настраиваемые паузы между отправкой подарков и периодами опроса  
- **Режим симуляции** — Возможность протестировать логику без списания средств  
- **Автопоиск подарков** — Скрипт отслеживает появление новых лимитированных подарков в реальном времени

## 🚀 Быстрый старт
**0. Склонируйте репозиторий**
```bash
git clone https://github.com/whale-crypto/GiftFlashBuyer
cd GiftFlashBuyer
```
Либо загрузите вручную и распакуйте архив

**1. Установите зависимости:**
```bash
pip install -r requirements.txt
```

**2. Создайте сессии для ваших аккаунтов:**
- В файле `session_create.py` впишите имя сессии для аккаунта (например, `name_session = "account1"`)
- Запустите `python session_create.py`
- Авторизуйтесь по номеру телефона
- Повторите для всех используемых аккаунтов

Таким образом создадутся файлы сессий `.session` локально, которые далее будут использоваться скриптом покупки

**3. Настройте скрипт:**
- Откройте `config.toml`
- Укажите имена сессий для проверки новых подарков, например
```toml
...
# Аккаунты для проверки выхода новых подарков
sessions_for_checking = ["account1", "account2", ...]
...
```
Вписывайте все подключенные аккаунты, так как если на один введут лимит запросов, то другие продолжат работу

- Имена сессий аккаунтов со звёздами → юзернеймы получателя подарков, например:
```toml
...
# Конфигурация отправки подарков
[[send_config]]
session_name_send_from = "account1" # Аккаунт со звёздами (Имя сессии)
username_send_to = "@someuser1"     # Получатель подарков

#[[send_config]]
#session_name_send_from = "account2"
#username_send_to = "@someuser2"
...
```
То есть: от какого аккаунта (название сессии) → какому (юзернейм) мы отправляем подарок. Копируйте строчки аналогично для каждой сессии.
- Задержки между запросами, которые выбираются на свой страх и риск. Рекомендуется оставить дефолтные
```toml
...
# Задержки
sleep_send_seconds = 0.2        # Задержка между запросами на отправку подарков
sleep_checking_seconds = 1      # Задержка между циклами проверки новых подарков
...
```

**4. Запустите скупщик:**
```bash
python main.py
```

## ⚙️ Настройка условий покупки

В файле `config.py` вы можете настроить логику фильтрации подарков:

```python
...
# Фильтр по подаркам, которые мы пропускаем
[[gift_filters]]
supply_range = ["5001", "10000"]
price_range = ["20001", "inf"]
...
```
Этот код надо читать так: если подарок от 5 до 10 тысяч штук стоит больше 20 тысяч звёзд, то мы пропускаем его и НЕ покупаем.

Вы можете настроить:
- Диапазоны саплая (общее количество)
- Диапазоны цен (Кол-во звезд для покупки)

## 🧪 Тестовый режим

Осуществляется урезанием текущего списка подарков, что позволяет сымитировать появление новых подарков при проверке и пропробовать их купить.

Для проверки работы без реальных покупок необходимо в `config.py` прописать:
```python
...
# Режимы
is_infinite_buying = true       # В данном режмие после покупки программа продолжит проверять новые подарки и закупать
...
```

Затем запустить скрипт
```bash
python main.py
```

Пример тестового вывода:

![img.png](img/img_debug.png)

Ошибка `StargiftUsageLimited` говорит о том, что сервер телеграма получил наш запрос и ответил нам, что подарок уже раскупили. Значит все параметры настроены, библиотеки установлены, интернет присутствует.

## 📝 Примечания

1. Убедитесь, что на ваших аккаунтах есть достаточное количество Telegram Stars.
2. Для работы скрипта необходимо стабильное интернет-соединение
3. Рекомендуется запускать скрипт на **Windows** для возможности активного контроля действий
4. Telegram может ввести лимиты на запросы - настройте разумные задержки
5. Внимательно настраивайте условия покупки - слишком строгие фильтры могут пропустить желанные подарки
6. Мониторьте логи работы скрипта и при необходимости корректируйте условия
7. Цены и суплай подарков могут меняться - регулярно обновляйте свои фильтры

## 📜 Лицензия

MIT License. Используйте на свой страх и риск. Автор не несет ответственности за возможные последствия.

---
Сделано с ❤️ для чистого Telegram-опыта