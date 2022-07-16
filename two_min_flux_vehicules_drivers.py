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

def get_last_update_date_alpha_taxis_ids(alpha_taxis_ids):
    result=[]
    for var in alpha_taxis_ids:
        
        odoo_last_update  = var["__last_update"]
        db_last_update_alpha= half_flow_odoo_topivotdb.getting_alpha_taxis_db_last_update_from_pivotdb(var["id"])
       
        if odoo_last_update is not False and odoo_last_update != 'false':
            if db_last_update_alpha is not None and db_last_update_alpha !='false':
                db_last_update_alpha= datetime.strptime(db_last_update_alpha, "%Y-%m-%d %H:%M:%S")
                odoo_last_update= datetime.strptime(odoo_last_update, "%Y-%m-%d %H:%M:%S") 
                if odoo_last_update > db_last_update_alpha:
                    return var
                else:
                    return []
            elif db_last_update_alpha =='false' or db_last_update_alpha=='False':
                return var
            else:
                return []
        else:
            return []
    

def get_alpha_taxis_with_ids(db_id):
    today = datetime.today() 
   #today_1  = datetime.strptime('2022-07-05', "%Y-%m-%d %H:%M:%S")
    #today_1= "2022-07-05 01:34:00"

    alpha_taxis_ids= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'alpha.taxis', 'search_read',
     [[('radio_contract', 'not like', 'S%'),('id', '=', db_id), ('start_date', '!=', False),'|',('end_date', '=', False),
     ('end_date', '>=', today)]], {'fields': ['driver_id', 'start_date','end_date', 'status','__last_update']})
    
    
    '''alpha_taxis_ids= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'alpha.taxis', 'search_read',
     [[('__last_update','<=', '2022-04-26 01:30:33')]], {'fields': ['__last_update']})
    '''

    return get_last_update_date_alpha_taxis_ids(alpha_taxis_ids)
    #return get_drivers_ids(alpha_taxis_ids)
    #return alpha_taxis_ids

def get_fleet_vehicule_assignation_lastupdate():
    pass

def get_fleet_vehicule_assignation(driver_ids):

    db_last_update= half_flow_odoo_topivotdb.getting_db_last_update_from_pivotdb(driver_ids)
    veh_to_take=""
    if db_last_update=="last_update_vehicule_actual":
        veh_to_take="actuel"
        db_last_update= half_flow_odoo_topivotdb.getting_actual_db_last_update_from_pivotdb(driver_ids)
    else:
       veh_to_take="prec"
       db_last_update= half_flow_odoo_topivotdb.getting_prec_db_last_update_from_pivotdb(driver_ids)

    var= driver_ids
    count= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log', 'search_count', [[('driver_id','=', var)]])

    if count==1:
        resul= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'fleet.vehicle.assignation.log', 
        'search_read', [[['driver_id','=', var]]],  {'fields': ['vehicle_id', 'driver_id', 'date_start', 'date_end', '__last_update']} )
        id_vehicule_prec=id_vehicule_actual= resul[0]['vehicle_id']
        start_date_vehic_prec=start_date_vehic_actual= resul[0]['date_start']
        end_date_vehic_prec= end_date_vehic_actual= resul[0]['date_end']
        last_update= resul[0]['__last_update']        
        odoo_last_update= resul[0]["__last_update"]
        if odoo_last_update  != 'false':
            if db_last_update != 'false':
                db_last_update  = datetime.strptime(db_last_update, "%Y-%m-%d %H:%M:%S")
                odoo_last_update= datetime.strptime(odoo_last_update, "%Y-%m-%d %H:%M:%S")                        
                if  odoo_last_update > db_last_update:
                    return  id_vehicule_prec[0], id_vehicule_actual[0], start_date_vehic_prec, start_date_vehic_actual, end_date_vehic_prec, end_date_vehic_actual, last_update,last_update
                else:
                    return []
            elif db_last_update == 'false':
                return  id_vehicule_prec[0], id_vehicule_actual[0], start_date_vehic_prec, start_date_vehic_actual, end_date_vehic_prec, end_date_vehic_actual, last_update,last_update
        elif odoo_last_update=='false':
            return[]
        else:
            return[]
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

        odoo_last_update= resul[0]["__last_update"]
        odoo_last_update_prec= resul[1]["__last_update"]
        
        if veh_to_take=='actuel':        
            if odoo_last_update  != 'false' and odoo_last_update != False:
                if db_last_update != 'false':
                    db_last_update  = datetime.strptime(db_last_update, "%Y-%m-%d %H:%M:%S")
                    odoo_last_update= datetime.strptime(odoo_last_update, "%Y-%m-%d %H:%M:%S")
                    if  odoo_last_update > db_last_update:
                        return id_vehicule_prec[0], id_vehicule_actual[0], start_date_vehic_prec, start_date_vehic_actual, end_date_vehic_prec, end_date_vehic_actual,last_update_prec, last_update_prec
                    else:
                        return []

                elif db_last_update == 'false':
                    return id_vehicule_prec[0], id_vehicule_actual[0], start_date_vehic_prec, start_date_vehic_actual, end_date_vehic_prec, end_date_vehic_actual,last_update_prec, last_update_prec
            elif odoo_last_update=='false' or odoo_last_update is False :
                return[]   
        else:
            odoo_last_update= odoo_last_update_prec
            if odoo_last_update  != 'false':
                if db_last_update != 'false':
                    db_last_update  = datetime.strptime(db_last_update, "%Y-%m-%d %H:%M:%S")
                    odoo_last_update= datetime.strptime(odoo_last_update, "%Y-%m-%d %H:%M:%S")
                    if  odoo_last_update > db_last_update:
                        return id_vehicule_prec[0], id_vehicule_actual[0], start_date_vehic_prec, start_date_vehic_actual, end_date_vehic_prec, end_date_vehic_actual,last_update_prec, last_update_prec
                    else:
                        return[]
                elif db_last_update == 'false':
                    return id_vehicule_prec[0], id_vehicule_actual[0], start_date_vehic_prec, start_date_vehic_actual, end_date_vehic_prec, end_date_vehic_actual,last_update_prec, last_update_prec
            elif odoo_last_update=='false' or odoo_last_update is False :
                return[]      
    
    

def get_alpha_taxis_datas(driver_ids):

    db_last_update= half_flow_odoo_topivotdb.getting_alpha_taxis_db_last_update_from_pivotdb(driver_ids)
    print("BEFORE db_last_update get_alpha_taxis_datas: ",   db_last_update)
    if db_last_update !=None:
        db_last_update= datetime.strptime(db_last_update, "%Y-%m-%d %H:%M:%S")
        
        alpha_taxis_datas= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'alpha.taxis', 'search_read',
     [[('driver_id','=', driver_ids)]], {'fields': ['driver_id', 'radio_code', 'start_date','end_date', 'status', '__last_update']})
        
        odoo_last_update= alpha_taxis_datas[0]["__last_update"]
        if odoo_last_update!='false':
            odoo_last_update= datetime.strptime(odoo_last_update, "%Y-%m-%d %H:%M:%S")
            print("db_last_update get_alpha_taxis_datas: ",   db_last_update)
            print("odoo_last_update get_alpha_taxis_datas: ", odoo_last_update)
            if  odoo_last_update > db_last_update:
                print("Yes odoo_last_update: ", odoo_last_update)
                return alpha_taxis_datas 
            else:
                return[]
        else:
            return []

def get_res_partner_with_ids(driver_id):

    db_x_studio_x_lastupdatedate_flow= half_flow_odoo_topivotdb.getting_db_x_studio_x_lastupdatedate__flow_from_pivotdb(driver_id)
    drivers_datas= models.execute_kw(odoo_acces.db, uid, odoo_acces.password, 'res.partner', 'search_read',
        [[('is_driver', '=', True), ('id', '=', driver_id)]], 
        {'fields': ['radio_code', 'alpha_taxis_ids', 'driver_lastname', 'driver_firstname',
        'email','mobile', 'street','zip', 'city', 'ref', 'display_name', 'x_studio_x_lastupdatedate_flow']})
    
    odoo_last_update= drivers_datas[0]["x_studio_x_lastupdatedate_flow"]

    if odoo_last_update is not False and not None:
        
        if db_x_studio_x_lastupdatedate_flow != 'false':
            odoo_last_update= datetime.strptime(odoo_last_update, "%Y-%m-%d %H:%M:%S") 
            db_x_studio_x_lastupdatedate_flow= datetime.strptime(db_x_studio_x_lastupdatedate_flow, "%Y-%m-%d %H:%M:%S") 
            if  odoo_last_update > db_x_studio_x_lastupdatedate_flow:
                print("Yes odoo_last_update: ", odoo_last_update)
                return drivers_datas[0]
            else:
                return []
        elif db_x_studio_x_lastupdatedate_flow == 'false':
            print("Yes odoo_last_update: ", odoo_last_update)
            return drivers_datas[0]
        else:
            return []

    elif odoo_last_update == False or odoo_last_update is None:
        return []

    

def two_min_getting_drivers_vehicules_datas():

    drivers_ids=  half_flow_odoo_topivotdb.get_alpha_taxis_with_ids_from_pivotdb()
    for elem in drivers_ids:        
        print("elem[0]: ", elem[0])
        if get_alpha_taxis_with_ids(elem[0]) != [] and get_alpha_taxis_with_ids(elem[0]) is not None:
            datas_alpha_taxis=get_alpha_taxis_with_ids(elem[0])
            print("Got some updates to be done on datas_alpha_taxis: ", datas_alpha_taxis)
            start_date_alpha_taxis= datas_alpha_taxis['start_date']
            end_date_alpha_taxis= datas_alpha_taxis['end_date']
            status= datas_alpha_taxis['status']
            last_update_alpha= datas_alpha_taxis["__last_update"] 
            driver_id= datas_alpha_taxis['id']   
            half_flow_odoo_topivotdb.two_min_flux_drivers_alpha_taxis_datas_update(driver_id, start_date_alpha_taxis, 
            end_date_alpha_taxis, status, last_update_alpha) 
          
        if get_res_partner_with_ids(elem[0]) != [] and get_res_partner_with_ids(elem[0]) is not None:  
            print("Got some updates to be done on datas_res_partner")
            datas_res_partner = get_res_partner_with_ids(elem[0])
            driver_id= datas_res_partner['id']
            driver_last_name= datas_res_partner['driver_lastname']
            driver_first_name= datas_res_partner['driver_firstname']
            email= datas_res_partner['email']
            mobile= datas_res_partner['mobile']
            adresse= str(datas_res_partner['street']) + " " +  str(datas_res_partner['zip']) +  str(datas_res_partner['zip']) + " " + str(datas_res_partner['city'])
            group_client_id= datas_res_partner['ref']
            display_name= datas_res_partner['display_name']         
            radio_code= datas_res_partner['radio_code']
            alpha_taxis_ids= datas_res_partner['alpha_taxis_ids']
            lastupdatedate_res_partner= datas_res_partner['x_studio_x_lastupdatedate_flow']
            half_flow_odoo_topivotdb.two_min_flux_drivers_res_partner_datas_update( 
              driver_id, radio_code, alpha_taxis_ids,driver_last_name,  driver_first_name, email, mobile, adresse, 
              group_client_id, display_name, lastupdatedate_res_partner)

        if get_fleet_vehicule_assignation(elem[0]) !=[] and get_fleet_vehicule_assignation(elem[0]) is not None:
            print("Got some updates to be done on get_fleet_vehicule_assignation")
            datas_fleet_vehicule_assign= get_fleet_vehicule_assignation(elem[0])
            driver_id=elem[0]         
            id_vehicule_prec, id_vehicule_actual, start_date_vehic_prec, start_date_vehic_actual, end_date_vehic_prec, end_date_vehic_actual, last_update_vehicule_prec, last_update_vehicule_actual=datas_fleet_vehicule_assign
            half_flow_odoo_topivotdb.two_min_flux_vehicules_fleet_vehicule_assignation_drivers_datas_update( 
              driver_id, id_vehicule_prec, start_date_vehic_prec, end_date_vehic_prec, id_vehicule_actual, 
              start_date_vehic_actual, end_date_vehic_actual, last_update_vehicule_prec, last_update_vehicule_actual)
        else:
            print("No update performed at this time")
        
    
    
'''
    final_result=[]
  
    for driver_id in drivers_ids:
        print(driver_id)
        if len(get_res_partner_with_ids(driver_id)) > 1:
            
            datas_res_partner = get_res_partner_with_ids(driver_id)[0]
            print("datas_res_partner: ", datas_res_partner)
            driver_last_name= datas_res_partner['driver_lastname']
            driver_first_name= datas_res_partner['driver_firstname']
            email= datas_res_partner['email']
            mobile= datas_res_partner['mobile']
            adresse= str(datas_res_partner['street']) + " " +  str(datas_res_partner['zip']) +  str(datas_res_partner['zip']) + " " + str(datas_res_partner['city'])
            group_client_id= datas_res_partner['ref']
            display_name= datas_res_partner['display_name']
            id= datas_res_partner['id']
            radio_code= datas_res_partner['radio_code']
            alpha_taxis_ids= datas_res_partner['alpha_taxis_ids']
            lastupdatedate_res_partner= datas_res_partner['x_studio_x_lastupdatedate_flow']
        
        else:
            print("EH TALA NE KA TIE")

            half_flow_odoo_topivotdb.two_min_flux_drivers_res_partner_datas_update( 
              driver_id, radio_code, alpha_taxis_ids,driver_last_name,  driver_first_name, email, mobile, adresse, 
              group_client_id, display_name, lastupdatedate_res_partner)

        if get_alpha_taxis_datas(driver_id) is not None:
            if  len(get_alpha_taxis_datas(driver_id)) > 1:
                datas_alpha_taxis = get_alpha_taxis_datas(driver_id)[0]
                print("get_alpha_taxis_datas: ", datas_alpha_taxis )
                start_date_alpha_taxis= datas_alpha_taxis['start_date']
                end_date_alpha_taxis= datas_alpha_taxis['end_date']
                status= datas_alpha_taxis['status']
                last_update_alpha= datas_alpha_taxis["__last_update"]   

                half_flow_odoo_topivotdb.two_min_flux_drivers_alpha_taxis_datas_update( 
              driver_id, start_date_alpha_taxis, end_date_alpha_taxis, status, last_update_alpha)         
        
        if get_fleet_vehicule_assignation(driver_id) is not False and get_fleet_vehicule_assignation(driver_id) != [] and get_fleet_vehicule_assignation(driver_id) is not None:
            
            datas_fleet_vehicule_assign= get_fleet_vehicule_assignation(driver_id)
            print("datas_fleet_vehicule_assign: ", datas_fleet_vehicule_assign)
            
            id_vehicule_prec, id_vehicule_actual, start_date_vehic_prec, start_date_vehic_actual, end_date_vehic_prec, end_date_vehic_actual, last_update_vehicule_prec, last_update_vehicule_actual=datas_fleet_vehicule_assign
            
            half_flow_odoo_topivotdb.two_min_flux_vehicules_fleet_vehicule_assignation_drivers_datas_update( 
              driver_id, id_vehicule_prec, start_date_vehic_prec, end_date_vehic_prec, id_vehicule_actual, 
              start_date_vehic_actual, end_date_vehic_actual, last_update_vehicule_prec, last_update_vehicule_actual)

        else:
            pass
    
    return final_result
'''
if __name__ == "__main__":    
    result= two_min_getting_drivers_vehicules_datas()
    '''with open("first_extractions" + "_datas" + ".json", "w") as outfile:
                outfile.write(json.dumps(result, indent=4))
'''