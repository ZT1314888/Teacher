#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib import admin

print("=" * 60)
print("Django Admin 注册检查")
print("=" * 60)

if admin.site._registry:
    print(f"\n已注册的模型数量: {len(admin.site._registry)}")
    print("\n已注册的模型:")
    for model, admin_class in admin.site._registry.items():
        app_label = model._meta.app_label
        model_name = model.__name__
        verbose_name = model._meta.verbose_name
        print(f"  ✅ {app_label}.{model_name} ({verbose_name})")
else:
    print("\n❌ 没有注册任何模型到 admin！")

print("\n" + "=" * 60)
