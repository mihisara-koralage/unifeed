from django.contrib import admin
from .models import Listing, ListingImage, Report

class ListingImageInline(admin.TabularInline):
    model  = ListingImage
    extra  = 0
    fields = ('image', 'order')

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display   = ('title', 'seller', 'price', 'category', 'condition', 'is_active', 'is_approved', 'created_at')
    list_filter    = ('category', 'condition', 'is_active', 'is_approved')
    search_fields  = ('title', 'seller__email', 'description')
    list_editable  = ('is_active', 'is_approved')
    readonly_fields = ('created_at',)
    inlines        = [ListingImageInline]

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('listing', 'reporter', 'reason', 'created_at')
    list_filter  = ('reason',)
    readonly_fields = ('created_at',)

    # Quick action to remove the reported listing from admin
    actions = ['remove_listing']

    def remove_listing(self, request, queryset):
        for report in queryset:
            report.listing.is_approved = False
            report.listing.save()
        self.message_user(request, f'{queryset.count()} listing(s) removed.')
    remove_listing.short_description = 'Remove reported listings'