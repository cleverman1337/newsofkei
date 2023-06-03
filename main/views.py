from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AccountEditForm

def index(request):
    return render(request, 'main/index.html')


def about(request):
    return render(request, 'main/about.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def inprogress(request):
    return render(request, 'main/inprogress.html')


@login_required
def view_account(request):
    return render(request, 'main/view_account.html', {'user': request.user})

@login_required
def edit_account(request):
    if request.method == 'POST':
        form = AccountEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('view_account')
    else:
        form = AccountEditForm(instance=request.user)
    return render(request, 'main/edit_account.html', {'form': form})