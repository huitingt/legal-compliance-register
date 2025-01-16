from django.contrib import admin
from .models import Category, Jurisdiction, Legislation, LegislationReview

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    ordering = ['code']

@admin.register(Jurisdiction)
class JurisdictionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

@admin.register(Legislation)
class LegislationAdmin(admin.ModelAdmin):
    list_display = ('title', 'tier', 'category', 'jurisdiction', 
                   'compliance_owner', 'next_review_date')
    list_filter = ('tier', 'category', 'jurisdiction')
    search_fields = ('title', 'description', 'compliance_owner', 
                    'business_owner')
    date_hierarchy = 'next_review_date'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(LegislationReview)
class LegislationReviewAdmin(admin.ModelAdmin):
    list_display = ('legislation', 'review_date', 'reviewed_by')
    list_filter = ('review_date', 'reviewed_by')
    search_fields = ('legislation__title', 'reviewed_by', 'comments')
    date_hierarchy = 'review_date'