from django.shortcuts import render
from .models import Category, Items

def items(request):
    query = request.GET.get('query', '')
    filters = request.GET.getlist('filters')

    # Get all categories
    cat = Category.objects.all()

    # Get all products
    pro = Items.objects.filter(for_sale=True)

    # Apply filters if a query is provided
    if query:
        if 'name' in filters:
            pro = pro.filter(name__icontains=query)
        if 'seller' in filters:
            pro = pro.filter(owned_by__user__username__icontains=query)
        if 'category' in filters:
            pro = pro.filter(category__name__icontains=query)
        else:
            # If no specific filter is selected, show all products matching the query
            pro = pro.filter(
                name__icontains=query
            ) | pro.filter(
                owned_by__user__username__icontains=query
            ) | pro.filter(
                category__name__icontains=query
            )
   

    context = {
        'cat': cat,
        'pro': pro,
        'query': query,
        'filters': filters,
    }
    return render(request, 'items/items.html', context)