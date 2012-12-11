from django.contrib import admin
import shopping.models

# This file enables using the /admin/-interface to see/modify the models.

admin.site.register(shopping.models.Customer)
admin.site.register(shopping.models.Category)
admin.site.register(shopping.models.Asset)
admin.site.register(shopping.models.Basket)
admin.site.register(shopping.models.BasketItem)
admin.site.register(shopping.models.Grade)
admin.site.register(shopping.models.GradeHistory)
