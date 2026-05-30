from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from .forms import ProductForm
import json


# หน้าร้านค้า
def index(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'bakery/index.html', {'products': products})


# Login
def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin_panel')
    
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_panel')
        else:
            error = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'
    
    return render(request, 'bakery/login.html', {'error': error})


# Logout
def logout_view(request):
    logout(request)
    return redirect('index')


# หน้าแอดมิน
@login_required
def admin_panel(request):
    products = Product.objects.all()
    form = ProductForm()
    return render(request, 'bakery/admin.html', {'products': products, 'form': form})


# เพิ่มสินค้า
@login_required
@require_POST
def product_add(request):
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors})


# แก้ไขสินค้า
@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    # GET: ส่งข้อมูลสินค้ากลับ
    return JsonResponse({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description,
        'image_url': product.image.url if product.image else '',
    })


# ลบสินค้า
@login_required
@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.image.delete(save=False)
    product.delete()
    return JsonResponse({'success': True})


# Toggle เปิด/ปิดขาย
@login_required
@require_POST
def product_toggle(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_available = not product.is_available
    product.save()
    return JsonResponse({'success': True, 'is_available': product.is_available})
