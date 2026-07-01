from django.contrib import admin
from .models import Event, RSVP

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ('title', 'organizer', 'start_date', 'location', 'going_count')
    list_filter   = ('start_date',)
    search_fields = ('title', 'organizer__email', 'location')
    readonly_fields = ('created_at',)

    def going_count(self, obj):
        return obj.going_count
    going_count.short_description = 'Going'

@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'created_at')
    list_filter  = ('status',)