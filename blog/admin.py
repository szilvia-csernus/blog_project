from django.contrib import admin

# Register your models here.

from .models import Post, Author, Tag, Comment

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "tags", "date",) # Tuple!
    list_display = ("title", "date", "author",) # Tuple!
    prepopulated_fields = {"slug": ("title",)} 
    
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post", "text",) # Tuple!
    

admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)