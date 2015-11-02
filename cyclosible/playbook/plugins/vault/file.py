from .base import VaultBase
from django.conf import settings


class FilePlugin(VaultBase):
    def get_password(self):
        with open(settings.VAULT_FILE) as vaultfile:
            self.vault_password = vaultfile.read()
            return self.vault_password
