from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone

from .forms import LoginWithPinForm, MaintenanceSlipForm
from .models import Block, Resident, MaintenanceSlip, Profile


from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Block, Resident
from django.contrib.auth.decorators import login_required




def home(request):
    # Handle block creation
    if request.method == 'POST':
        block_name = request.POST.get('name')
        if block_name and not Block.objects.filter(name=block_name).exists():
            Block.objects.create(name=block_name)
        return redirect('home')  # Refresh page after adding

    # Fetch all blocks
    blocks = Block.objects.all()

    # Count residents per block
    counts = Resident.objects.values('block_id').annotate(total=Count('id'))
    counts_dict = {c['block_id']: c['total'] for c in counts}

    # Attach resident count to each block
    for block in blocks:
        block.resident_count = counts_dict.get(block.id, 0)

    context = {
        'blocks': blocks
    }
    return render(request, 'society/home.html', context)


def login_with_pin(request):
    if request.method == 'POST':
        form = LoginWithPinForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            pin = form.cleaned_data['pin']
            user = authenticate(request, username=u, password=p)
            if user:
                try:
                    profile = user.profile
                except Profile.DoesNotExist:
                    messages.error(request, 'PIN not set. Contact admin.')
                    return redirect('login')
                if profile.pin == pin:
                    login(request, user)
                    messages.success(request, 'Welcome Chairman')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid PIN')
            else:
                messages.error(request, 'Invalid username/password')
    else:
        form = LoginWithPinForm()
    return render(request, 'society/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def block_detail(request, block_id):
    block = get_object_or_404(Block, id=block_id)
    
    # Only residents of this block, sorted by flat number
    residents = block.residents.all().order_by('flat_no')
    
    context = {
        'block1': block,
        'residents': residents
    }
    return render(request, 'society/block_detail.html', context)


from django.db.models import Q
from calendar import monthrange

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from .models import Block, Resident, MaintenanceSlip
from .forms import MaintenanceSlipForm



@login_required
def slip_detail(request, pk):
    slip = get_object_or_404(MaintenanceSlip, pk=pk)
    return render(request, 'society/slip_detail.html', {'slip': slip})





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Block, Resident
from .forms import ResidentForm

def block_detail(request, block_id):
    block1 = get_object_or_404(Block, id=block_id)
    residents = block1.residents.all()

    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            flat_no = form.cleaned_data['flat_no']
            # Check if the flat number already exists in this block
            if residents.filter(flat_no=flat_no).exists():
                messages.error(request, f"Flat No {flat_no} already exists in this block!")
            else:
                resident = form.save(commit=False)
                resident.block = block1
                resident.save()
                messages.success(request, f"Resident {resident.name} added successfully!")
            return redirect('block_detail', block_id=block_id)
    else:
        form = ResidentForm()

    context = {
        'block1': block1,
        'residents': residents,
        'form': form
    }
    return render(request, 'society/block_detail.html', context)
# views.py
@login_required
def create_slip(request, block_id=None):
    if not block_id:
        messages.error(request, "Block ID is required to create a slip.")
        print("No Block ID provided in create_slip")
        return redirect("home")

    block = get_object_or_404(Block, id=block_id)
    
    residents = block.residents.all().order_by('flat_no')

    date_str = request.POST.get('date') or request.GET.get('date')
    selected_date = None
    if date_str:
        try:
            selected_date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format.")

    available_residents = residents.none()
    if selected_date:
        year, month = selected_date.year, selected_date.month
        existing_slips = MaintenanceSlip.objects.filter(
            block=block,
            date__year=year,
            date__month=month
        ).values_list('resident_id', flat=True)
        available_residents = residents.exclude(id__in=existing_slips)

    if request.method == 'POST':
        form = MaintenanceSlipForm(request.POST)
        form.fields['resident'].queryset = available_residents
        if form.is_valid():
            slip = form.save(commit=False)
            slip.created_by = request.user
            base = slip.date.strftime("%Y%m%d")
            existing_today = MaintenanceSlip.objects.filter(date=slip.date).count()
            slip.slip_no = f"{base}-{existing_today+1}"
            slip.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": True, "message": "Slip created successfully."})

            messages.success(request, "Slip saved successfully.")
            return redirect("slip_detail", slip.pk)
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({"success": False, "errors": form.errors})

            messages.error(request, "Please correct the errors below.")
    else:
        form = MaintenanceSlipForm(initial={
            "block": block.id,
            "date": selected_date,
            "maintenance_charge_date": selected_date
        })
        form.fields['resident'].queryset = available_residents
    print("Block ID in create_slip:", block.id)
    context = {
        "form": form,
        "block1": block,
        "residents": residents,
        "available_residents": available_residents,
        "selected_date": selected_date
    }
    return render(request, "society/create_slip.html", context)

@login_required
def get_available_residents_ajax(request, block_id):
    block = get_object_or_404(Block, id=block_id)
    residents = block.residents.all().order_by('flat_no')
    date_str = request.GET.get("date")
    available = []

    if date_str:
        try:
            date_val = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
            year, month = date_val.year, date_val.month

            existing_slips = MaintenanceSlip.objects.filter(
                block=block,
                maintenance_charge_date__year=year,
                maintenance_charge_date__month=month
            ).values_list('resident_id', flat=True)

            available = residents.exclude(id__in=existing_slips)

        except ValueError:
            pass

    data = [{"id": r.id, "name": r.name, "flat_no": r.flat_no} for r in available]
    return JsonResponse({"residents": data})

