from django.contrib import admin
from tech.models import TechKind, TechBlog, BlogComment

admin.site.register(TechKind)
admin.site.register(TechBlog)
admin.site.register(BlogComment)
