from cyclosible.Cyclosible.routers import main_router
from .views import (PlaybookViewSet, PlaybookRunHistoryViewSet)

main_router.register(r'playbooks', PlaybookViewSet)
main_router.register(r'playbookrunhistorys', PlaybookRunHistoryViewSet)
