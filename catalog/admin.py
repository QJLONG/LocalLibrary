from django.contrib import admin
from .models import Book, Author, BookInstance, Genre, Language

# Register your models here.
# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)

"""
可通过如下命令创建一个超级用户:
python3 manage.py createsuperuser
"""


class BooksInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # 在管理员Author界面显示author的指定属性
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # fields 字段为作者详细视图中显示的字段，字段默认情况下垂直显示，但如果你进一步将它们分组在元组中（如上述“日期”字段中所示），则会水平显示。
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    # 在author详细界面中显示对应的book
    inlines = [BooksInline]


class BooksInstanceInline(admin.TabularInline):
    # TabularInline (水平布局) StackedInline (垂直布局)
    model = BookInstance
    # 备用bookinstance数量设置为0
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # author是book的一个外键，通过book模型中定义的 __str__()来显示为字符串。
    # genre 为一个多对多的属性，也不可直接写在这里，通过book模型中东儿display_genre()方法将其以字符串列表的形式显示出来。
    list_display = ('title', 'author', 'display_genre')

    # 显示book与bookinstance的关联信息
    # 在这种情况下，我们所做的就是声明我们的tablular内联类，它只是从内联模型添加所有字段。你可以为布局指定各种附加信息，包括要显示的字段，其顺序，是否只读等。（有关详细信息，请参阅 TabularInline ).
    inlines = [BooksInstanceInline]
    

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    # 在列表中显示如下属性
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    # Create a filter of your lists
    list_filter = ('status', 'due_back')

    # fieldsets 可根据自定义标题（这里为None和Availability）将fields进行分类布局
    fieldsets = (
        (
            None, {
                'fields': ('book', 'imprint', 'id')
            }
        ),
        (
            'Availability', {
                'fields': ('status', 'due_back', 'borrower')
            }
        ),
    )
