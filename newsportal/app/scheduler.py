# from apscheduler.schedulers.background import BackgroundScheduler
# from django_apscheduler.jobstores import DjangoJobStore
# from .tasks import send_weekly_newsletter
# from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
#
# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "default")
#
#
# def weekly_newsletter_job():
#     send_weekly_newsletter()
#
#
# # Schedule the job
# scheduler.add_job(weekly_newsletter_job, 'interval', weeks=1, id='weekly_newsletter_job', replace_existing=True)
#
#
# # Add a listener to handle job events (e.g., job completion, job errors)
# def job_listener(event):
#     if event.exception:
#         print(f"Job {event.job_id} failed")
#     else:
#         print(f"Job {event.job_id} completed successfully")
#
#
# scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
#
# scheduler.start()
