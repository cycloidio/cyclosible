from rest_framework.routers import DefaultRouter


class ContainerRouter(DefaultRouter):
    def register_router(self, router):
        self.registry.extend(router.registry)

main_router = ContainerRouter()
