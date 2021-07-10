from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.db.models import Sum


now = timezone.now()
def home(request):
   return render(request, 'portfolio/home.html',
                 {'portfolio': home})

@login_required
def customer_list(request):
    customer = Customer.objects.filter(created_date__lte=timezone.now())
    return render(request, 'portfolio/customer_list.html',
                 {'customers': customer})

@login_required
def customer_edit(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   if request.method == "POST":
       # update
       form = CustomerForm(request.POST, instance=customer)
       if form.is_valid():
           customer = form.save(commit=False)
           customer.updated_date = timezone.now()
           customer.save()
           customer = Customer.objects.filter(created_date__lte=timezone.now())
           return render(request, 'portfolio/customer_list.html',
                         {'customers': customer})
   else:
        # edit
       form = CustomerForm(instance=customer)
   return render(request, 'portfolio/customer_edit.html', {'form': form})

@login_required
def customer_delete(request, pk):
   customer = get_object_or_404(Customer, pk=pk)
   customer.delete()
   return redirect('portfolio:customer_list')

@login_required
def stock_list(request):
   stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
   return render(request, 'portfolio/stock_list.html', {'stocks': stocks})

@login_required
def stock_new(request):
   if request.method == "POST":
       form = StockForm(request.POST)
       if form.is_valid():
           stock = form.save(commit=False)
           stock.created_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html',
                         {'stocks': stocks})
   else:
       form = StockForm()
       # print("Else")
   return render(request, 'portfolio/stock_new.html', {'form': form})

@login_required
def stock_edit(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   if request.method == "POST":
       form = StockForm(request.POST, instance=stock)
       if form.is_valid():
           stock = form.save()
           # stock.customer = stock.id
           stock.updated_date = timezone.now()
           stock.save()
           stocks = Stock.objects.filter(purchase_date__lte=timezone.now())
           return render(request, 'portfolio/stock_list.html', {'stocks': stocks})
   else:
       # print("else")
       form = StockForm(instance=stock)
   return render(request, 'portfolio/stock_edit.html', {'form': form})

@login_required
def stock_delete(request, pk):
   stock = get_object_or_404(Stock, pk=pk)
   stock.delete()
   return redirect('portfolio:stock_list')

@login_required
def investment_list(request):
   investments = Investment.objects.filter(acquired_date__lte=timezone.now())
   return render(request, 'portfolio/investment_list.html', {'investments': investments})

@login_required
def investment_new(request):
   if request.method == "POST":
       form = InvestmentForm(request.POST)
       if form.is_valid():
           investment = form.save(commit=False)
           investment.created_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html',
                         {'investments': investments})
   else:
       form = InvestmentForm()
       # print("Else")
   return render(request, 'portfolio/investment_new.html', {'form': form})

@login_required
def investment_edit(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   if request.method == "POST":
       form = InvestmentForm(request.POST, instance=investment)
       if form.is_valid():
           investment = form.save()
           # stock.customer = stock.id
           investment.updated_date = timezone.now()
           investment.save()
           investments = Investment.objects.filter(acquired_date__lte=timezone.now())
           return render(request, 'portfolio/investment_list.html', {'investments': investments})
   else:
       # print("else")
       form = InvestmentForm(instance=investment)
   return render(request, 'portfolio/investment_edit.html', {'form': form})

@login_required
def investment_delete(request, pk):
   investment = get_object_or_404(Investment, pk=pk)
   investment.delete()
   return redirect('portfolio:investment_list')

def signup_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('portfolio:home')
    else:
        form = UserCreationForm()
    return render(request, 'portfolio/signup.html', {'form': form})

@login_required
def fund_list(request):
   funds = Fund.objects.filter(ex_date__lte=timezone.now())
   return render(request, 'portfolio/fund_list.html', {'funds': funds})

@login_required
def fund_new(request):
   if request.method == "POST":
       form = FundForm(request.POST)
       if form.is_valid():
           fund = form.save(commit=False)
           fund.created_date = timezone.now()
           fund.save()
           funds = Fund.objects.filter(ex_date__lte=timezone.now())
           return render(request, 'portfolio/fund_list.html',
                         {'funds': funds})
   else:
       form = FundForm()
       # print("Else")
   return render(request, 'portfolio/fund_new.html', {'form': form})

@login_required
def fund_edit(request, pk):
   fund = get_object_or_404(Fund, pk=pk)
   if request.method == "POST":
       form = FundForm(request.POST, instance=fund)
       if form.is_valid():
           fund = form.save()
           # fund.customer = fund.id
           fund.updated_date = timezone.now()
           fund.save()
           funds = Fund.objects.filter(ex_date__lte=timezone.now())
           return render(request, 'portfolio/fund_list.html', {'funds': funds})
   else:
       # print("else")
       form = FundForm(instance=fund)
   return render(request, 'portfolio/fund_edit.html', {'form': form})

@login_required
def fund_delete(request, pk):
   fund = get_object_or_404(Fund, pk=pk)
   fund.delete()
   return redirect('portfolio:fund_list')



@login_required
def portfolio(request,pk):
   customer = get_object_or_404(Customer, pk=pk)
   customers = Customer.objects.filter(created_date__lte=timezone.now())
   investments =Investment.objects.filter(customer=pk)
   stocks = Stock.objects.filter(customer=pk)
   sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
   sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
   #overall_investment_results = sum_recent_value-sum_acquired_value
   # Initialize the value of the stocks
   sum_current_stocks_value = 0
   sum_of_initial_stock_value = 0

   # Loop through each stock and add the value to the total
   for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()

   return render(request, 'portfolio/portfolio.html', {'customers': customers,
                                                       'investments': investments,
                                                       'stocks': stocks,
                                                       'sum_acquired_value': sum_acquired_value,
                                                       'sum_recent_value': sum_recent_value,
                                                       'sum_current_stocks_value': sum_current_stocks_value,
                                                       'sum_of_initial_stock_value': sum_of_initial_stock_value,
                                                       })

# from django.http import HttpResponse
# from django.views.generic import View
# from portfolio.utils import render_to_pdf
# from django.template.loader import get_template
#from django.template.loader import render_to_string


# def portfolio_summary_pdf(request):
#     movie_ratingss = Customer.objects.all()
#     context = {'movie_ratingss': movie_ratingss,}
#     template = get_template('portfolio/customer_list.html')
#     html = template.render(context)
#     pdf = render_to_pdf('portfolio/customer_list.html', context)
#     return pdf

# def portfolio_summary_pdf(request,pk):
#     #portfolio_summary = Movie_Ratings.objects.all()
#     customer = get_object_or_404(Customer, pk=pk)
#     customerss = Customer.objects.filter(created_date__lte=timezone.now())
#     investmentss = Investment.objects.filter(customer=pk)
#     stockss = Stock.objects.filter(customer=pk)
#     sum_recent_values = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
#     sum_acquired_values = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
#     # overall_investment_results = sum_recent_value-sum_acquired_value
#     # Initialize the value of the stocks
#     sum_current_stocks_values = 0
#     sum_of_initial_stock_values = 0
#
#     # Loop through each stock and add the value to the total
#     for stock in stockss:
#         sum_current_stocks_values += stock.current_stock_value()
#         sum_of_initial_stock_values += stock.initial_stock_value()
#         overall_stocks_results = sum_current_stocks_values - float(sum_of_initial_stock_values)
#         overall_initial_amounts = float(sum_current_stocks_values) + float(sum_acquired_values['acquired_value__sum'])
#         overall_recent_amounts = float(sum_current_stocks_values) + float(sum_recent_values['recent_value__sum'])
#         overall_total = overall_recent_amounts - overall_initial_amounts
#
#     context = {'customerss': customerss,
#                'investmentss': investmentss,
#                'stockss': stockss,
#                'sum_acquired_values': sum_acquired_values,
#                'sum_recent_values': sum_recent_values,
#                'sum_current_stocks_values': sum_current_stocks_values,
#                'sum_of_initial_stock_values': sum_of_initial_stock_values,}
#     template = get_template('portfolio/portfolio_summary_pdf.html')
#     html = template.render(context)
#     pdf = render_to_pdf('portfolio/portfolio_summary_pdf.html', context)
#     return pdf
#     # return render(request, 'portfolio/portfolio_summary_pdf.html', {'customers': customers,
#     #                                                     'investments': investments,
#     #                                                     'stocks': stocks,
#     #                                                     'sum_acquired_value': sum_acquired_value,
#     #                                                     'sum_recent_value': sum_recent_value,
#     #                                                     'sum_current_stocks_value': sum_current_stocks_value,
#     #                                                     'sum_of_initial_stock_value': sum_of_initial_stock_value,
#     #                                                     })



# https://www.bedjango.com/blog/how-generate-pdf-django-weasyprint/
# https://stackoverflow.com/questions/59481394/django-oserror-no-library-called-cairo-was-found-on-windows
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string

#No changes required in utils.py
@login_required
def portfolio_summary_pdf(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    #customers = Customer.objects.filter(created_date__lte=timezone.now())
    investments = Investment.objects.filter(customer=pk)
    stocks = Stock.objects.filter(customer=pk)
    sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
    sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
    # Initialize the value of the stocks
    sum_current_stocks_value = 0
    sum_of_initial_stock_value = 0

    # Loop through each stock and add the value to the total
    for stock in stocks:
        sum_current_stocks_value += stock.current_stock_value()
        sum_of_initial_stock_value += stock.initial_stock_value()
    html_string = render_to_string('portfolio/portfolio_summary_pdf.html', {'customer': customer,
                                                       'investments': investments,
                                                       'stocks': stocks,
                                                       'sum_acquired_value': sum_acquired_value,
                                                       'sum_recent_value': sum_recent_value,
                                                        'sum_current_stocks_value': sum_current_stocks_value,
                                                        'sum_of_initial_stock_value': sum_of_initial_stock_value,})
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=portfolio_summary.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    result = html.write_pdf(response,)
    return response




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer

# List at the end of the views.py
# Lists all customers
class CustomerList(APIView):

    def get(self,request):
        customers_json = Customer.objects.all()
        serializer = CustomerSerializer(customers_json, many=True)
        return Response(serializer.data)






# def portfolio_summary(request,pk):
#     customer = get_object_or_404(Customer, pk=pk)
#     print(customer.id)
#     investments = Investment.objects.filter(customer=pk)
#     stocks = Stock.objects.filter(customer=pk)
#     sum_recent_value = Investment.objects.filter(customer=pk).aggregate(Sum('recent_value'))
#     sum_acquired_value = Investment.objects.filter(customer=pk).aggregate(Sum('acquired_value'))
#     # overall_investment_results = sum_recent_value-sum_acquired_value
#     # Initialize the value of the stocks
#     sum_current_stocks_value = 0
#     sum_of_initial_stock_value = 0
#
#     # Loop through each stock and add the value to the total
#     for stock in stocks:
#         sum_current_stocks_value += stock.current_stock_value()
#         sum_of_initial_stock_value += stock.initial_stock_value()
#     html_string = render_to_string('portfolio/portfolio_summary.html', {'customer': customer,
#                                                        'investments': investments,
#                                                        'stocks': stocks,
#                                                        'sum_acquired_value': sum_acquired_value,
#                                                        'sum_recent_value': sum_recent_value,
#                                                         'sum_current_stocks_value': sum_current_stocks_value,
#                                                         'sum_of_initial_stock_value': sum_of_initial_stock_value,})
#
#     response = HttpResponse(content_type='application/pdf;')
#     response['Content-Disposition'] = 'inline; filename=portfolio_{}.pdf'.format(customer.name)
#     response['Content-Transfer-Encoding'] = 'binary'
#     result = HTML(string=html_string).write_pdf(response,
#                                                 stylesheets=[CSS(
#                                                     settings.STATIC_ROOT + '/css/pdf.css')])
#     return response