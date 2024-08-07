from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


# 基于函数的视图可通过login_required修饰器来限制访问
# @login_required
def index(request):
    """
    View function for home page of site.
    """
    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact = 'a').count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1


    context = {
        'num_books': num_books, 
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    } 

    return render(request, 'index.html', context=context)


from django.views import generic


# 基于类的视图可通过在主视图类之前的超类列表中声明mixin，如下所示
class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'book_list'  # tamplate中的变量名
    queryset = Book.objects.all()
    template_name = 'catalog/book_list.html'  # 模板的位置
    paginate_by = 5 # 分页：5条一页
    
    """
    # 可以重写get_queryset()方法，让我们的查询语句更灵活。
    def get_queryset(self):
        return Book.objects.filter(title__icontains='war')[:5] 
    """

    """
    可以通过重写get_context_data()方法，让我们的context更灵活
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs) # 获取原函数返回的数据
        context['some_data'] = 'This is just some data'
        return context
    """

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'catalog/book_detail.html'

# 也可通过定义函数的方式创建book_detail视图
# def book_detail_view(request,pk):
#     try:
#         book_id=Book.objects.get(pk=pk)
#     except Book.DoesNotExist:
#         raise Http404("Book does not exist")

#     #book_id=get_object_or_404(Book, pk=pk)

#     return render(
#         request,
#         'catalog/book_detail.html',
#         context={'book':book_id,}
#     )

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

