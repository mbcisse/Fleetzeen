import authotoken
import requests
import odoo_acces
import xmlrpc.client
import json
from datetime import datetime, timedelta

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_acces.url))
uid = common.authenticate(odoo_acces.db, odoo_acces.username, odoo_acces.password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_acces.url))

def get_drivers_ids(ids):
    
    drivers_list=[]
    drivers_list_1=[]
    
    for var in ids:

        drivers_list_1.append(var['driver_id'])
        drivers_list.append(var['driver_id'][0])
        
   
    return drivers_list, drivers_list_1

def get_alpha_taxis_with_ids():

    today = datetime.today() 
    alpha_taxis_ids= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'alpha.taxis', 'search_read',
     [[('radio_contract', 'not like', 'S%'), ('start_date', '!=', False),'|',('end_date', '=', False),
     ('end_date', '>=', today)]], {'fields': ['driver_id', 'start_date','end_date', 'status'  ]})


    print('get_alpha_taxis_with_ids', alpha_taxis_ids)
    drivers_list, drivers_1= get_drivers_ids(alpha_taxis_ids)
    
    return drivers_list, drivers_1, alpha_taxis_ids


def get_res_partner_with_ids():
    
    drivers_ids, drivers_1, alpha_taxis_ids_datas = get_alpha_taxis_with_ids()

    drivers_datas= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read',
     [[[('is_driver', '=', True), ('id', 'in', drivers_ids)]]], {'fields': ['radio_code', 'alpha_taxis_ids', 'driver_lastname', 'driver_firstname',
      'email','mobile', 'street','zip', 'city', 'ref', 'display_name']})
    
    return drivers_datas



def get_fleet_vehicule_assignation():
    
    drivers_ids, drivers_ids_1, alpha_taxis_ids = get_alpha_taxis_with_ids()
    
    print("drivers_ids", drivers_ids)
    print("drivers_ids_1", drivers_ids_1)
    print("alpha_taxis_ids", alpha_taxis_ids)

    for var in drivers_ids:
        
        count= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log', 'search_count', [[['driver_id','=', var]]] )
        
        if count==1:
            resul= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log', 
            'search_read', [[['driver_id','=', var]]],  {'fields': ['vehicle_id', 'driver_id', 'date_start', 'date_end' ]} )
            
            id_vehicule_prec=id_vehicule_actual= resul[0]['vehicle_id']
            start_date_vehic_prec=start_date_vehic_actual= resul[0]['date_start']
            end_date_vehic_prec= end_date_vehic_actual= resul[0]['date_end']
            
            print(id_vehicule_prec[0], id_vehicule_actual[0], start_date_vehic_prec, start_date_vehic_actual, end_date_vehic_prec, end_date_vehic_actual)

           
     
        elif count > 1:

            resul= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log',
             'search_read', [[['driver_id','=', var]]],  {'fields': ['vehicle_id', 'driver_id', 'date_start', 'date_end' ]} )

            id_vehicule_actual= resul[0]['vehicle_id']
            start_date_vehic_actual= resul[0]['date_start']
            end_date_vehic_actual= resul[0]['date_end']

            id_vehicule_prec= resul[1]['vehicle_id']
            start_date_vehic_prec= resul[1]['date_start']
            end_date_vehic_prec= resul[1]['date_end']
            
            print(id_vehicule_prec[0], id_vehicule_actual[0], start_date_vehic_prec, start_date_vehic_actual, end_date_vehic_prec, end_date_vehic_actual)

        
        else:
            pass



    
    '''resul= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log', 
    'search_read', [[['driver_id','=', 60491]]],  {'fields': ['vehicle_id', 'driver_id', 'date_start', 'date_end' ]} )

    with open("fleet_vehicle_assignation_log_filtered" + "_datas" + ".json", "w") as outfile:
                outfile.write(json.dumps(resul, indent=4))

    return resul'''



def get_num_contrat_alpha_taxis_ids(drivers_ids,alpha_taxis_datas):

    for id in drivers_ids:
        for var in alpha_taxis_datas:
            if id in alpha_taxis_datas['driver_id']:
                num_alpha_taxis_ids



    
    pass

if __name__ == "__main__":
    print(get_fleet_vehicule_assignation())
    #print(get_alpha_taxis_with_ids())
