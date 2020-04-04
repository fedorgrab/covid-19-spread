# import atexit
# from apscheduler.schedulers.background import BackgroundScheduler
# from backend.data_mining import update_data
# from backend.application.settings import BackendSettings
#
# scheduler = BackgroundScheduler()
# scheduler.add_job(
#     func=update_data,
#     trigger="interval",
#     hours=BackendSettings.UPDATE_DATA_EVERY_X_HOUR
# )
# scheduler.start()
# atexit.register(lambda: scheduler.shutdown())
