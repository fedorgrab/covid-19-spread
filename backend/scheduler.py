import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from backend.application.settings import BackendSettings

scheduler = BackgroundScheduler()
scheduler.add_job(
    func="backend.data_mining:update_data",
    trigger="interval",
    hours=BackendSettings.UPDATE_DATA_EVERY_X_HOUR,
)
scheduler.add_job(
    func="backend.data_mining:update_total_data",
    trigger="interval",
    hours=BackendSettings.UPDATE_DATA_EVERY_X_HOUR,
)

scheduler.start()
atexit.register(lambda: scheduler.shutdown())
