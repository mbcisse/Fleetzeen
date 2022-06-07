import authotoken
from datetime import date
from datetime import timedelta
import requests
import odoo_acces
import xmlrpc.client

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_acces.url))
uid = common.authenticate(odoo_acces.db, odoo_acces.username, odoo_acces.password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_acces.url))

'''today = date.today()
print("Today is: ", today)
# Yesterday date
yesterday = today - timedelta(days = 1)
print("Yesterday was: ", yesterday)
yesterday= str(yesterday)
'''

def get_vehic_drivers():
    
    id_drivers_from_vehicule= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle', 'search_read', [], {'fields': ['driver_id']}) 

    id_drivers_from_driver=   models.execute_kw(odoo_acces.db, uid, odoo_acces.password,  'res.partner', 'search_read', 
    [[[('is_driver', '=', True),('id_drivers_from_vehicule','in', 'driver_id'  
    )]]])

    return id_drivers_from_driver


def get_drivers():
    drivers= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_driver', '=', True]]], 
    {'fields': ['radio_code', 'driver_lastname', 'driver_firstname', 'email','mobile', 'street','zip', 'city', 'ref', 'display_name']})
          
    return drivers

def get_champs_drivers():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'fields_get', [], {'attributes': ['string', 'help', 'type']})

'''ids= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_driver', '=', True]]])

    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'fields_get', [], {'attributes': ['string', 'help', 'type']})
'''

def get_vehicules():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle', 'search_read', [], {'fields': ['name', 'driver_id','license_plate', 'brand_id', 
    'model_id', 'color', 'co2']})


def get_company():
    models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_company', '=', True]]], {'fields': ['ref', 'name', 'comment'], 'limit': 5})

def get_subscribers():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_subscriber', '=', True]]], {'fields': ['name', 'parent_id'], 'limit': 5})

def get_contracts():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.log.contract', 'search_read', [], {'limit': 1})    

def get_services():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.log.services', 'search_read', [], {'limit': 10})    
    
def get_courses():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'driver.platform.ride', 'search_read', [], {'limit': 10})    

    

if __name__ == "__main__":
    print(get_drivers())
    #print(get_vehicules())
    #print(get_company())
    #print(get_services())
    #get_vehic_drivers()
    #print(get_champs_drivers())
    #print(get_courses())