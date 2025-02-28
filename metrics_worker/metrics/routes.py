import asyncio

from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CollectorRegistry, Gauge

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
scripts_by_campaign = Gauge(
    'scripts_by_campaign_total',
    'Количество скриптов по кампаниям',
    ['campaign_name'],
    registry=registry
)

# --- Группировка по ботам ---
scripts_by_bot = Gauge(
    'scripts_by_bot_total',
    'Количество скриптов по ботам',
    ['username'],
    registry=registry
)

# --- Группировка по чатам (агрегированные данные) ---
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

# Инициализируем MetricsService
metrics_service = MetricsService(
    scripts_repo=ScriptsRepository(),
    scripts_for_campaign_repo=ScriptsForCampaignRepository(),
    campaign_repo=CampaignRepository(session_maker=session_maker),
    workers_repo=SQLAlchemyWorkerRepository(session_maker=session_maker)
)


async def update_business_metrics():
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

    # Обновляем группировку по кампаниям
    for entry in grouped_campaign:
        campaign_name = entry['_id']  # Используем campaign_name напрямую
        count = entry.get('count', 0)
        scripts_by_campaign.labels(campaign_name=campaign_name).set(count)

    # Обновляем группировку по ботам (по username)
    for entry in grouped_bots:
        username = entry.get('username', 'unknown')  # Используем username напрямую
        count = entry.get('count', 0)
        scripts_by_bot.labels(username=username).set(count)

    # Обновляем метрики по чатам (используем campaign_name напрямую)
    for entry in grouped_chats:
        campaign_name = entry['_id']
        total_runs = entry.get('total_runs', 0)
        skipped_runs = entry.get('skipped_runs', 0)
        chat_runs_total.labels(campaign_name=campaign_name).set(total_runs)
        chat_runs_skipped.labels(campaign_name=campaign_name).set(skipped_runs)

    # Обновляем статистику по ботам (используем username напрямую)
    for entry in bots_stats:
        username = entry.get('username', 'unknown')
        count = entry.get('chats_count', 0)
        bot_chats_count.labels(username=username).set(count)

    # Обновляем статистику по чатам за последние 7 дней
    for entry in chats_stats:
        campaign_name = entry['_id']
        total_runs = entry.get('total_runs', 0)
        skipped_runs = entry.get('skipped_runs', 0)
        chats_total_last_7.labels(campaign_name=campaign_name).set(total_runs)
        chats_skipped_last_7.labels(campaign_name=campaign_name).set(skipped_runs)


@router.get('/metrics')
async def metrics():
    await update_business_metrics()
    return Response(generate_latest(registry), media_type='text/plain')
