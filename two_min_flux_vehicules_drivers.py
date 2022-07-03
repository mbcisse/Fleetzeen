import authotoken
import requests
import odoo_acces
import xmlrpc.client
import json
import half_flow_odoo_topivotdb
from datetime import datetime, timedelta

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(odoo_acces.url))
uid = common.authenticate(odoo_acces.db, odoo_acces.username, odoo_acces.password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(odoo_acces.url))


def get_drivers_ids(ids):
    drivers_list=[]
    for var in ids:
        drivers_list.append(var['driver_id'][0])
    return drivers_list

#getting drivers_ids_list:

def get_alpha_taxis_with_ids():
    today = datetime.today() 
    alpha_taxis_ids= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'alpha.taxis', 'search_read',
     [[('radio_contract', 'not like', 'S%'), ('start_date', '!=', False),'|',('end_date', '=', False),
     ('end_date', '>=', today)]], {'fields': ['driver_id', 'start_date','end_date', 'status'  ]})

    return get_drivers_ids(alpha_taxis_ids)


def get_fleet_vehicule_assignation(driver_ids):

    db_last_update= half_flow_odoo_topivotdb.getting_db_last_update_from_pivotdb(driver_ids)
    
    if db_last_update=="last_update_vehicule_actual":
        db_last_update= half_flow_odoo_topivotdb.getting_actual_db_last_update_from_pivotdb(driver_ids)
    else:
       db_last_update= half_flow_odoo_topivotdb.getting_prec_db_last_update_from_pivotdb(driver_ids)

    var= driver_ids
    count= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log', 'search_count', [[('driver_id','=', var), ('__last_update', '>', db_last_update)]])
    
    if count==1:
        resul= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log', 
        'search_read', [[['driver_id','=', var]]],  {'fields': ['vehicle_id', 'driver_id', 'date_start', 'date_end', '__last_update']} )
        id_vehicule_prec=id_vehicule_actual= resul[0]['vehicle_id']
        start_date_vehic_prec=start_date_vehic_actual= resul[0]['date_start']
        end_date_vehic_prec= end_date_vehic_actual= resul[0]['date_end']
        last_update= resul[0]['__last_update']
            
        return id_vehicule_prec[0], id_vehicule_actual[0], start_date_vehic_prec, start_date_vehic_actual, end_date_vehic_prec, end_date_vehic_actual, last_update, last_update

    elif count > 1:
        resul= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log',
        'search_read', [[['driver_id','=', var]]],  {'fields': ['vehicle_id', 'driver_id', 'date_start', 'date_end', '__last_update' ]} )
        id_vehicule_actual= resul[0]['vehicle_id']
        start_date_vehic_actual= resul[0]['date_start']
        end_date_vehic_actual= resul[0]['date_end']
        last_update_actual= resul[0]['__last_update']


        id_vehicule_prec= resul[1]['vehicle_id']
        start_date_vehic_prec= resul[1]['date_start']
        end_date_vehic_prec= resul[1]['date_end']
        last_update_prec= resul[1]['__last_update']

          
        return id_vehicule_prec[0], id_vehicule_actual[0], start_date_vehic_prec, start_date_vehic_actual, end_date_vehic_prec, end_date_vehic_actual, last_update_actual,last_update_prec
    
    else:
        return False
    

def get_res_partner_with_ids(driver_id):

    db_x_studio_x_lastupdatedate_flow= half_flow_odoo_topivotdb.getting_db_x_studio_x_lastupdatedate__flow_from_pivotdb(driver_id)
    
    if db_x_studio_x_lastupdatedate_flow !='false':
        drivers_datas= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read',
        [[('is_driver', '=', True), ('id', '=', driver_id), ('x_studio_x_lastupdatedate_flow', '!=', 'False'), 
        ('x_studio_x_lastupdatedate_flow', '>', db_x_studio_x_lastupdatedate_flow)]], 
        {'fields': ['radio_code', 'alpha_taxis_ids', 'driver_lastname', 'driver_firstname',
        'email','mobile', 'street','zip', 'city', 'ref', 'display_name', 'x_studio_x_lastupdatedate_flow']})
        
        return drivers_datas
    else:
        return []

def getting_drivers_vehicules_datas():

    drivers_ids=get_alpha_taxis_with_ids()

    print("Len: ", len(drivers_ids))
    
    final_result=[]
    
    #half_flow_odoo_topivotdb.purges_pivotdb_purge("drivers_vehicules")

    for driver_id in drivers_ids:
        
        if len(get_res_partner_with_ids(driver_id)) > 1:
            
            datas_res_partner = get_res_partner_with_ids(driver_id)[0]
            # Perfom a new update here with the datas of the new divers from get_res_partner_with_ids(call in update function)
            # datas_alpha_taxis = get_alpha_taxis_datas(driver_id)[0], we don't need any information into alpha_taxis_datas
            
            datas_fleet_vehicule_assign= get_fleet_vehicule_assignation(driver_id)
            # Perfom a new update here with the datas of the new divers from get_fleet_vehicule_assignation(call in update function)
        
        if datas_fleet_vehicule_assign is not False:
            id= datas_res_partner['id']
            radio_code= datas_res_partner['radio_code']
            alpha_taxis_ids= datas_res_partner['alpha_taxis_ids']
            lastupdatedate_res_partner= datas_res_partner['x_studio_x_lastupdatedate_flow']
            
            #start_date_alpha_taxis= datas_alpha_taxis['start_date']
            #end_date_alpha_taxis= datas_alpha_taxis['end_date']
            #status= datas_alpha_taxis['status']
            
            driver_last_name= datas_res_partner['driver_lastname']
            driver_first_name= datas_res_partner['driver_firstname']
            email= datas_res_partner['email']
            mobile= datas_res_partner['mobile']
            adresse= str(datas_res_partner['street']) + " " +  str(datas_res_partner['zip']) +  str(datas_res_partner['zip']) + " " + str(datas_res_partner['city'])
            group_client_id= datas_res_partner['ref']
            display_name= datas_res_partner['display_name']
            id_vehicule_prec, id_vehicule_actual, start_date_vehic_prec, start_date_vehic_actual, end_date_vehic_prec, end_date_vehic_actual, last_update_vehicule_prec, last_update_vehicule_actual=datas_fleet_vehicule_assign
                  
            #half_flow_odoo_topivotdb.full_half_flow_VehicDrivers_to_pivotdb= This will be an update wtith the required datas and then send this datas to fleet

            half_flow_odoo_topivotdb.full_half_flow_VehicDrivers_to_pivotdb( 
              id, radio_code, alpha_taxis_ids,driver_last_name,  driver_first_name, email, mobile, adresse, 
              group_client_id, display_name, id_vehicule_prec, start_date_vehic_prec, end_date_vehic_prec, id_vehicule_actual, 
              start_date_vehic_actual, end_date_vehic_actual, lastupdatedate_res_partner, last_update_vehicule_prec, 
              last_update_vehicule_actual)


            # why not do here the insert process to the corresponded database tables with the required datas:  
            # full_half_flow_VehicDrivers_to_pivotdb to check

        else:
            pass
    return final_result

if __name__ == "__main__":    
    result= getting_drivers_vehicules_datas()
    '''with open("first_extractions" + "_datas" + ".json", "w") as outfile:
                outfile.write(json.dumps(result, indent=4))
'''