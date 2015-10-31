from ..Cyclosible.celery import app
from .models import Playbook
from django.contrib.auth.models import User
from celery.utils.log import get_task_logger
from django.conf import settings
from .callbacks_ansiblev1 import PlaybookCallbacks, PlaybookRunnerCallbacks
from .models import PlaybookRunHistory
import ansible.playbook
import ansible.utils.template
from ansible import errors
from ansible import callbacks
from ansible import utils
from .s3 import S3PlaybookLog
import tempfile
from django.utils import timezone
logger = get_task_logger(__name__)


@app.task(bind=True, name="Run a playbook")
def run_playbook(self, playbook_name, user_name, s3_filename=None, only_tags=None, skip_tags=None, extra_vars=None):
    self.tmpfile = tempfile.NamedTemporaryFile(mode='a+')
    self.s3 = S3PlaybookLog(task_id=self.request.id)
    url = self.s3.write_log(tmpfile=self.tmpfile)
    history = PlaybookRunHistory.objects.create(
        playbook=Playbook.objects.get(name=playbook_name),
        date_launched=timezone.now(),
        status='RUNNING',
        task_id=self.request.id,
        launched_by=User.objects.get(username=user_name),
        log_url=url
    )

    # Here, we override the default ansible callbacks to pass our customs parameters
    stats = callbacks.AggregateStats()
    playbook_cb = PlaybookCallbacks(
        verbose=utils.VERBOSITY,
        task_id=self.request.id,
        tmpfile=self.tmpfile
    )
    runner_cb = PlaybookRunnerCallbacks(
        stats=stats,
        verbose=utils.VERBOSITY,
        task_id=self.request.id,
        tmpfile=self.tmpfile
    )

    pb = ansible.playbook.PlayBook(
        playbook=''.join([settings.PLAYBOOK_PATH, playbook_name, '.yml']),
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        stats=stats,
        extra_vars=extra_vars,
        only_tags=only_tags,
        skip_tags=skip_tags,
    )

    try:
        pb.run()
        hosts = sorted(pb.stats.processed.keys())
        logger.info(hosts)
        playbook_cb.on_stats(pb.stats)
    except errors.AnsibleError:
        history.date_finished = timezone.now()
        history.status = 'FAILED'
        history.save()
        self.tmpfile.seek(0)
        self.s3.write_log(tmpfile=self.tmpfile)
        print(u"ERROR: %s" % utils.unicode.to_unicode(errors.AnsibleError, nonstring='simplerepr'))
        self.tmpfile.close()
        return 1

    # Be kind, rewind
    self.tmpfile.seek(0)
    self.s3.write_log(tmpfile=self.tmpfile)
    self.tmpfile.close()
    history.date_finished = timezone.now()
    history.status = 'SUCCESS'
    history.save()
