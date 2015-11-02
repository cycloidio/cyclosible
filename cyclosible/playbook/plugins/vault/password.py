from .base import VaultBase
from django.conf import settings


class PasswordPlugin(VaultBase):
    def get_password(self):
        self.vault_password = settings.VAULT_PASSWORD
        return self.vault_password
