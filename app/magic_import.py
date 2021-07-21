"""
This module is configure django code outside of views context
Import this to use django models
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

django.setup()
