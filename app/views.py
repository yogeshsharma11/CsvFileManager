from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import CSVFile, CSVRow
from django.core.paginator import Paginator
import csv,json
# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password1':'','password2':""}
        form = UserCreationForm(initial=initial_data)
    return render(request, 'register.html',{'form':form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request, 'login.html',{'form':form}) 


def logout_view(request):
    logout(request)
    return redirect('login')



from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import CSVFile, CSVRow
from django.core.paginator import Paginator

@login_required
def dashboard_view(request):
    if request.method == "POST":
        csv_file = request.FILES.get('file')

        if not csv_file:
            messages.error(request, "No file was uploaded.")
            return redirect('dashboard')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "This is not a CSV file!.")
            return redirect('dashboard')

        try:
            file_instance = CSVFile.objects.create(
                user=request.user,
                file_name=csv_file.name
            )

            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines())
            for row in reader:
                CSVRow.objects.create(csv_file=file_instance, data=row)

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('dashboard')

        return redirect('dashboard')

    uploaded_files = CSVFile.objects.filter(user=request.user)

    paginator = Paginator(uploaded_files, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    file_data = {}
    for file in uploaded_files:
        csv_rows = CSVRow.objects.filter(csv_file=file)
        headers = csv_rows.first().data.keys() if csv_rows.exists() else []
        rows = [row.data.values() for row in csv_rows]
        file_data[file.id] = {
            'headers': headers,
            'rows': rows,
        }

    return render(request, 'dashboard.html', {
        'page_obj': page_obj,
        'file_data': file_data
    })

def delete_file(request, file_id):
    file = get_object_or_404(CSVFile, id=file_id, user=request.user)
    
    if request.method == "POST":
        file.delete()
        return redirect('dashboard') 

    return render(request, 'confirm_delete.html', {'file': file})

def edit_data(request, file_id):
    csv_file = get_object_or_404(CSVFile, id=file_id, user=request.user)
    rows = csv_file.rows.all()

    if request.method == "POST":
        
        for i in range(len(rows)):
            row_id = request.POST.get(f'row_id_{i}')
            if row_id:
                row = get_object_or_404(CSVRow, id=row_id)
                
                for key in row.data.keys():
                    value = request.POST.get(f'row_data_{i}_{key}', '')  
                    row.data[key] = value if value != '' else None  
                row.save()  

        
        new_row_data = {}
        for key in request.POST.keys():
            if key.startswith('new_row_data_'):
                header_name = key.split('new_row_data_')[1]
                new_row_data[header_name] = request.POST[key] if request.POST[key] != '' else None  # 

        # Create a new row if there is data
        if new_row_data:
            CSVRow.objects.create(csv_file=csv_file, data=new_row_data)

        return redirect('dashboard')

    return render(request, 'edit_data.html', {'csv_file': csv_file, 'rows': rows})



def view_file_data(request, file_id):
    csv_file = get_object_or_404(CSVFile, id=file_id, user=request.user)
    csv_rows = CSVRow.objects.filter(csv_file=csv_file)

    headers = csv_rows.first().data.keys() if csv_rows.exists() else []
    rows = [row.data.values() for row in csv_rows]

    return render(request, 'view_file_data.html', {
        'csv_file': csv_file,
        'headers': headers,
        'rows': rows
    })