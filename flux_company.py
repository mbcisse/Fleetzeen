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
     [[('company_id', '=', False), ('is_subscriber', '=', True), ('parent_id', '=', False)]],
     {'fields': ['display_name', 'subscriber_code_int', 'subscriber_in','subscriber_out' ]})
   
    return family



def get_res_partner_abonne():
    
    family= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read',
     [[('company_id', '!=', False), ('is_subscriber', '=', True), ('parent_id', '=', False)]], 
     {'fields': ['subscriber_code_int', 'Ref', 'display_name','compan,y_id', 'subscriber_in', 'subscriber_out', 
     'street', 'rue2', 'city', 'zip', 'country_id'  ]})
    
    return family

def get_res_partner_service():
    
    family= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read',
     [[('company_id', '!=', False), ('is_subscriber', '=', True), ('parent_id', '!=', False)]], 
     {'fields':['subscriber_code_int', 'company_id', 'parent_id', 'subscriber_in', 'subscriber_out', 'mobile',
     'email', 'street', 'city', 'zip', 'country_id', 'comment_for_operator','comment_for_driver']}
     )
    
    return family


if __name__ == "__main__":    
    company= get_res_partner_abonne()
    with open("Full_contracts_abonnes" + "_datas" + ".json", "w") as outfile:
                outfile.write(json.dumps(company, indent=4))

