import authotoken
import requests
import odoo_acces
import xmlrpc.client
import json
from datetime import datetime, timedelta
import half_flow_odoo_topivotdb

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_acces.url))
uid = common.authenticate(odoo_acces.db, odoo_acces.username, odoo_acces.password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_acces.url))

def get_res_partner_family():
    
    family= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read',
     [[('company_group_id', '=', False), ('is_subscriber', '=', True), ('parent_id', '=', False)]],
     {'fields': ['subscriber_code_str', 'display_name', 'subscriber_code_int', 'subscriber_in','subscriber_out' ]})
    
    half_flow_odoo_topivotdb.purges_pivotdb_purge("company")
    
    for cmp in family:
        half_flow_odoo_topivotdb.full_half_flow_company_to_pivotdb(cmp['id'], cmp['display_name'], cmp['subscriber_code_int'], cmp['subscriber_out'], cmp['subscriber_code_str'])

    return family

def get_res_partner_abonne():

    contracts= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read',
     [[('company_group_id', '!=', False), ('is_subscriber', '=', True), ('parent_id', '=', False)]], 
     {'fields': ['subscriber_code_str',  'ref', 'display_name', 'company_group_id','subscriber_in', 'subscriber_out', 
     'street',  'city', 'zip', 'country_id']})
    
    #populate here the database Table named contracts with the requred datas
    half_flow_odoo_topivotdb.purges_pivotdb_purge("contract")

    for cmp in contracts:
        half_flow_odoo_topivotdb.full_half_flow_contracts_to_pivotdb(cmp['id'], cmp['subscriber_code_str'], cmp['ref'], cmp['display_name'], cmp['company_group_id'], cmp['subscriber_in'], cmp['subscriber_out'], cmp['street'], cmp['city'], cmp['zip'], cmp['country_id'])

    return contracts


def get_res_partner_service():
    # display_name, name
    
    service= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read',
     [[('company_group_id', '!=', False), ('is_subscriber', '=', True), ('parent_id', '!=', False)]], 
     {'fields':['subscriber_code_str', 'name', 'company_id', 'parent_id', 'subscriber_in', 'subscriber_out', 'mobile',
     'email', 'street', 'city', 'zip', 'country_id', 'comment_for_operator','comment_for_driver']})
  
    #populate here the database Table named service with the requred datas
    half_flow_odoo_topivotdb.purges_pivotdb_purge("service")
    for cmp in service:
        half_flow_odoo_topivotdb.full_half_flow_services_to_pivotdb(cmp['id'], cmp['subscriber_code_str'], cmp['name'], cmp['company_id'], cmp['parent_id'], cmp['subscriber_in'],cmp['subscriber_out'], cmp['mobile'], cmp['email'], cmp['street'], cmp['city'], cmp['zip'], cmp['country_id'], cmp['comment_for_operator'], cmp['comment_for_driver'])
    return service

    return service


if __name__ == "__main__":    
    company= get_res_partner_service()
    '''with open("get_res_partner_family_full" + "_datas" + ".json", "w") as outfile:
                outfile.write(json.dumps(company, indent=4))'''

