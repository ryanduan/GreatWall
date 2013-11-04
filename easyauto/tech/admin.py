from django.contrib import admin
from tech.models import TechKind, TechBlog, BlogComment


class TechKindAdmin(admin.ModelAdmin):
    list_display = (
            'kind_name',
            'user',
            'create_at',
        )

admin.site.register(TechKind, TechKindAdmin)


class TechBlogAdmin(admin.ModelAdmin):
    list_display = (
                'kind',
                'user',
                'title',
                'create_at',
                'check_time',
                'review_time',
                'good_heart',
        )

    def check_times(self, obj):
        if obj.check_time:
            cont = obj.check_time
        else:
            cont = "<a href=''>change</a>"
        return cont

    check_times.short_description = 'check_time'
    check_times.allow_tags = True


admin.site.register(TechBlog, TechBlogAdmin)
admin.site.register(BlogComment)
