from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Cliente, Fornecedor

admin.site.register(Usuario, UserAdmin)
admin.site.register(Cliente)
admin.site.register(Fornecedor)
