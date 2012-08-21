"""Admin of Zinnia"""
from django.contrib import admin

from zinnia.models import Entry
from zinnia.models import Category
from zinnia.admin.entry import EntryAdmin
from zinnia.admin.category import CategoryAdmin
from django.contrib.comments.models import Comment


admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)

class MyCommentsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Content',
           {'fields': ('user', 'user_name', 'user_email', 'user_url', 'comment')}
        ),
        ('Metadata',
           {'fields': ('submit_date', 'ip_address', 'is_public', 'is_removed')}
        ),
     )

    list_display = ('name', 'ip_address', 'submit_date', 'is_public', 'is_removed')
    list_filter = ('submit_date', 'site', 'is_public', 'is_removed')
    date_hierarchy = 'submit_date'
    ordering = ('-submit_date',)
    raw_id_fields = ('user',)
    search_fields = ('comment', 'user__username', 'user_name', 'user_email', 'user_url', 'ip_address')

admin.site.unregister(Comment)
admin.site.register(Comment, MyCommentsAdmin)
