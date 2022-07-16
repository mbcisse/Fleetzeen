from unicodedata import name
import psycopg2
from datetime import date
import fleet_api
import half_flow_odoo_topivotdb
from datetime import datetime


def getting_drivers_datas_from_pivotdb_to_fleet():
    
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
        postgres_select_query= """      select dh_id, radio_code, driver_last_name, driver_first_name, email,
                                         mobile, adresse, ident_adherent, display_name
                                         from drivers_vehicules
  
                               """


        drivers_datas= dict()
               
        try:
            cur.execute(postgres_select_query)
            drivers_records = cur.fetchall()

            for drivers in drivers_records:
                drivers_datas["user_id"], drivers_datas["user_client_id"], drivers_datas["last_name"], drivers_datas["first_name"], drivers_datas["email"], drivers_datas["gsm"], drivers_datas["address"], drivers_datas["group_client_id"], drivers_datas["name"]=drivers
                #print(drivers_datas["user_id"], drivers_datas["user_client_id"], drivers_datas["last_name"], drivers_datas["first_name"], drivers_datas["email"], drivers_datas["gsm"], drivers_datas["address"], drivers_datas["group_client_id"], drivers_datas["name"])
                #Call fleet api to send this drivers datas to fleet
                
                status= fleet_api.new_drivers_to_fleet(drivers_datas)
                if status=="OK":
                    pivotdb_to_fleet_sync_status="OK"
                    now =  datetime.now()
                    pivotdb_to_fleet_sync_date = now.strftime("%Y-%m-%d %H:%M:%S")
                    pivotdb_to_fleet_sync_error_message="No error"

                    half_flow_odoo_topivotdb.drivers_datas_pivotdb_to_fleet_update_status(drivers_datas["user_id"], pivotdb_to_fleet_sync_status, pivotdb_to_fleet_sync_date,pivotdb_to_fleet_sync_error_message)

                else:
                    pivotdb_to_fleet_sync_status="KO"
                    pivotdb_to_fleet_sync_date=  date.today()
                    pivotdb_to_fleet_sync_error_message= status

                    half_flow_odoo_topivotdb.drivers_datas_pivotdb_to_fleet_update_status(drivers_datas["user_id"], pivotdb_to_fleet_sync_status, pivotdb_to_fleet_sync_date,pivotdb_to_fleet_sync_error_message)
                    #print("KO")     

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here")
      
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()


def getting_drivers_vehiculedatas_from_pivotdb_to_fleet():
    
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
        postgres_select_query= """select dvh.dh_id, dvh.radio_code, dvh.driver_last_name, dvh.driver_first_name, 
                                    dvh.email, dvh.mobile, dvh.adresse, dvh.ident_adherent, dvh.display_name, 
                                    veh.plaque, veh.marque, veh.modele, veh.couleur, veh.co2 from drivers_vehicules as dvh
                                    inner join vehicules as veh on  dvh.dh_id =veh.user_id"""

        drivers_datas= dict()
        vehicule_datas=dict()
        try:
            cur.execute(postgres_select_query)
            drivers_records = cur.fetchall()
            #print(drivers_records)
            
            for drivers in drivers_records:
                drivers_datas["user_id"], drivers_datas["user_client_id"], drivers_datas["last_name"], drivers_datas["first_name"], drivers_datas["email"], drivers_datas["gsm"], drivers_datas["address"], drivers_datas["group_client_id"], drivers_datas["name"], vehicule_datas["plaque"], vehicule_datas["brand"], vehicule_datas["model"], vehicule_datas["color"], vehicule_datas["co2"]=drivers

                drivers_datas["vehicle"]=vehicule_datas
                #print(drivers_datas["user_id"], drivers_datas["user_client_id"], drivers_datas["last_name"], drivers_datas["first_name"], drivers_datas["email"], drivers_datas["gsm"], drivers_datas["address"], drivers_datas["group_client_id"], drivers_datas["name"])
                #Call fleet api to send this drivers datas to fleet
                print("The drivers datas is: ", drivers_datas)
                status= fleet_api.new_vehicule_to_fleet(drivers_datas)
                if status=="OK":
                    pivotdb_to_fleet_sync_status="OK"
                    now =  datetime.now()
                    pivotdb_to_fleet_sync_date = now.strftime("%Y-%m-%d %H:%M:%S")
                    pivotdb_to_fleet_sync_error_message="No error"

                    half_flow_odoo_topivotdb.veh_drivers_datas_pivotdb_to_fleet_update_status(drivers_datas["user_id"], pivotdb_to_fleet_sync_status, pivotdb_to_fleet_sync_date,pivotdb_to_fleet_sync_error_message)

                else:
                    pivotdb_to_fleet_sync_status="KO"
                    pivotdb_to_fleet_sync_date=  date.today()
                    pivotdb_to_fleet_sync_error_message= status

                    half_flow_odoo_topivotdb.veh_drivers_datas_pivotdb_to_fleet_update_status(drivers_datas["user_id"], pivotdb_to_fleet_sync_status, pivotdb_to_fleet_sync_date,pivotdb_to_fleet_sync_error_message)
                    #print("KO")     
                
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Veh: this is also an error: Djo some thing is wrong here")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()



def getting_company_datas_from_pivotdb_to_fleet():
    
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
        postgres_select_query= """ select id_company, client_id, nom from company"""

        drivers_datas= dict()
               
        try:
            cur.execute(postgres_select_query)
            drivers_records = cur.fetchall()

            for drivers in drivers_records:
                id_company, client_id, nom=drivers
                drivers_datas["company_id"]= str(id_company)
                drivers_datas["client_id"]= str(client_id)
                drivers_datas["name"]= str(nom)
                #Call fleet api to send this drivers datas to fleet
                print("COMPANY DATAS SENT TO FLEET:", drivers_datas)

                status= fleet_api.new_familly_to_fleet(drivers_datas)
                if status=="OK":
                    pivotdb_to_fleet_sync_status="OK"
                    now =  datetime.now()
                    pivotdb_to_fleet_sync_date = now.strftime("%Y-%m-%d %H:%M:%S")
                    pivotdb_to_fleet_sync_error_message="No error"

                    half_flow_odoo_topivotdb.company_datas_pivotdb_to_fleet_update_status(str(drivers_datas["company_id"]), str(pivotdb_to_fleet_sync_status), str(pivotdb_to_fleet_sync_date), str(pivotdb_to_fleet_sync_error_message))

                else:
                    pivotdb_to_fleet_sync_status="KO"
                    pivotdb_to_fleet_sync_date=  date.today()
                    pivotdb_to_fleet_sync_error_message= status

                    half_flow_odoo_topivotdb.company_datas_pivotdb_to_fleet_update_status(str(drivers_datas["company_id"]), str(pivotdb_to_fleet_sync_status), str(pivotdb_to_fleet_sync_date),str(pivotdb_to_fleet_sync_error_message))
                    #print("KO")     

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here")
        
        
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()

def getting_abonne_datas_from_pivotdb_to_fleet():
    
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
        postgres_select_query= """ select id_contract, code, name, company_id from contract"""

        drivers_datas= dict()
               
        try:
            cur.execute(postgres_select_query)
            drivers_records = cur.fetchall()

            for drivers in drivers_records:
                companycontract_id, client_id, name, company=drivers
                auth= str(True).lower()
                #pos= str(company).find(',')
                drivers_datas["companycontract_id"]=str(companycontract_id)
                drivers_datas["client_id"]= str(client_id)
                drivers_datas["name"]= str(name)
                drivers_datas["company"]= str(company)
                #drivers_datas["auth_account"]= str('true')
                #print("Company_id: ", type(drivers_datas["company"]))
                #print(drivers_datas["companycontract_id"], drivers_datas["client_id"], drivers_datas["name"],drivers_datas["company"] )
                #Call fleet api to send this drivers datas to fleet
                #print(" = str(company)")
                print("Abonne datas sending to Fleet: ", drivers_datas)

                status= fleet_api.new_company_contract_to_fleet(drivers_datas)
                if status=="OK":
                    pivotdb_to_fleet_sync_status="OK"
                    now =  datetime.now()
                    pivotdb_to_fleet_sync_date = now.strftime("%Y-%m-%d %H:%M:%S")
                    pivotdb_to_fleet_sync_error_message="No error"

                    half_flow_odoo_topivotdb.abonne_datas_pivotdb_to_fleet_update_status(str(drivers_datas["companycontract_id"]), str(pivotdb_to_fleet_sync_status), str(pivotdb_to_fleet_sync_date), str(pivotdb_to_fleet_sync_error_message))

                else:
                    now =  datetime.now()
                    pivotdb_to_fleet_sync_status="KO"
                    pivotdb_to_fleet_sync_date = now.strftime("%Y-%m-%d %H:%M:%S")
                    pivotdb_to_fleet_sync_error_message= status

                    half_flow_odoo_topivotdb.abonne_datas_pivotdb_to_fleet_update_status(str(drivers_datas["companycontract_id"]), str(pivotdb_to_fleet_sync_status), str(pivotdb_to_fleet_sync_date),str(pivotdb_to_fleet_sync_error_message))
                    #print("KO")     

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here")
        
        
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()


def getting_services_datas_from_pivotdb_to_fleet():
    
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
        postgres_select_query= """ select id_service, code_service, service_name, id_contract_parentid from service"""

        drivers_datas= dict()
               
        try:
            cur.execute(postgres_select_query)
            drivers_records = cur.fetchall()

            for drivers in drivers_records:
                companyservice_id, client_id, name, contract=drivers
                
                drivers_datas["companyservice_id"]= str(companyservice_id)
                drivers_datas["client_id"]= str(client_id)
                drivers_datas["name"]= str(name)
                drivers_datas["contract"]=int(contract)
                #drivers_datas["comment_to_call_taker"]= str(comment_to_call_taker)
                #drivers_datas["comment_to_driver"]= str(comment_to_driver)

                print("Services sending to fleet: ", drivers_datas)
                #print(drivers_datas["id_service"], drivers_datas["code_service"], drivers_datas["service_name"],drivers_datas["id_contract_parentid"] )
                #Call fleet api to send this drivers datas to fleet
                
                status= fleet_api.new_sevice_to_fleet(drivers_datas)
                if status=="OK":
                    pivotdb_to_fleet_sync_status="OK"
                    now =  datetime.now()
                    pivotdb_to_fleet_sync_date = now.strftime("%Y-%m-%d %H:%M:%S")
                    pivotdb_to_fleet_sync_error_message="No error"

                    half_flow_odoo_topivotdb.services_datas_pivotdb_to_fleet_update_status(str(drivers_datas["companyservice_id"]), str(pivotdb_to_fleet_sync_status), str(pivotdb_to_fleet_sync_date), str(pivotdb_to_fleet_sync_error_message))

                else:
                    pivotdb_to_fleet_sync_status="KO"
                    now =  datetime.now()
                    pivotdb_to_fleet_sync_date=  now.strftime("%Y-%m-%d %H:%M:%S")
                    pivotdb_to_fleet_sync_error_message= status

                    half_flow_odoo_topivotdb.services_datas_pivotdb_to_fleet_update_status(str(drivers_datas["companyservice_id"]), str(pivotdb_to_fleet_sync_status), str(pivotdb_to_fleet_sync_date),str(pivotdb_to_fleet_sync_error_message))
                    #print("KO")     

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("Djo some thing is wrong here")
        
        
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    #getting_company_datas_from_pivotdb_to_fleet()
    getting_abonne_datas_from_pivotdb_to_fleet()
    #getting_services_datas_from_pivotdb_to_fleet()
    #getting_drivers_vehiculedatas_from_pivotdb_to_fleet()
    #getting_drivers_datas_from_pivotdb_to_fleet()
