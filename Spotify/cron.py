from django_cron import CronJobBase, Schedule
from artists.models import Artist
from datetime import datetime
import os
from django.conf import settings
log_file_path = os.path.join(settings.BASE_DIR, 'cron.log')

class UpdateListenersCronJob(CronJobBase):
    # log_file_path = os.path.join(settings.BASE_DIR, 'cron.log')
    RUN_EVERY_MINS = 1 # run once a day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Spotify.update_listeners_cron_job'

    def do(self):
        artists = Artist.objects.all()

        with open(log_file_path, 'a') as log_file:
            log_file.write(f"Running update at {datetime.now()}\n")

        for artist in artists:
            artist.update_listeners_counter()

            with open(log_file_path, 'a') as log_file:
                log_file.write(f"Updated listeners for {artist.name} - {artist.listeners_counter}\n")