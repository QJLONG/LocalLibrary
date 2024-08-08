"""
程序运行前，需要运行数据库迁移命令。
当我们更改模型定义时，Django 会跟踪更改并创建数据库迁移脚本 (in /locallibrary/catalog/migrations/) 来自动迁移数据库中的底层数据结构来：
python manage.py makemigrations
python manage.py migrate
"""

import uuid
from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Genre(models.Model):
    """
    图书的类型：如Science Fiction, Non Fiction。
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)")

    def __str__(self):
        """
        返回模型名称
        """
        return self.name
    
    
class Book(models.Model):
    """
    用于记录一本书籍信息
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField("ISNB", max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.

    """
    以两个模型为例，老师和学生，其中，学生通过外键关联老师
    on_delete 属性有6个可选值：
        CASCADE：删除级联，当父表（老师）的记录删除时，子表（学生）中与其相关的记录也会被删除。
        PROTECT：保护模式，当父表（老师）的记录删除时，会报ProtectedError异常。
        Set_NULL：当父表（老师）的记录删除时，会将子表中记录的关联字段设置为NULL。
        Set_DEFAULT：当父表（老师）的记录删除时，会将子表中记录的关联字段设置为一个给定的默认值。
        DO_NOTHING：当父表（老师）的记录删除时，什么也不做。
        SET()：设置为一个传递给SET（）的值，或一个回调函数的返回值。该参数用的相对较少。
    """

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """
        返回访问book实例的url
        """
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        return ','.join([ genre.name for genre in self.genre.all()[:3] ])
    
    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    # uuid.uuid4基于随机数生成128位（长度32的十六进制字符）的唯一ID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book ailability')

    def is_overtime(self):
        """
        备注：在进行比较之前，我们首先验证due_back是否为空。空的due_back字段，会导致 Django 抛出错误，而不是显示页面：空值不具有可比性。这不是我们希望用户体验到的东西！
        """
        if self.due_back and date.today() > self.due_back:
            return True
        return False


    class Meta:
        ordering = ["due_back"]
        # 允许用户标记已经归还的书
        permissions = (("can_mark_returned", "Set book as returned"),)



    def __str__(self):
        return '%s (%s)' % (self.id, self.book.title)
        

class Author(models.Model):
    """
    Model representing an author
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['last_name', 'first_name']

    

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)
    
class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def get_absolute_url(self):
        """Returns the url to access a particular language instance."""
        return reverse('language-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    # 检查是否已经存在该language
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ]



