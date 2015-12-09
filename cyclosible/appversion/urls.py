from cyclosible.Cyclosible.routers import main_router
from .views import (AppVersionViewSet)

main_router.register(r'app-version', AppVersionViewSet)
