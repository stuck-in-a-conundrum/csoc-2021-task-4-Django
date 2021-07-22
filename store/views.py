from django.shortcuts import render
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, response
from django.views.decorators.csrf import csrf_exempt
from datetime import date

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    context = {
        'book': None, # set this to an instance of the required book
        'num_available': None, # set this to the number of copies of the book available, or 0 if the book isn't available
    }
    # START YOUR CODE HERE
    bookDetail=Book.objects.get(id=bid)
    isAvailable=[a for a in BookCopy.objects.filter(book=bookDetail).filter(status=True)]
    context['book']=bookDetail
    context['num_available']=len(isAvailable)
    
    
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    context = {
        'books': None, # set this to the list of required books upon filtering using the GET parameters
                       # (i.e. the book search feature will also be implemented in this view)
    }
    get_data = request.GET
    # START YOUR CODE HERE
    book_query = Book.objects.filter(title__icontains=get_data.get('title',''),
                                author__icontains=get_data.get('author',''),
                                genre__icontains=get_data.get('genre', ''))

    context['books'] = book_query
    
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    context = {
        'books': None,
    }

    '''
    The above key 'books' in the context dictionary should contain a list of instances of the 
    BookCopy model. Only those book copies should be included which have been loaned by the user.
    '''
    # START YOUR CODE HERE
    loanedBooks=BookCopy.objects.filter(borrower=request.user)
    context['books']=loanedBooks

    return render(request, template_name, context=context)

@csrf_exempt
@login_required


def loanBookView(request):
    response_data = {
        'message': None,
    }
    '''
    Check if an instance of the asked book is available.
    If yes, then set the message to 'success', otherwise 'failure'
    '''
    data=request.POST
    # START YOUR CODE HERE
    bid = data.get('bid')# get the book id from post data
    book_loan = BookCopy.objects.filter(book=bid,status=True)
    
    if len(book_loan)!=0:
        book_loan[0].borrower = request.user
        book_loan[0].borrow_date = date.today()
        book_loan[0].status = False
        book_loan[0].save()
        response_data['message'] = 'success'
    else:
        response_data['message']= 'failure'
    return JsonResponse(response_data)

'''
FILL IN THE BELOW VIEW BY YOURSELF.
This view will return the issued book.
You need to accept the book id as argument from a post request.
You additionally need to complete the returnBook function in the loaned_books.html file
to make this feature complete
''' 
@csrf_exempt
@login_required

def returnBookView(request):
    response_data = {
        'message': None,
    }
    data=request.POST
    bid = data.get('bid')
    book_return = BookCopy.objects.filter(id=bid)
    
    if len(book_return)!=0:
        book_return[0].borrower = None
        book_return[0].borrow_date = None
        book_return[0].status = True
        book_return[0].save()
        response_data['message'] = 'success'
    else:
        response_data['message']= 'failure'
    return JsonResponse(response_data)

@csrf_exempt
@login_required
def rateBookView(request):
    response_data={
        'message': 'failure',
    }
    data=request.POST
    book=data.get('bid')
    book_rate=Book.objects.get(bid=book)
    book_rate.rating=5.0
    book_rate.save()
    response_data['message']='success'
    return JsonResponse(response_data)