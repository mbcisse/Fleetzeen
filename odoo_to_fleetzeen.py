import authotoken
import requests
import odoo_acces
import xmlrpc.client
import json
from datetime import datetime, timedelta

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_acces.url))
uid = common.authenticate(odoo_acces.db, odoo_acces.username, odoo_acces.password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_acces.url))



def get_fields_models(model_name):

    fields= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, model_name, 'fields_get', [], {'attributes': ['string', 'help', 'type']})
    #fields= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, model_name, 'fields_get',[[['is_driver', '=', True]]], {'attributes': ['string', 'help', 'type']})
    
    with open(model_name + "_fields" + ".json", "w") as outfile:
                outfile.write(json.dumps(fields, indent=4))

def get_vehic_drivers():
    
    id_drivers_from_vehicule= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle', 'search_read', [], {'fields': ['driver_id']}) 

    id_drivers_from_driver=   models.execute_kw(odoo_acces.db, uid, odoo_acces.password,  'res.partner', 'search_read', 
    [[[('is_driver', '=', True),('id_drivers_from_vehicule','in', 'driver_id'  
    )]]])

    return id_drivers_from_driver


def get_drivers():
    drivers= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_driver', '=', True]]], 
    {'fields': ['radio_code', 'alpha_taxis_ids', 'driver_lastname', 'driver_firstname', 'email','mobile', 'street','zip', 'city', 'ref', 'display_name']})

    with open("drivers_new" + "_fields" + ".json", "w") as outfile:
                outfile.write(json.dumps(drivers, indent=4))
    # Which on to describe the contracts flux ou bien on utilise res.partner' is_subscriber ou bien fleet.vehicle.log.contract
          
    #return drivers

def get_champs_drivers():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'fields_get', [], {'attributes': ['string', 'help', 'type']})

'''ids= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_driver', '=', True]]])

    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'fields_get', [], {'attributes': ['string', 'help', 'type']})
'''

def get_vehicules():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle', 'search_read', [[['license_plate','=' '']]], {'fields': ['name', 'driver_id','license_plate', 'brand_id', 
    'model_id', 'color', 'co2']})


def get_company():
    models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_company', '=', True]]], {'fields': ['ref', 'name', 'comment'], 'limit': 5})

def get_subscribers():
    #return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_subscriber', '=', True]]], {'fields': ['name', 'parent_id'], 'limit': 5})
    result= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['name', '=', 'Service test']]])

    with open("service" + "_fields" + ".json", "w") as outfile:
                outfile.write(json.dumps(result, indent=4))
    # Which on to describe the contracts flux ou bien on utilise res.partner' is_subscriber ou bien fleet.vehicle.log.contract

def get_alpha_taxis_filtered():

    datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d 00:00:00')
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    datef=datetime.today().strftime( '%Y-%m-%d 00:00:00')
    print("This the date:", datef)
    
    #return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_subscriber', '=', True]]], {'fields': ['name', 'parent_id'], 'limit': 5})
    result1= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'alpha.taxis', 'search_read', [[('radio_contract', 'not like', 'S%'),
        ('start_date', '<=', today),'|',('end_date', '=', False),('end_date', '>=', today)]], {'fields': ['id']})   
    
    #Get all the alpha_taxis ids code array and the the corresponding drivers based on this ids.
    '''ids= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'alpha.taxis', 'search', [[('radio_contract', 'not like', 'S%'),
        ('start_date', '<=', today),'|',('end_date', '=', False),('end_date', '>=', today)]])  '''

    print(len(result1))
    print((result1))
    with open("alpha_taxis_datas" + "_fields" + ".json", "w") as outfile:
                outfile.write(json.dumps(result1, indent=4))
    #return result1
    #result= list()

    '''for var in result1:
        if 'S' not in var['radio_contract'] and var['start_date'] <='2022-06-13 00:00:00'and  (var['end_date'] == False or str(var['end_date']) >= '2022-06-13 00:00:00'):
            result.append(var)
        else:
            pass

    print(len(result))
    with open("alpha_taxis_datas" + "_fields" + ".json", "w") as outfile:
                outfile.write(json.dumps(result, indent=4))
'''

def get_contracts():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.log.contract', 'search_read', [], {'limit': 1})    

def get_services():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.log.services', 'search_read', [], {'limit': 10})    
    
def get_courses():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'driver.platform.ride', 'search_read', [], {'limit': 10})    

def get_alpha_in_out():
    drivers= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_driver', '=', True]]], 
    {'fields': ['radio_code', 'alpha_taxis_ids', 'driver_lastname', 'driver_firstname', 'alpha_in','alpha_out']})

    with open("get_alpha_in_out" + "_fields" + ".json", "w") as outfile:
                outfile.write(json.dumps(drivers, indent=4))
    

if __name__ == "__main__":
    #print(get_drivers())
    #print(get_vehicules())
    #print(get_company())
    #print(get_services())
    #get_vehic_drivers()
    #print(get_champs_drivers())
    #print(get_subscribers())
    #get_fields_models('fleet.vehicle')
    #get_alpha_taxis()
    #get_alpha_in_out()
    print(get_alpha_taxis_filtered())
