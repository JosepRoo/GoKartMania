from crontab import CronTab

my_cron = CronTab(tabfile='/tmp/crontab.mH8jNu', user=False)
job = my_cron.new(command='./venv/Scripts/python app/cron_test.py')
job.minute.every(1)

my_cron.write()
