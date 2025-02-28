import asyncio
from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CollectorRegistry, Gauge
import ast

from infrastructure.repositories.sqlalchemy import session_maker
from repositories.beanie.ScriptsForCampaignRepository import ScriptsForCampaignRepository
from repositories.beanie.ScriptsRepository import ScriptsRepository
from repositories.sqlalchemy.CampaignRepository import CampaignRepository
from repositories.sqlalchemy.WorkersRepository import SQLAlchemyWorkerRepository
from .service import MetricsService

router = APIRouter()
registry = CollectorRegistry()

# --- Простые счетчики скриптов ---
scripts_today = Gauge('scripts_today_total', 'Количество скриптов, активированных сегодня', registry=registry)
scripts_week = Gauge('scripts_week_total', 'Количество скриптов, активированных за неделю', registry=registry)
scripts_month = Gauge('scripts_month_total', 'Количество скриптов, активированных за месяц', registry=registry)
scripts_all = Gauge('scripts_all_total', 'Общее количество скриптов', registry=registry)
scripts_active = Gauge('scripts_active_total', 'Количество активных скриптов', registry=registry)

# --- Группировка по кампаниям ---
# Используем только один лейбл: campaign_name (человеко-читаемое имя кампании)
scripts_by_campaign = Gauge(
    'scripts_by_campaign_total',
    'Количество скриптов по кампаниям',
    ['campaign_name'],
    registry=registry
)

# --- Группировка по ботам ---
# Используем username вместо bot_id
scripts_by_bot = Gauge(
    'scripts_by_bot_total',
    'Количество скриптов по ботам',
    ['username'],
    registry=registry
)

# --- Группировка по чатам (агрегированные данные) ---
# Преобразуем campaign_id в campaign_name
chat_runs_total = Gauge(
    'scripts_chat_total',
    'Количество запусков скриптов по чатам (группировка по кампании)',
    ['campaign_name'],
    registry=registry
)
chat_runs_skipped = Gauge(
    'scripts_chat_skipped_total',
    'Количество пропущенных запусков скриптов по чатам (группировка по кампании)',
    ['campaign_name'],
    registry=registry
)

# --- Статистика по ботам ---
# Используем только username для понятной подписи
bot_chats_count = Gauge(
    'bot_chats_count',
    'Количество чатов, с которыми работает бот',
    ['username'],
    registry=registry
)

# --- Статистика по чатам за последние 7 дней ---
chats_total_last_7 = Gauge(
    'chats_total_last_7_days',
    'Общее количество запусков чатов за последние 7 дней',
    ['campaign_name'],
    registry=registry
)
chats_skipped_last_7 = Gauge(
    'chats_skipped_last_7_days',
    'Количество пропущенных запусков чатов за последние 7 дней',
    ['campaign_name'],
    registry=registry
)

# Инициализируем MetricsService с реальными репозиториями
metrics_service = MetricsService(
    scripts_repo=ScriptsRepository(),
    scripts_for_campaign_repo=ScriptsForCampaignRepository(),
    campaign_repo=CampaignRepository(session_maker=session_maker),
    workers_repo=SQLAlchemyWorkerRepository(session_maker=session_maker)
)

# Функция для получения имени кампании по campaign_id с декодированием, если необходимо

async def get_campaign_name(campaign_id: str) -> str:
    try:
        campaign = await metrics_service.campaign_repo.get(campaign_id)
        if campaign and hasattr(campaign, 'name'):
            name = campaign.name
            # Если значение уже объект bytes – декодируем
            if isinstance(name, bytes):
                return name.decode('utf-8')
            # Если значение строка и выглядит как литерал байтов (например, "b'Campaign Name'")
            if isinstance(name, str) and name.startswith("b'") and name.endswith("'"):
                try:
                    # Преобразуем строку в объект bytes с помощью ast.literal_eval
                    evaluated = ast.literal_eval(name)
                    if isinstance(evaluated, bytes):
                        return evaluated.decode('utf-8')
                except Exception:
                    # Если не удалось оценить – просто удаляем префикс и суффикс
                    return name[2:-1]
            return name
        else:
            return campaign_id
    except Exception:
        return campaign_id


# Функция для получения username бота с декодированием, если необходимо
def get_bot_username(raw_username) -> str:
    if raw_username:
        return raw_username.decode('utf-8') if isinstance(raw_username, bytes) else raw_username
    return "unknown"

async def update_business_metrics():
    # Получаем данные из MetricsService
    today = await metrics_service.get_today_scripts()
    week = await metrics_service.get_week_scripts()
    month = await metrics_service.get_month_scripts()
    all_scripts = await metrics_service.get_all_scripts()
    active_scripts = await metrics_service.get_active_scripts()
    grouped_campaign = await metrics_service.get_grouped_scripts_by_campaign()
    grouped_bots = await metrics_service.get_grouped_scripts_by_bots()
    grouped_chats = await metrics_service.get_grouped_scripts_by_chats()
    bots_stats = await metrics_service.get_bots_statistics()
    chats_stats = await metrics_service.get_chats_statistics(n=7)

    # Обновляем простые счетчики
    scripts_today.set(len(today))
    scripts_week.set(len(week))
    scripts_month.set(len(month))
    scripts_all.set(len(all_scripts))
    scripts_active.set(len(active_scripts))

    # Обновляем метрику группировки по кампаниям: конвертация campaign_id -> campaign_name
    campaign_tasks = []
    for entry in grouped_campaign:
        campaign_id = entry['_id']
        count = entry.get('count', 0)
        campaign_tasks.append((campaign_id, count))
    campaign_names = await asyncio.gather(*[get_campaign_name(cid) for cid, _ in campaign_tasks])
    for (campaign_id, count), campaign_name in zip(campaign_tasks, campaign_names):
        scripts_by_campaign.labels(campaign_name=campaign_name).set(count)

    # Обновляем метрику группировки по ботам: используем username
    for entry in grouped_bots:
        raw_username = entry.get('username')
        count = entry.get('count', 0)
        username = get_bot_username(raw_username)
        if username:
            scripts_by_bot.labels(username=username).set(count)

    # Обновляем метрики по чатам: конвертация campaign_id -> campaign_name
    chat_tasks = []
    for entry in grouped_chats:
        campaign_id = entry['_id']
        total_runs = entry.get('total_runs', 0)
        skipped_runs = entry.get('skipped_runs', 0)
        chat_tasks.append((campaign_id, total_runs, skipped_runs))
    chat_names = await asyncio.gather(*[get_campaign_name(cid) for cid, _, _ in chat_tasks])
    for (campaign_id, total_runs, skipped_runs), campaign_name in zip(chat_tasks, chat_names):
        chat_runs_total.labels(campaign_name=campaign_name).set(total_runs)
        chat_runs_skipped.labels(campaign_name=campaign_name).set(skipped_runs)

    # Обновляем статистику по ботам (количество чатов): используем username
    for entry in bots_stats:
        raw_username = entry.get('username')
        count = entry.get('chats_count', 0)
        username = get_bot_username(raw_username)
        if username:
            bot_chats_count.labels(username=username).set(count)

    # Обновляем статистику по чатам за последние 7 дней: конвертация campaign_id -> campaign_name
    chats_tasks = []
    for entry in chats_stats:
        campaign_id = entry['_id']
        total_runs = entry.get('total_runs', 0)
        skipped_runs = entry.get('skipped_runs', 0)
        chats_tasks.append((campaign_id, total_runs, skipped_runs))
    chats_names = await asyncio.gather(*[get_campaign_name(cid) for cid, _, _ in chats_tasks])
    for (campaign_id, total_runs, skipped_runs), campaign_name in zip(chats_tasks, chats_names):
        chats_total_last_7.labels(campaign_name=campaign_name).set(total_runs)
        chats_skipped_last_7.labels(campaign_name=campaign_name).set(skipped_runs)

@router.get('/metrics')
async def metrics():
    await update_business_metrics()
    return Response(generate_latest(registry), media_type='text/plain')
