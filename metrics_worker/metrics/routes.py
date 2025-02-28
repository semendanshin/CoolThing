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
# Теперь используем лейбл campaign_name для отображения имени кампании
scripts_by_campaign = Gauge(
    'scripts_by_campaign_total',
    'Количество скриптов по кампаниям',
    ['campaign_name'],
    registry=registry
)

# --- Группировка по ботам ---
# Для ботов выводим username, а не raw id
scripts_by_bot = Gauge(
    'scripts_by_bot_total',
    'Количество скриптов по ботам',
    ['username'],
    registry=registry
)

# --- Группировка по чатам (на основе агрегированных данных) ---
# Конвертируем campaign_id в campaign_name
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
# Выводим только username для понятной легенды
bot_chats_count = Gauge(
    'bot_chats_count',
    'Количество чатов, с которыми работает бот',
    ['username'],
    registry=registry
)

# --- Статистика по чатам за последние 7 дней ---
# Аналогично преобразуем campaign_id в campaign_name
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

# Функция для получения имени кампании по campaign_id.
# Если не найдено, возвращает исходное значение.
async def get_campaign_name(campaign_id: str) -> str:
    try:
        campaign = await metrics_service.campaign_repo.get(campaign_id)
        return campaign.name if campaign and hasattr(campaign, 'name') else campaign_id
    except Exception:
        return campaign_id

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

    # --- Обновляем метрику по кампаниям ---
    # Для каждого campaign_id получаем имя кампании
    campaign_tasks = []
    for entry in grouped_campaign:
        campaign_id = entry['_id']
        count = entry.get('count', 0)
        campaign_tasks.append((campaign_id, count))
    campaign_names = await asyncio.gather(*[get_campaign_name(cid) for cid, _ in campaign_tasks])
    for (campaign_id, count), campaign_name in zip(campaign_tasks, campaign_names):
        scripts_by_campaign.labels(campaign_name=campaign_name).set(count)

    # --- Обновляем метрику по ботам (группировка по username) ---
    for entry in grouped_bots:
        username = entry.get('username')
        count = entry.get('count', 0)
        if username:
            scripts_by_bot.labels(username=username).set(count)

    # --- Обновляем метрики по чатам ---
    # Конвертируем campaign_id в campaign_name для каждой записи
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

    # --- Обновляем статистику по ботам (количество чатов) ---
    for entry in bots_stats:
        username = entry.get('username')
        count = entry.get('chats_count', 0)
        if username:
            bot_chats_count.labels(username=username).set(count)

    # --- Обновляем статистику по чатам за последние 7 дней ---
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
