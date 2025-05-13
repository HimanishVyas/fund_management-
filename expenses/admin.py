from django.contrib import admin
from django.apps import apps

# Automatically get all models from this app
app = apps.get_app_config('expenses')  # Replace with your actual app name

for model in app.get_models():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
