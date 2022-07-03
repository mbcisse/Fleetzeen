from config import config
import psycopg2
from datetime import date

from datetime import datetime

def purges_pivotdb_purge(table_name):
    conn = None
    try:

        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
        
        postgres_purge_query= "DELETE FROM " + table_name
        cur = conn.cursor()  

        try:
            cur.execute(postgres_purge_query)
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here: postgres_purge_query")
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

def full_half_flow_company_to_pivotdb(id, display_name, subscriber_code_int, subscriber_out, client_id):
    conn = None
    try:

        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        print('Connected to the PostgreSQL database...')

        cur = conn.cursor()  
        #postgres_purge_query= "DELETE FROM company"

        postgres_insert_query= """INSERT INTO company(id_company, nom, date_entre, date_sortie, cmp_odoo_to_pivotdb_input_date, 
					              cmp_odoo_to_pivotdb_lastupdate, cmp_odoo_to_pivotdb_sync_status, 
					              cmp_odoo_to_pivotdb_sync_error_message, cmp_pivotdb_to_fleet_sync_date,
					              cmp_pivotdb_to_fleet_sync_status, cmp_pivotdb_to_fleet_sync_error_message, client_id)
					              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        
        now =  datetime.now()
        cmp_odoo_to_pivotdb_input_date=  now.strftime("%Y-%m-%d_%H:%M:%S")
        cmp_odoo_to_pivotdb_lastupdate= now.strftime("%Y-%m-%d_%H:%M:%S")
        cmp_pivotdb_to_fleet_sync_date = now.strftime("%Y-%m-%d_%H:%M:%S")

        cmp_pivotdb_to_fleet_sync_status="no_Sync_ToFleet_yet"
        cmp_odoo_to_pivotdb_sync_error_message="No error"
        cmp_pivotdb_to_fleet_sync_error_message="Not sent yet"
        cmp_odoo_to_pivotdb_sync_status="OK"

        record_to_insert = (str(id), str(display_name), str(subscriber_code_int), str(subscriber_out), str(cmp_odoo_to_pivotdb_input_date), str(cmp_odoo_to_pivotdb_lastupdate), str(cmp_odoo_to_pivotdb_sync_status), str(cmp_odoo_to_pivotdb_sync_error_message), str(cmp_pivotdb_to_fleet_sync_date), str(cmp_pivotdb_to_fleet_sync_status), str(cmp_pivotdb_to_fleet_sync_error_message), str(client_id))

        print("record_to_insert is: ", record_to_insert)
                
        try:
            
            cur.execute(postgres_insert_query, record_to_insert)
            conn.commit()
            count = cur.rowcount
            #print(count, "Record inserted successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here: postgres_insert_query")
        
        
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')



def full_half_flow_contracts_to_pivotdb(id, subscriber_code_str, ref, display_name, company_group_id, subscriber_in, subscriber_out, street,city, zip, country_id):
    conn = None
    try:

        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        print('Connected to the PostgreSQL database...')

        cur = conn.cursor()  
        #postgres_purge_query= "DELETE FROM company"

        postgres_insert_query= """INSERT INTO contract(id_contract, code, ref, name, company_id, date_entre, date_sortie, adress, 
                                        cr_odoo_to_pivotdb_input_date, cr_odoo_to_pivotdb_last_update, cr_odoo_to_pivotdb_sync_error_message,
                                        cr_odoo_to_pivotdb_sync_status, cr_pivotdb_to_fleet_sync_date,
                                        cr_pivotdb_to_fleet_sync_status, cr_pivotdb_to_fleet_sync_error_message)
					              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s) """
        
        now =  datetime.now()
        cmp_odoo_to_pivotdb_input_date=  now.strftime("%Y-%m-%d_%H:%M:%S")
        cmp_odoo_to_pivotdb_lastupdate= now.strftime("%Y-%m-%d_%H:%M:%S")
        cmp_pivotdb_to_fleet_sync_date = now.strftime("%Y-%m-%d_%H:%M:%S")

        cmp_pivotdb_to_fleet_sync_status="no_Sync_ToFleet_yet"
        cmp_odoo_to_pivotdb_sync_error_message="No error"
        cmp_pivotdb_to_fleet_sync_error_message="Not sent yet"
        cmp_odoo_to_pivotdb_sync_status="OK"

        print("the adress is: ", street,city, zip, country_id)
        if street==False:
            street=""
        if city==False:
            city=""
        if zip==False:
            zip=""
        if country_id==False:
            country_id=[1, "No adresse provided"]
        
        if company_group_id== False:
            company_group_id=["dummy_company", "No parent_id"]

        adress= street +" " + " "+ city + " " +zip+ " "+country_id[1]
        
        record_to_insert = (str(id), str(subscriber_code_str), str(ref), str(display_name), str(company_group_id[0]), str(subscriber_in), str(subscriber_out), str(adress),str(cmp_odoo_to_pivotdb_input_date), str(cmp_odoo_to_pivotdb_lastupdate), str(cmp_odoo_to_pivotdb_sync_error_message),str(cmp_odoo_to_pivotdb_sync_status), str(cmp_pivotdb_to_fleet_sync_date), str(cmp_pivotdb_to_fleet_sync_status), str(cmp_pivotdb_to_fleet_sync_error_message))

        print("record_to_insert is: ", record_to_insert)
                
        try:
            
            cur.execute(postgres_insert_query, record_to_insert)
            conn.commit()
            count = cur.rowcount
            #print(count, "Record inserted successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here: postgres_insert_query")
     
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')


def full_half_flow_services_to_pivotdb(id, subscriber_code_str, name, company_id, parent_id, subscriber_in, subscriber_out, mobile, email, street, city, zip, country_id, comment_for_operator, comment_for_driver):
    conn = None
    try:

        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        print('Connected to the PostgreSQL database...')

        cur = conn.cursor()  
        #postgres_purge_query= "DELETE FROM company"

        postgres_insert_query= """INSERT INTO service(id_service, code_service, service_name, company_id, id_contract_parentid, date_entre, date_sortie, 
                                        telephone, email, adress, comment_operateur, comment_drivers, sr_odoo_to_pivotdb_input_date, 
                                        sr_odoo_to_pivotdb_last_update, sr_odoo_to_pivotdb_sync_error_message,
                                        sr_odoo_to_pivotdb_sync_status, sr_pivotdb_to_fleet_sync_date,
                                        sr_pivotdb_to_fleet_sync_status, sr_pivotdb_to_fleet_sync_error_message)
					              VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s) """
        
        now =  datetime.now()
        cmp_odoo_to_pivotdb_input_date=  now.strftime("%Y-%m-%d_%H:%M:%S")
        cmp_odoo_to_pivotdb_lastupdate= now.strftime("%Y-%m-%d_%H:%M:%S")
        cmp_pivotdb_to_fleet_sync_date = now.strftime("%Y-%m-%d_%H:%M:%S")

        cmp_pivotdb_to_fleet_sync_status="no_Sync_ToFleet_yet"
        cmp_odoo_to_pivotdb_sync_error_message="No error"
        cmp_pivotdb_to_fleet_sync_error_message="Not sent yet"
        cmp_odoo_to_pivotdb_sync_status="OK"

        print("the adress is: ", street,city, zip, country_id)
        if street==False:
            street=""
        if city==False:
            city=""
        if zip==False:
            zip=""
        if country_id==False:
            country_id=[1, "No adresse provided"]
        if parent_id== False:
            parent_id=[1, "No parent_id"]
        

        adress= street +" " + " "+ city + " " +zip+ " "+country_id[1]
        
        record_to_insert = (str(id), str(subscriber_code_str), str(name), str(company_id), str(parent_id[1]), str(subscriber_in), str(subscriber_out), 
        str(mobile),str(email) ,str(adress), str(comment_for_operator), str(comment_for_driver),str(cmp_odoo_to_pivotdb_input_date), str(cmp_odoo_to_pivotdb_lastupdate), str(cmp_odoo_to_pivotdb_sync_error_message),str(cmp_odoo_to_pivotdb_sync_status), str(cmp_pivotdb_to_fleet_sync_date), str(cmp_pivotdb_to_fleet_sync_status), str(cmp_pivotdb_to_fleet_sync_error_message))

        print("record_to_insert is: ", record_to_insert)
                
        try:
            
            cur.execute(postgres_insert_query, record_to_insert)
            conn.commit()
            count = cur.rowcount
            #print(count, "Record inserted successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here: postgres_insert_query")
     
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

def services_datas_pivotdb_to_fleet_update_status(service_id, pivotdb_to_fleet_sync_status, pivotdb_to_fleet_sync_date, pivotdb_to_fleet_sync_error_message):
    conn = None
    try:
        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        cur = conn.cursor()

        sql_update_query = """Update service set sr_pivotdb_to_fleet_sync_status = %s, sr_pivotdb_to_fleet_sync_date =  %s, 
                              sr_pivotdb_to_fleet_sync_error_message  = %s where id_service = %s """
        
        try:
            cur.execute(sql_update_query, (str(pivotdb_to_fleet_sync_status), str(pivotdb_to_fleet_sync_date), str(pivotdb_to_fleet_sync_error_message), str(service_id)))
            conn.commit()
        
        except (Exception, psycopg2.DatabaseError) as error:
            print("Taliko:  Error, DJO IL YA ERROR: ", error)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')
                        

def abonne_datas_pivotdb_to_fleet_update_status(companycontract_id, pivotdb_to_fleet_sync_status, pivotdb_to_fleet_sync_date, pivotdb_to_fleet_sync_error_message):

    conn = None
    try:
        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        cur = conn.cursor()

        sql_update_query = """Update contract set cr_pivotdb_to_fleet_sync_status = %s, cr_pivotdb_to_fleet_sync_date =  %s, 
                              cr_pivotdb_to_fleet_sync_error_message  = %s where id_contract = %s """
        
        try:
            cur.execute(sql_update_query, (str(pivotdb_to_fleet_sync_status), str(pivotdb_to_fleet_sync_date), str(pivotdb_to_fleet_sync_error_message), str(companycontract_id)))
            conn.commit()
        
        except (Exception, psycopg2.DatabaseError) as error:
            print("Taliko:  Error, DJO IL YA ERROR: ", error)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')





def company_datas_pivotdb_to_fleet_update_status(id_company, pivotdb_to_fleet_sync_status, pivotdb_to_fleet_sync_date,pivotdb_to_fleet_sync_error_message):
    conn = None
    try:
        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        cur = conn.cursor()

        sql_update_query = """Update company set cmp_pivotdb_to_fleet_sync_status = %s, cmp_pivotdb_to_fleet_sync_date =  %s, 
                              cmp_pivotdb_to_fleet_sync_error_message  = %s where id_company = %s """
        
        try:
            cur.execute(sql_update_query, (str(pivotdb_to_fleet_sync_status), str(pivotdb_to_fleet_sync_date), str(pivotdb_to_fleet_sync_error_message), str(id_company)))
            conn.commit()
        
        except (Exception, psycopg2.DatabaseError) as error:
            print("Taliko:  Error, DJO IL YA ERROR: ", error)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')



def veh_drivers_datas_pivotdb_to_fleet_update_status(driver_id, pivotdb_to_fleet_sync_status,  pivotdb_to_fleet_sync_date, pivotdb_to_fleet_sync_error_message ):
    conn = None
    try:
        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        cur = conn.cursor()

        sql_update_query = """Update vehicules set veh_pivotdb_to_fleet_sync_status = %s, veh_pivotdb_to_fleet_sync_date =  %s, 
                              veh_pivotdb_to_fleet_sync_error_message  = %s where user_id = %s """
        
        try:
            cur.execute(sql_update_query, (str(pivotdb_to_fleet_sync_status), str(pivotdb_to_fleet_sync_date), str(pivotdb_to_fleet_sync_error_message), int(driver_id)))
            conn.commit()
        
        except (Exception, psycopg2.DatabaseError) as error:
            print("Taliko:  Error, DJO IL YA ERROR: ", error)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')
    

def drivers_datas_pivotdb_to_fleet_update_status(driver_id, pivotdb_to_fleet_sync_status,  pivotdb_to_fleet_sync_date, pivotdb_to_fleet_sync_error_message ):
    conn = None
    try:
        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        cur = conn.cursor()

        sql_update_query = """Update drivers_vehicules set pivotdb_to_fleet_sync_status = %s, pivotdb_to_fleet_sync_date =  %s, 
                              pivotdb_to_fleet_sync_error_message  = %s where dh_id = %s
                           """
        
        try:
            cur.execute(sql_update_query, (str(pivotdb_to_fleet_sync_status), str(pivotdb_to_fleet_sync_date), str(pivotdb_to_fleet_sync_error_message), int(driver_id)))
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("DJO IL YA ERROR: ", error)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

def full_half_flow_VehicDrivers_to_pivotdb(id, radio_code, alpha_taxis_ids, start_date_alpha_taxis, end_date_alpha_taxis, 
                                            status, driver_last_name, driver_first_name, email, mobile, adresse, group_client_id, 
                                            display_name, id_vehicule_prec, start_date_vehic_prec, end_date_vehic_prec, 
                                            id_vehicule_actual, start_date_vehic_actual, end_date_vehic_actual, 
                                            lastupdatedate_res_partner, last_update_vehicule_prec, last_update_vehicule_actual):
    
    '''
    print("Entrando en las base de datos:", id, radio_code, alpha_taxis_ids, start_date_alpha_taxis, end_date_alpha_taxis, 
                                            status, driver_last_name, driver_first_name, email, mobile, adresse, group_client_id, 
                                            display_name, id_vehicule_prec, start_date_vehic_prec, end_date_vehic_prec, 
                                            id_vehicule_actual, start_date_vehic_actual, end_date_vehic_actual, 
                                            lastupdatedate_res_partner, last_update_vehicule_prec, last_update_vehicule_actual)
    '''
    
    conn = None
    try:

        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        print('Connected to the PostgreSQL database...')

        cur = conn.cursor()  
        

        postgres_insert_query= """INSERT INTO drivers_vehicules(dh_id, radio_code, alpha_taxis_ids, start_alpha_code_radio, end_alpha_code_radio, status_alpha_taxis,
            driver_last_name, driver_first_name, email, mobile, adresse, ident_adherent, display_name,
            id_vehicule_precedent, start_vehic_fleet_prec, end_vehic_fleet_prec, id_vehiclule_actuel, start_vehic_fleet_actuel,
            end_vehic_fleet_actuel, odoo_to_pivotdb_input_date, odoo_to_pivotdb_last_update, pivotdb_to_fleet_sync_date, 
            pivotdb_to_fleet_sync_status, pivotdb_to_fleet_sync_error_message, odoo_to_pivotdb_sync_status, 
            odoo_to_pivotdb_sync_error_message, last_update_res_partner, last_update_vehicule_prec, last_update_vehicule_actual)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        now =  datetime.now()
        odoo_to_pivotdb_input_date=  now.strftime("%Y-%m-%d_%H:%M:%S")
        odoo_to_pivotdb_last_update= now.strftime("%Y-%m-%d_%H:%M:%S")
        pivotdb_to_fleet_sync_date = now.strftime("%Y-%m-%d_%H:%M:%S")

        pivotdb_to_fleet_sync_status="no_Sync_ToFleet_yet"
        odoo_to_pivotdb_sync_error_message1="No error"
        pivotdb_to_fleet_sync_error_message1="Not sent yet"
        odoo_to_pivotdb_sync_status="OK"

        record_to_insert = (id, radio_code, alpha_taxis_ids, start_date_alpha_taxis, end_date_alpha_taxis, status, driver_last_name, 
              driver_first_name, email, mobile, adresse, group_client_id, display_name, id_vehicule_prec, start_date_vehic_prec, 
              end_date_vehic_prec, id_vehicule_actual, start_date_vehic_actual, end_date_vehic_actual, odoo_to_pivotdb_input_date, 
              odoo_to_pivotdb_last_update, pivotdb_to_fleet_sync_date, pivotdb_to_fleet_sync_status, pivotdb_to_fleet_sync_error_message1, 
              odoo_to_pivotdb_sync_status, odoo_to_pivotdb_sync_error_message1, lastupdatedate_res_partner, last_update_vehicule_prec, last_update_vehicule_actual)

        #print("record_to_insert is: ", record_to_insert)
        
        try:
            cur.execute(postgres_insert_query, record_to_insert)
            conn.commit()
            count = cur.rowcount
            #print(count, "Record inserted successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here")
        
        
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')
    
    

def full_half_flow_Vehicules_to_pivotdb(vehicules_datas):
    
    conn = None
    try:

        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        print('Connected to the PostgreSQL database...')

        cur = conn.cursor()  
        postgres_insert_query=  """INSERT INTO vehicules(user_id, id_vehicule, plaque, marque, modele, nbre_places , nbre_portes, 
                                    transmission, energie, couleur,co2, veh_odoo_to_pivotdb_input_date, veh_odoo_to_pivotdb_lastupdate, 
                                    veh_pivotdb_to_fleet_sync_date, veh_odoo_to_pivotdb_sync_status, veh_odoo_to_pivotdb_sync_error_message, 
                                    veh_pivotdb_to_fleet_sync_status, veh_pivotdb_to_fleet_sync_error_message)
                                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                                """
        now =  datetime.now()
        veh_odoo_to_pivotdb_input_date=  now.strftime("%Y-%m-%d_%H:%M:%S")
        veh_odoo_to_pivotdb_lastupdate= now.strftime("%Y-%m-%d_%H:%M:%S")
        veh_pivotdb_to_fleet_sync_date = now.strftime("%Y-%m-%d_%H:%M:%S")

        veh_pivotdb_to_fleet_sync_status="no_Sync_ToFleet_yet"
        veh_odoo_to_pivotdb_sync_error_message="No error"
        veh_pivotdb_to_fleet_sync_error_message="Not sent yet"
        veh_odoo_to_pivotdb_sync_status="OK"

        if vehicules_datas["fuel_type"] is False:
            fuel_type= "False"
        else:
            fuel_type= vehicules_datas["fuel_type"][1]
      
        if vehicules_datas["name"] is False:
            vehicules_name="False"
        else:
            vehicules_name=vehicules_datas["name"].split("/")[0]
         
        if vehicules_datas["model_id"] is False:
            vehicules_model= "False"
        else:
            vehicules_model= vehicules_datas["model_id"][1].split("/")[1]


        record_to_insert=(vehicules_datas["driver_id"][0], vehicules_datas["id"], vehicules_datas["license_plate"],
        vehicules_name, vehicules_model, vehicules_datas["seats"], 
        vehicules_datas["doors"],  vehicules_datas["transmission"], fuel_type, vehicules_datas["color"], 
        vehicules_datas["co2"],veh_odoo_to_pivotdb_input_date, veh_odoo_to_pivotdb_lastupdate, veh_pivotdb_to_fleet_sync_date, 
        veh_odoo_to_pivotdb_sync_status, veh_odoo_to_pivotdb_sync_error_message, veh_pivotdb_to_fleet_sync_status,
        veh_pivotdb_to_fleet_sync_error_message)

        
        try:
            cur.execute(postgres_insert_query, record_to_insert)
            conn.commit()
            count = cur.rowcount
            #print(count, "Record inserted successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here")


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

def getting_db_x_studio_x_lastupdatedate__flow_from_pivotdb(driver_id):
    
    conn = None
    try:

        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        #print('Connected to the PostgreSQL database...')

        cur = conn.cursor()  
        postgres_select_query= "select last_update_res_partner from drivers_vehicules where dh_id = %s"

            
        try:
            print("db_last_update_res")
            cur.execute(postgres_select_query, (driver_id,))
            db_last_update_res= cur.fetchall()
            #print(db_last_update_res)
            for db_last in db_last_update_res:
                return db_last[0]
				
               

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here")
        
        
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()

def getting_actual_db_last_update_from_pivotdb(driver_id):
    conn = None
    try:

        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        #print('Connected to the PostgreSQL database...')

        cur = conn.cursor()  
        postgres_select_query= "select last_update_vehicule_actual from drivers_vehicules where dh_id = %s"

            
        try:
            print("db_last_update_res")
            cur.execute(postgres_select_query, (driver_id,))
            db_last_update_res= cur.fetchall()
            #print(db_last_update_res)
            for db_last in db_last_update_res:
                return db_last[0]
				
               

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here")
        
        
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
def getting_prec_db_last_update_from_pivotdb(driver_id):
    conn = None
    try:
        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        cur = conn.cursor()  
        postgres_select_query= "select last_update_vehicule_prec from drivers_vehicules where dh_id = %s"

        try:
            print("db_last_update_res")
            cur.execute(postgres_select_query, (driver_id,))
            db_last_update_res= cur.fetchall()
            #print(db_last_update_res)
            for db_last in db_last_update_res:
                return db_last[0]

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()


def getting_db_last_update_from_pivotdb(driver_id):
    
    conn = None
    try:

        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        #print('Connected to the PostgreSQL database...')

        cur = conn.cursor()  
        postgres_select_query= """SELECT CASE WHEN end_vehic_fleet_prec='false' THEN 'last_update_vehicule_actual' 
                                  WHEN end_vehic_fleet_prec <> 'false' AND TO_DATE(end_vehic_fleet_prec,'YYYY-MM-DD') > now() 
		   				          THEN 'last_update_vehicule_actual' ELSE  'last_update_vehicule_prec' END last_update 
                                  FROM drivers_vehicules WHERE dh_id = %s"""           
        try:
            print("db_last_update_res")
            cur.execute(postgres_select_query, (driver_id,))
            db_last_update_res= cur.fetchall()
            #print(db_last_update_res)
            for db_last in db_last_update_res:
                return db_last[0]
				
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here")  
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()



if __name__ == '__main__':
   print(getting_db_last_update_from_pivotdb(11968))
 
