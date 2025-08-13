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
