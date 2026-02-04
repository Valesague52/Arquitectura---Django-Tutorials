from django.shortcuts import render
from django.views.generic import TemplateView
from django import forms
from django.shortcuts import render, redirect

class HomePageView(TemplateView):
    template_name = 'pages/home.html'
    
class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page",
            "author": "Developed by: Helen Sanabria",
        })
        return context    
    
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact us - Online Store",
            "subtitle": "Contact Information",
        })
        return context    
    
from django.views import View

class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV"},
        {"id":"2", "name":"iPhone", "description":"Best iPhone"},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast"},
        {"id":"4", "name":"Glasses", "description":"Best Glasses"}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'
    
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)

from django.shortcuts import render, redirect  # Añadir redirect
from django.http import HttpResponseRedirect  # Añadir esta importación

class ProductShowView(View):
    template_name = 'products/show.html'
    
    def get(self, request, id):
        try:
            # Intentar convertir a número y validar rango
            product_id = int(id)
            if product_id < 1 or product_id > len(Product.products):
                return redirect('home')  # Redirigir si ID no válido
            
            product = Product.products[product_id-1]
            viewData = {}
            viewData["title"] = product["name"] + " - Online Store"
            viewData["subtitle"] = product["name"] + " - Product information"
            viewData["product"] = product
            
            return render(request, self.template_name, viewData)
            
        except (ValueError, IndexError):
            # Si hay error (no es número o fuera de rango)
            return redirect('home')
        
        
        
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)
    
    # ACTIVIDAD 7: Validar que precio sea mayor a 0
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'
    
    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            # ACTIVIDAD 8: Redirigir a página de éxito
            return redirect('success')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)

# ACTIVIDAD 8: Vista para mensaje de éxito
class ProductSuccessView(TemplateView):
    template_name = 'products/success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Success - Online Store",
            "subtitle": "Product Created Successfully",
            "message": "Product created successfully!",
        })
        return context        