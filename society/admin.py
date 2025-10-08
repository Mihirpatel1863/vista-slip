from django.contrib import admin
from .models import Profile, Block, Resident, MaintenanceSlip


@admin.register(MaintenanceSlip)
class MaintenanceSlipAdmin(admin.ModelAdmin):
    list_display = ('slip_no', 'block_name', 'resident_name', 'amount_number', 'payment_method', 'date')
    list_filter = ('block', 'payment_method', 'date')
    search_fields = ('slip_no', 'resident__name', 'block__name')

    def block_name(self, obj):
        return obj.block.name
    block_name.short_description = "Block"

    def resident_name(self, obj):
        return obj.resident.flat_no
    resident_name.short_description = "Resident"


admin.site.register(Profile)
admin.site.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)   
admin.site.register(Resident)
class ResidentAdmin(admin.ModelAdmin):          
    list_display = ('name', 'flat_no', 'block_name')
    list_filter = ('block',)
    search_fields = ('name', 'flat_no', 'block__name')

    def block_name(self, obj):
        return obj.block.name
    block_name.short_description = "Block"  
