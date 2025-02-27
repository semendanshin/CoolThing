from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CollectorRegistry, Gauge

from scripts_watchdog.abstractions.repositories.CampaignRepositoryInterface import CampaignRepositoryInterface
from scripts_watchdog.abstractions.repositories.ScriptsForCampaignRepositoryInterface import \
    ScriptsForCampaignRepositoryInterface
from scripts_watchdog.abstractions.repositories.ScriptsRepositoryInterface import ScriptsRepositoryInterface
from scripts_watchdog.abstractions.repositories.WorkersRepositoryInterface import WorkersRepositoryInterface
# Импортируем MetricsService с вашими зависимостями
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
# Для каждой кампании обновляем значение с меткой campaign_id
scripts_by_campaign = Gauge('scripts_by_campaign_total', 'Количество скриптов по кампаниям', ['campaign_id'],
                            registry=registry)

# --- Группировка по ботам ---
scripts_by_bot = Gauge('scripts_by_bot_total', 'Количество скриптов по ботам', ['bot_id'], registry=registry)

# --- Группировка по чатам (на основе агрегированных данных) ---
chat_runs_total = Gauge('scripts_chat_total', 'Количество запусков скриптов по чатам (группировка по кампании)',
                        ['campaign_id'], registry=registry)
chat_runs_skipped = Gauge('scripts_chat_skipped_total',
                          'Количество пропущенных запусков скриптов по чатам (группировка по кампании)',
                          ['campaign_id'], registry=registry)

# --- Статистика по ботам ---
bot_chats_count = Gauge('bot_chats_count', 'Количество чатов, с которыми работает бот', ['bot_id', 'username'],
                        registry=registry)

# --- Статистика по чатам за последние 7 дней ---
chats_total_last_7 = Gauge('chats_total_last_7_days', 'Общее количество запусков чатов за последние 7 дней',
                           ['campaign_id'], registry=registry)
chats_skipped_last_7 = Gauge('chats_skipped_last_7_days', 'Количество пропущенных запусков чатов за последние 7 дней',
                             ['campaign_id'], registry=registry)

# Инициализируйте MetricsService, передав в него реальные реализации репозиториев
metrics_service = MetricsService(
    scripts_repo=ScriptsRepositoryInterface(),
    scripts_for_campaign_repo=ScriptsForCampaignRepositoryInterface(),
    campaign_repo=CampaignRepositoryInterface(),
    workers_repo=WorkersRepositoryInterface()
)


async def update_business_metrics():
    # Получаем данные из MetricsService (каждый метод возвращает список или агрегированные данные)
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

    # Обновляем метрику группировки по кампаниям
    for entry in grouped_campaign:
        campaign_id = entry['_id']
        count = entry.get('count', 0)
        scripts_by_campaign.labels(campaign_id=campaign_id).set(count)

    # Обновляем метрику группировки по ботам
    for entry in grouped_bots:
        bot_id = entry['_id']
        count = entry.get('count', 0)
        scripts_by_bot.labels(bot_id=bot_id).set(count)

    # Обновляем метрики по чатам (total и skipped)
    for entry in grouped_chats:
        campaign_id = entry['_id']
        total_runs = entry.get('total_runs', 0)
        skipped_runs = entry.get('skipped_runs', 0)
        chat_runs_total.labels(campaign_id=campaign_id).set(total_runs)
        chat_runs_skipped.labels(campaign_id=campaign_id).set(skipped_runs)

    # Обновляем статистику по ботам (количество чатов)
    for entry in bots_stats:
        bot_id = entry.get('worker_id')
        username = entry.get('username')
        count = entry.get('chats_count', 0)
        bot_chats_count.labels(bot_id=bot_id, username=username).set(count)

    # Обновляем статистику по чатам за последние 7 дней
    for entry in chats_stats:
        campaign_id = entry['_id']
        total_runs = entry.get('total_runs', 0)
        skipped_runs = entry.get('skipped_runs', 0)
        chats_total_last_7.labels(campaign_id=campaign_id).set(total_runs)
        chats_skipped_last_7.labels(campaign_id=campaign_id).set(skipped_runs)


@router.get('/metrics')
async def metrics():
    await update_business_metrics()
    return Response(generate_latest(registry), media_type='text/plain')
