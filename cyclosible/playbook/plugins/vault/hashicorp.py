from .base import VaultBase
from django.conf import settings
import hvac


class HashicorpPlugin(VaultBase):
    def get_password(self):
        client = hvac.Client(
            url='{scheme}://{host}:{port}'.format(
                scheme=settings.VAULT_HASHICORP.get('scheme'),
                host=settings.VAULT_HASHICORP.get('host'),
                port=settings.VAULT_HASHICORP.get('port'),
            ),
            token=settings.VAULT_HASHICORP.get('token')
        )
        self.vault_password = client.read(
            settings.VAULT_HASHICORP.get('secret_path')
        ).get('data').get(settings.VAULT_HASHICORP.get('secret_field'))
        return self.vault_password
