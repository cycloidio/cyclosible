from django.contrib import admin
from .models import Playbook, PlaybookRunHistory
from guardian.admin import GuardedModelAdmin


@admin.register(Playbook)
class PlaybookAdmin(GuardedModelAdmin):
    queryset = Playbook.objects.all()
    list_display = ('name', 'group', 'only_tags', 'skip_tags')


@admin.register(PlaybookRunHistory)
class PlaybookRunHistoryAdmin(GuardedModelAdmin):
    queryset = PlaybookRunHistory.objects.all()
    list_display = ('playbook', 'date_launched', 'date_finished', 'status', 'task_id', 'launched_by')
