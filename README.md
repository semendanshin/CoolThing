# 🚀 CoolThing - Advanced Telegram Automation Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docs.docker.com/compose/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 🎯 **Pet Project** - A sophisticated microservices-based Telegram automation platform showcasing modern Python development practices, AI integration, and distributed architecture.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Technologies](#-technologies)
- [Getting Started](#-getting-started)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Monitoring](#-monitoring)
- [Development](#-development)
- [Contributing](#-contributing)
- [License](#-license)

## 🌟 Overview

CoolThing is a comprehensive Telegram automation platform built as a demonstration of modern software engineering practices. It combines multiple microservices to create a powerful system for managing Telegram interactions, processing messages with AI, and providing administrative capabilities through a web interface.

### 🎯 Project Goals

This pet project was designed to showcase:
- **Microservices Architecture** - Modular, scalable service design
- **AI Integration** - OpenAI GPT-powered message processing
- **Modern Python Stack** - FastAPI, SQLAlchemy, AsyncIO
- **DevOps Practices** - Docker containerization, monitoring, logging
- **Telegram API Mastery** - Both Bot API and MTProto implementation

## ✨ Features

### 🤖 Telegram Automation
- **Multi-bot Management** - Handle multiple Telegram bots simultaneously
- **Group Message Parsing** - Monitor and process messages from Telegram groups
- **Automated Responses** - AI-powered intelligent message responses
- **Campaign Management** - Organize and track messaging campaigns
- **Real-time Notifications** - Instant alerts for important events

### 🧠 AI Integration
- **OpenAI GPT Integration** - Natural language processing and generation
- **Custom Assistants** - Support for OpenAI Assistants API
- **Message Analysis** - Intelligent message categorization and processing
- **NLTK Text Processing** - Advanced text analysis and stemming

### 🏗️ Infrastructure
- **Microservices Architecture** - Independently deployable services
- **Message Queue** - RabbitMQ for reliable inter-service communication
- **Database Management** - PostgreSQL with Alembic migrations
- **Comprehensive Logging** - Fluentd-based centralized logging
- **Monitoring & Metrics** - Grafana dashboards for system health
- **Load Balancing** - Nginx reverse proxy configuration

### 🌐 Web Interface
- **Admin Dashboard** - Comprehensive management interface
- **Authentication System** - JWT-based secure access
- **Real-time Updates** - Live monitoring of system activity
- **Responsive Design** - Mobile-friendly interface
- **WebApp Integration** - Telegram Mini Apps support

## 🏛️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Parser      │    │     Manager     │    │       Bot       │
│   (Telethon)    │    │   (Telethon +   │    │ (python-tg-bot) │
│                 │    │     OpenAI)     │    │                 │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          │              ┌───────▼───────┐              │
          │              │   RabbitMQ    │              │
          │              │ Message Queue │              │
          │              └───────┬───────┘              │
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │     PostgreSQL DB      │
                    │    (with Alembic)      │
                    └────────────┬────────────┘
                                 │
                ┌────────────────▼────────────────┐
                │          Admin Panel           │
                │         (FastAPI)              │
                └────────────────┬────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │        Nginx           │
                    │    (Reverse Proxy)     │
                    └─────────────────────────┘
```

### 📦 Services Overview

1. **Parser Service** - Monitors Telegram groups and extracts target messages
2. **Manager Service** - Processes messages with AI and handles responses
3. **Bot Service** - Telegram bot interface for notifications and user interaction
4. **Admin Service** - Web-based administration panel
5. **Watchdog Service** - System monitoring and health checks

## 🛠️ Technologies

### Backend & Core
- **Python 3.11+** - Primary programming language
- **FastAPI** - Modern, fast web framework for APIs
- **SQLAlchemy 2.0** - SQL toolkit and ORM with async support
- **Alembic** - Database migration tool
- **AsyncPG** - Asynchronous PostgreSQL driver
- **Pydantic** - Data validation using Python type hints

### Telegram APIs
- **Telethon** - Full-featured Telegram client library (MTProto)
- **python-telegram-bot** - Telegram Bot API wrapper
- **Telegram WebApps** - Mini Apps integration

### AI & NLP
- **OpenAI API** - GPT models integration
- **OpenAI Assistants** - Advanced AI assistant capabilities
- **NLTK** - Natural Language Toolkit for text processing

### Message Queue & Communication
- **RabbitMQ** - Reliable message broker
- **aio-pika** - Asynchronous RabbitMQ client

### Database
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage

### DevOps & Infrastructure
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy and load balancer
- **Fluentd** - Log collection and processing
- **Grafana** - Monitoring and visualization

### Development Tools
- **Uvicorn** - ASGI server
- **Pytest** - Testing framework
- **Poetry/pip** - Dependency management

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Telegram API credentials
- OpenAI API key (optional)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/semendanshin/CoolThing.git
   cd CoolThing
   ```

2. **Create the Docker network**
   ```bash
   make mn
   ```

3. **Configure services**
   ```bash
   # Copy example configurations
   cp bot/example.settings.json bot/settings.json
   cp manager/example.settings.json manager/settings.json
   cp admin/example.settings.json admin/settings.json
   cp parser/example.settings.json parser/settings.json
   cp database/.env.example database/.env
   ```

4. **Build images**
   ```bash
   make bm  # Build manager
   make bp  # Build parser
   ```

5. **Start services**
   ```bash
   docker-compose up -d
   ```

6. **Access the admin panel**
   ```
   http://localhost:8081
   ```

### Manual Build Options

```bash
# Build specific services
make bm    # Build manager image
make bp    # Build parser image
make mn    # Create network

# Or build all at once
docker-compose build
```

## ⚙️ Configuration

### Bot Service (`bot/settings.json`)
```json
{
    "tg_bot_token": "YOUR_BOT_TOKEN",
    "tg_log_chats": [CHAT_ID_1, CHAT_ID_2],
    "host": "http://localhost:8081",
    "rabbit": {
        "host": "queue",
        "port": 5672,
        "user": "guest",
        "password": "guest",
        "vhost": ""
    }
}
```

### Manager Service (`manager/settings.json`)
```json
{
    "app": {
        "id": "unique-worker-id",
        "api_id": YOUR_API_ID,
        "api_hash": "YOUR_API_HASH",
        "session_string": "YOUR_SESSION_STRING",
        "proxy": "socks5://user:pass@host:port"
    },
    "db": {
        "host": "db",
        "port": 5432,
        "user": "postgres",
        "password": "postgres",
        "name": "postgres"
    },
    "openai": {
        "api_key": "YOUR_OPENAI_KEY",
        "model": "gpt-3.5-turbo",
        "service_prompt": "Your AI assistant prompt",
        "assistant": "asst_xxxxx"
    },
    "welcome_message": "Welcome message template",
    "campaign_id": "campaign-uuid"
}
```

### Environment Variables

Set up the database environment:
```bash
# database/.env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
```

## 📱 Usage

### Admin Dashboard

1. **Access the dashboard** at `http://localhost:8081`
2. **Login** with your credentials
3. **Manage bots** - Add, configure, and monitor Telegram bots
4. **Monitor campaigns** - Track message campaigns and performance
5. **View analytics** - Check system metrics and message statistics

### Telegram Bot Commands

- `/start` - Initialize bot and get admin panel access
- The bot provides notifications about detected target messages
- Access the web interface through the inline keyboard

### API Endpoints

The admin service exposes several REST API endpoints:

- `GET /api/bots` - List all configured bots
- `GET /api/campaigns` - List campaigns
- `GET /api/chats` - List monitored chats
- `POST /api/gpt-settings` - Configure AI settings

## 📊 API Documentation

Once the services are running, access the interactive API documentation:

- **FastAPI Swagger UI**: `http://localhost:8081/docs`
- **ReDoc**: `http://localhost:8081/redoc`

## 📈 Monitoring

### Grafana Dashboard

Access Grafana at the configured port to monitor:
- Service health and uptime
- Message processing rates
- Database performance
- Queue metrics
- Error rates and logs

### Fluentd Logging

All services send logs to Fluentd for centralized processing:
- Structured JSON logging
- Log aggregation and routing
- Integration with monitoring systems

## 🔧 Development

### Local Development Setup

1. **Install dependencies**
   ```bash
   cd manager && pip install -r requirements.txt
   cd ../bot && pip install -r requirements.txt
   cd ../admin && pip install -r requirements.txt
   cd ../parser && pip install -r requirements.txt
   ```

2. **Set up the database**
   ```bash
   # Run migrations
   cd database
   alembic upgrade head
   ```

3. **Run services individually**
   ```bash
   # Terminal 1 - Manager
   cd manager && python main.py

   # Terminal 2 - Bot
   cd bot && python main.py

   # Terminal 3 - Admin
   cd admin && uvicorn main:app --reload --port 8080

   # Terminal 4 - Parser
   cd parser && python main.py
   ```

### Testing

```bash
# Run tests for each service
pytest manager/tests/
pytest bot/tests/
pytest admin/tests/
pytest parser/tests/
```

### Code Style

The project follows PEP 8 standards with:
- Type hints throughout the codebase
- Async/await patterns for I/O operations
- Clean architecture principles
- SOLID design patterns

## 🤝 Contributing

This is a pet project, but contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow existing code style and patterns
- Add tests for new functionality
- Update documentation as needed
- Ensure Docker builds work correctly

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Telegram** for providing excellent APIs
- **OpenAI** for GPT integration capabilities
- **FastAPI** team for the amazing web framework
- **Python async** ecosystem contributors

## 📞 Contact

Created as a pet project by [@semendanshin](https://github.com/semendanshin)

---

⭐ **If you found this project interesting, please give it a star!** ⭐