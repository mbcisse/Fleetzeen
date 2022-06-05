import authotoken
import requests
import odoo_acces
import xmlrpc.client

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_acces.url))
uid = common.authenticate(odoo_acces.db, odoo_acces.username, odoo_acces.password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_acces.url))

def get_drivers():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_driver', '=', True]]], 
    {'fields': ['ref', 'driver_lastname', 'driver_firstname', 'shares_coop_id', 'bgt_in', 'bgt_out', 'mobile', 'email','city'], 'limit': 10})


def get_vehicules():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle', 'search_read', [], {'fields': ['name', 'driver_id','license_plate', 'brand_id', 
    'model_id', 'color', 'co2'], 'limit': 1})

def get_company():
    models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_company', '=', True]]], {'fields': ['ref', 'name', 'comment'], 'limit': 5})

def get_subscribers():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read', [[['is_subscriber', '=', True]]], {'fields': ['name', 'parent_id'], 'limit': 5})

def get_contracts():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.log.contract', 'search_read', [], {'limit': 1})    

def get_services():
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.log.services', 'search_read', [], {'limit': 1})    
    


if __name__ == "__main__":
    #print(get_drivers())
    #print(get_vehicules())
    #print(get_company())
    print(get_services())

