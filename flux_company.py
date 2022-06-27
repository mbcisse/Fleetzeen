import authotoken
import requests
import odoo_acces
import xmlrpc.client
import json
from datetime import datetime, timedelta

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_acces.url))
uid = common.authenticate(odoo_acces.db, odoo_acces.username, odoo_acces.password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_acces.url))

def get_res_partner_family():
    
    family= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read',
     [[('company_group_id', '=', False), ('is_subscriber', '=', True), ('parent_id', '=', False)]],
     {'fields': ['display_name', 'subscriber_code_int', 'subscriber_in','subscriber_out' ]})
 
    #populate here the database Table named company with the requred datas

    return family

def get_res_partner_abonne():
    
    family= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read',
     [[('company_group_id', '!=', False), ('is_subscriber', '=', True), ('parent_id', '=', False)]], 
     {'fields': ['subscriber_code_int', 'ref', 'display_name', 'subscriber_in', 'subscriber_out', 
     'street',  'city', 'zip', 'country_id']})
    
    #populate here the database Table named contracts with the requred datas
    return family

def get_res_partner_service():
    
    service= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read',
     [[('company_group_id', '!=', False), ('is_subscriber', '=', True), ('parent_id', '!=', False)]], 
     {'fields':['subscriber_code_int', 'company_id', 'parent_id', 'subscriber_in', 'subscriber_out', 'mobile',
     'email', 'street', 'city', 'zip', 'country_id', 'comment_for_operator','comment_for_driver']})
    
    #populate here the database Table named service with the requred datas
    return service


if __name__ == "__main__":    
    company= get_res_partner_family()
    with open("get_res_partner_family_full" + "_datas" + ".json", "w") as outfile:
                outfile.write(json.dumps(company, indent=4))

