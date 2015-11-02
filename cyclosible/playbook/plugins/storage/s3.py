from .base import StorageBase
from django.conf import settings
from boto.s3.key import Key
import boto


class S3Plugin(StorageBase):
    def __init__(self, task_id):
        super(S3Plugin, self).__init__(task_id)
        self.s3_connection = boto.connect_s3(aws_access_key_id=settings.S3_ACCESS_KEY,
                                             aws_secret_access_key=settings.S3_SECRET_KEY)
        self.s3_filename = 'cyclosible-{task_id}.log'.format(task_id=task_id)
        self.bucket = self.s3_connection.get_bucket(settings.S3_BUCKET)

    def write_log(self):
        k = Key(self.bucket)
        k.key = self.s3_filename
        self.log_url = k.generate_url(expires_in=600, query_auth=False)
        if k.set_contents_from_file(self.tmpfile):
            return True
        else:
            return False
