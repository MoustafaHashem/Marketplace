from django.shortcuts import render,redirect
from core.models import UserProfile
from items.models import Items, Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from decimal import Decimal


def account_page(request):
    user_profile = None
    available_items = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            available_items = Items.objects.filter(owned_by=user_profile)
            
        except UserProfile.DoesNotExist:
            user_profile = None
            available_items = None

    return render(request, 'inventory/inventory.html', {'available_items': available_items})
def item_detail(request, id):
    product = Items.objects.get(id=id)
    return render(request, 'inventory/item_detail.html', {'product': product})


@login_required
def add_item(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to add items.")
        return redirect('login')  
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            category_name = request.POST.get('category')  
            price_str = request.POST.get('price')
            quantity_str = request.POST.get('quantity', '1')  # default to 1 if missing

            try:
                price = float(price_str)
                quantity = int(quantity_str)
            except ValueError:
                messages.error(request, "Price must be a number and quantity must be an integer.")
                return redirect('add_item')
            # Convert to Decimal first
            # price = Decimal(price) if price else None
            # if not price or price <= 0:  # Proper numerical comparison
            #     messages.error(request, "Please enter a valid positive price")
            #     return redirect('add_item')
            
            description = request.POST.get('description')
            image = request.FILES.get('image')
            # quantity = request.POST.get('quantity')  # Default to 1 if not provided
            

            # Validate image
            if not image:
                messages.error(request, "Please upload an image for the item.")
                return redirect('add_item')

            # Validate required fields
            if not all([name, category_name, price]):  
                messages.error(request, "Please fill all required fields.")
                return redirect('add_item')
            
            # Get or create the category by name
            category, created = Category.objects.get_or_create(name=category_name)
            
            # Create and save the new item
            Items.objects.create(
                name=name,
                category=category,  # Now using the category object directly
                price=price,
                description=description,
                image=image,
                quantity=quantity,  # Default quantity set to 1
                owned_by=UserProfile.get_profile_by_user(user=request.user), 
            )
            
            messages.success(request, "Item added successfully!")
            return redirect('Inventory')
            
        except Exception as e:
            messages.error(request, f"Error adding item: {str(e)}")
            return redirect('add_item')
    
    # GET request - show the form
    categories = Category.objects.all()
    return render(request, 'inventory/add_item.html', {'categories': categories})



@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.get_or_create(name=name.strip())
            messages.success(request, "Category added successfully!")
        else:
            messages.error(request, "Category name cannot be empty.")
    return redirect('Inventory') 