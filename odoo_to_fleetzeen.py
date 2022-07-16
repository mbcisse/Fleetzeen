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


def get_company_test():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [], {'fields': ['ref', 'name', 'comment'], 'limit': 1})

def get_company():
    models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_company', '=', True]]], {'fields': ['ref', 'name', 'comment'], 'limit': 5})


def get_subscribers():
    #return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_subscriber', '=', True]]], {'fields': ['name', 'parent_id'], 'limit': 5})
    result= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['name', '=', 'Service test']]])

    with open("service" + "_fields" + ".json", "w") as outfile:
                outfile.write(json.dumps(result, indent=4))
    # Which on to describe the contracts flux ou bien on utilise res.partner' is_subscriber ou bien fleet.vehicle.log.contract

def get_fleet_vehicule_with_ids(ids):
    
    res_part= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log', 'search_read',
     [[ ('id', 'in', ids), ]])


    pass

def get_res_partner_with_ids(ids):
    res_part= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search',
     [[('is_company', '=', True), ('id', 'in', ids)]])
    return res_part

def get_alpha_taxis_with_ids():

    datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d 00:00:00')
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    datef=datetime.today().strftime( '%Y-%m-%d 00:00:00')
    print("This the date:", datef)
    

    #Get all the alpha_taxis ids code array and the the corresponding drivers based on this ids.
    alpha_taxis_ids= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'alpha.taxis', 'search_read', [[('radio_contract', 'not like', 'S%'),
        ('start_date', '!=', False),'|',('end_date', '=', False),('end_date', '>=', today)]], {'fields': ['driver_id']})
    
    if [12448, 'ADAMS DANIEL'] in get_drivers_ids_1(alpha_taxis_ids):
        print("YES YES YES")
    #return get_fleet_vehicle_assignation_log(alpha_taxis_ids)
    #return get_res_partner_with_ids(get_drivers_ids(alpha_taxis_ids))

def get_drivers_ids(ids):

    drivers_list=[]
    for var in ids:
        drivers_list.append(var['driver_id'][0])
    
    return drivers_list
    

def get_drivers_ids_1(ids):

    drivers_list=[]
    for var in ids:
        drivers_list.append(var['driver_id'])
    
    return drivers_list
    
def get_services_aux():

    service= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read',
     [[('company_group_id', '!=', False), ('is_subscriber', '=', True), ('parent_id', '!=', False)]], 
     {'fields':['subscriber_code_str', 'name', 'company_group_id', 'parent_id', 'subscriber_in', 'subscriber_out', 'mobile',
     'email', 'street', 'city', 'zip', 'country_id', 'comment_for_operator','comment_for_driver']})
    with open("service" + "_datas" + ".json", "w") as outfile:
                outfile.write(json.dumps(service, indent=4))

def get_alpha_taxis_datas():
    today = datetime.today()
    resul= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'alpha.taxis', 'search_read',  [[('radio_contract', 'not like', 'S%'),
        ('start_date', '!=', False),'|',('end_date', '=', False),('end_date', '>=', today)]] )
    with open("alpha_taxis_filtered" + "_datas" + ".json", "w") as outfile:
                outfile.write(json.dumps(resul, indent=4))


def get_fleet_vehicle_assignation_log():
    
    resul= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log', 'search_read', [] )
    with open("fleet_vehicle_assignation_log" + "_datas" + ".json", "w") as outfile:
                outfile.write(json.dumps(resul, indent=4))

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
    #print(get_fleet_vehicle_assignation_log())
    #print(get_services())
    #get_vehic_drivers()
    #print(get_champs_drivers())
    #print(get_subscribers())
    #get_fields_models('alpha.taxis')
    #get_alpha_taxis()
    #get_alpha_in_out()
    #print(get_alpha_taxis_datas())
    #print(get_fields_models('fleet.vehicle.assignation.log'))
    #print(get_company_test())
    #print(get_alpha_taxis_with_ids())
    get_services_aux()
