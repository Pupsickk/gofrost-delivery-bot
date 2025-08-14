Telegram bot for temperature-controlled deliveries in Crimea. Calculates shipping costs based on distance, weight, temperature requirements (chilled/frozen), and urgency. Built with Python/Aiogram.
GoFROST - Telegram Bot for Temperature-Controlled Deliveries in Crimea
📌 Overview
GoFROST is a specialized Telegram bot designed to manage and calculate costs for temperature-sensitive deliveries across Crimea. This solution serves businesses and individuals who need reliable transportation of chilled and frozen goods between major Crimean cities.
✨ Key Features
🗺️ Smart Route Calculation
Covers 10 major Crimean cities including:

Simferopol

Sevastopol

Yalta

Kerch

Feodosia

Precise distance calculations using geopy's geodesic algorithm

❄️ Temperature-Sensitive Logistics
Supports two temperature regimes:

Chilled (+2°C to +6°C)

Frozen (-18°C and below)

Specialized pricing for different thermal requirements

💰 Dynamic Pricing Engine
Multi-factor cost calculation:

Base fare: 500₽

Distance rate: 30₽/km

Weight surcharge (for >10kg)

Temperature premium (frozen +500₽)

Urgency fee (express +1000₽)

📦 Complete Order Management
SQLite database for order storage

Detailed order confirmation system

Instant admin notifications for new orders

User order history tracking

🚀 Getting Started
Prerequisites
Python 3.10+

Telegram bot token from @BotFather

Basic understanding of Python environments
![photo_2025-07-27_11-10-55](https://github.com/user-attachments/assets/a29357a3-8148-4c0c-9d9c-bfd74dd04a28)
![photo_2025-07-27_11-10-41](https://github.com/user-attachments/assets/e6cc3d63-8f92-4bb9-bdfb-d99a9fc35a5b)
![photo_2025-07-27_11-10-36](https://github.com/user-attachments/assets/4b7e6dc1-c74f-4648-972f-e996f2b4ae2a)
<img width="748" height="627" alt="photo_2025-07-27_11-10-17" src="https://github.com/user-attachments/assets/6b445ff3-ec9f-43ae-a239-e0b8b27af6f4" />
![photo_2025-07-27_11-10-51](https://github.com/user-attachments/assets/8b5f3bcc-3171-4c8d-b0c6-eb05f1b98db7)


