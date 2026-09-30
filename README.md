# GoFROST · Delivery Bot

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-3-26A5E4?logo=telegram&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=white)

**Telegram-бот для расчёта стоимости доставки охлаждённых и замороженных грузов и приёма заказов.**

Помогает собрать маршрут, вес, температурный режим, срочность и телефон клиента в одной пошаговой заявке. Заказ сохраняется в SQLite и отправляется администратору.

## Сценарий клиента

1. Выбрать города отправления и назначения из списка десяти городов Крыма.
2. Указать вес, охлаждение или заморозку, обычную или срочную доставку.
3. Получить расчёт и указать телефон.
4. Подтвердить заказ; администратор получает детали в Telegram.

## Расчёт стоимости

| Составляющая | Значение в текущем коде |
| --- | --- |
| Базовая стоимость | 500 ₽ |
| Расстояние | 30 ₽/км |
| Вес больше 10 кг | +100 ₽ |
| Заморозка | +500 ₽ |
| Срочная доставка | +1 000 ₽ |

Расстояние считается по координатам через `geopy.geodesic`, поэтому это предварительная оценка, а не длина автомобильного маршрута. Тарифы настраиваются в `calculate_price()`.

## Запуск

Нужен Python 3.10+.

```bash
git clone https://github.com/Pupsickk/gofrost-delivery-bot.git
cd gofrost-delivery-bot
python -m venv .venv
```

Активируйте окружение: Windows PowerShell — `.venv\Scripts\Activate.ps1`, Linux/macOS — `source .venv/bin/activate`.

```bash
python -m pip install -r requirements.txt
```

Скопируйте `.env.example` в `.env` и заполните настройки. Затем:

```bash
python tes.py
```

Укажите `BOT_TOKEN` и числовой `ADMIN_ID`. Перед запуском оператор должен отправить боту `/start`, чтобы бот мог присылать ему заказы.

## Устройство проекта

| Компонент | Назначение |
| --- | --- |
| [tes.py](tes.py) | Обработчики, FSM, клавиатуры и расчёт |
| `delivery_orders.db` | SQLite-база, создаётся при запуске |
| `.env` | Локальные настройки бота |
| [requirements.txt](requirements.txt) | Зависимости |

Незавершённые формы находятся в `MemoryStorage` и сбрасываются после перезапуска. Сохранённые заказы остаются в SQLite. Версия не содержит GPS-трекинга, эквайринга или интеграции с дорожными картами.


## Скриншоты

<img src="https://github.com/user-attachments/assets/a29357a3-8148-4c0c-9d9c-bfd74dd04a28" alt="Экран приложения 1" width="300" />

<img src="https://github.com/user-attachments/assets/e6cc3d63-8f92-4bb9-bdfb-d99a9fc35a5b" alt="Экран приложения 2" width="300" />

<img src="https://github.com/user-attachments/assets/4b7e6dc1-c74f-4648-972f-e996f2b4ae2a" alt="Экран приложения 3" width="300" />

<img src="https://github.com/user-attachments/assets/6b445ff3-ec9f-43ae-a239-e0b8b27af6f4" alt="Экран приложения 4" width="300" />

<img src="https://github.com/user-attachments/assets/8b5f3bcc-3171-4c8d-b0c6-eb05f1b98db7" alt="Экран приложения 5" width="300" />
