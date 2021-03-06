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


def get_drivers_ids(ids):
    drivers_list=[]
    for var in ids:
        drivers_list.append(var['driver_id'][0])
    return drivers_list

def get_only_end_dates(alpha_taxis_ids_end):
    return alpha_taxis_ids_end[0]['end_date']
     
    

def get_alpha_taxis_with_ids():
    today = datetime.today() 
    alpha_taxis_ids= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'alpha.taxis', 'search_read',
     [[('radio_contract', 'not like', 'S%'), ('start_date', '!=', False),'|',('end_date', '=', False),
     ('end_date', '>=', today)]], {'fields': ['driver_id', 'start_date','end_date', 'status']})

    return get_drivers_ids(alpha_taxis_ids)

def getting_alpha_end_dates_actual(driver_ids):
    alpha_taxis_ids_end= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'alpha.taxis', 'search_read',
     [[['driver_id','=', driver_ids]]], {'fields': ['end_date']})
    
    return get_only_end_dates(alpha_taxis_ids_end)

#Add here the start date and endate parameters from alpha.taxis and return or get only the good actual  
def get_fleet_vehicule_assignation(driver_ids):
    
    var= driver_ids
    count= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log', 'search_count', [[['driver_id','=', var]]] )
    
    if count==1:
        resul= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log', 
        'search_read', [[['driver_id','=', var]]],  {'fields': ['vehicle_id', 'driver_id', 'date_start', 'date_end', '__last_update']} )
        return resul[0]['vehicle_id']

    elif count > 1:
        resul= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log',
        'search_read', [[['driver_id','=', var]]],  {'fields': ['vehicle_id', 'driver_id', 'date_start', 'date_end', '__last_update' ]} )
        id_vehicule_actual= resul[0]['vehicle_id']
        end_date_vehic_actual= resul[0]['date_end']
        id_vehicule_prec= resul[1]['vehicle_id']


        print("datetime.today(): ", datetime.today())

        #Check here if the enddate and start from alpha.taxis

        end_date_vehic_actual= getting_alpha_end_dates_actual(driver_ids)
        print("end_date_vehic_actual: ", end_date_vehic_actual)


        if end_date_vehic_actual is False or datetime.strptime(end_date_vehic_actual, "%Y-%m-%d %H:%M:%S") > datetime.today() :
            #print ("end_date_vehic_actual: ", datetime.strptime(end_date_vehic_actual, "%Y-%m-%d"))

            return id_vehicule_actual
        
        else:
            return id_vehicule_prec
    else:
        return False

def getting_vehicules_aux(id_vehic):
    return models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle', 'search_read', 
    [[('id','=', id_vehic)]], {'fields': ['name', 'driver_id','license_plate', 'brand_id', 
    'model_id', 'seats' , 'doors', 'transmission', 'fuel_type', 'color', 'co2']})


def getting_vehicules_datas():

    drivers_ids=get_alpha_taxis_with_ids()

    print("Len: ", len(drivers_ids))
    
    final_result=[]
    half_flow_odoo_topivotdb.purges_pivotdb_purge("vehicules")

    for driver_id in drivers_ids:
        id_vehic= get_fleet_vehicule_assignation(driver_id)
        print("id_vehic: ", id_vehic)
        if id_vehic is not False:
            temp_result= getting_vehicules_aux(id_vehic[0])
            vehicules_datas=  temp_result[0]
            print("Eso es mis datas: ", vehicules_datas)

            half_flow_odoo_topivotdb.full_half_flow_Vehicules_to_pivotdb(vehicules_datas)
            final_result.append(vehicules_datas)
        else:
            pass
    return final_result

if __name__ == "__main__":    
    result= getting_vehicules_datas()
    '''with open("Full_Vehicules_extractions" + "_datas" + ".json", "w") as outfile:
                outfile.write(json.dumps(result, indent=4))'''

