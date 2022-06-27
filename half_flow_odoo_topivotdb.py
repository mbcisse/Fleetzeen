from config import config
import psycopg2
from datetime import date

def update_datas(driver_id, tempstatus,  failure_message):
    conn = None
    try:
        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        cur = conn.cursor()
        sql_update_query = """Update fleetzeen_log set status = %s, failure_message  = %s where user_id = %s"""
        
        try:
            cur.execute(sql_update_query, (str(tempstatus), str(failure_message), str(driver_id)))
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("DJO IL YA ERROR: ", error)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')


def inserting_datas(datas, datas1, tempstatus, failure_message):
    
    conn = None
    try:
        params = config()

        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        #print('Connected to the PostgreSQL database...')

        cur = conn.cursor()  
        postgres_insert_query= """INSERT INTO fleetzeen_log (user_id, user_client_id, last_name, first_name, 
                                 email, gsm, adresse, group_client_id,name, plaque, brand, model, color, co2, input_date, status, failure_message) 
                                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        
        record_to_insert = (datas.get('user_id'), datas.get('user_client_id'),datas.get('last_name'), datas.get('first_name'),
                   datas.get('email'),datas.get('gsm'),
                   datas.get('adresse'),datas.get('group_client_id'),datas.get('name'),
                   datas1.get('plaque'),datas1.get('brand'),datas1.get('model'),
                   datas1.get('color'),datas1.get('co2'), date.today(), tempstatus, failure_message)

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
    


    from config import config
import psycopg2
from datetime import date

def close_connect(conn, cur):
    
    try:
        cur.close()
        conn.close()
 
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def connection():
    conn = None
    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        cur = conn.cursor()  
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
        

def update_datas(driver_id, tempstatus,  failure_message):
    conn = None
    try:
        params = config()

        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        cur = conn.cursor()
        sql_update_query = """Update fleetzeen_log set status = %s, failure_message  = %s where user_id = %s"""
        
        try:
            cur.execute(sql_update_query, (str(tempstatus), str(failure_message), str(driver_id)))
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("DJO IL YA ERROR: ", error)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')


def full_half_flow_VehicDrivers_to_pivotdb(vh_datas, tempstatus, failure_message):
    
    conn = None
    try:
        params = config()

        #print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(      user="openpg",
                                      password="openpgpwd",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="Fleetzeen")
		
        #print('Connected to the PostgreSQL database...')

        cur = conn.cursor()  
        postgres_insert_query= """INSERT INTO drivers_vehicules (id, radio_code, contrat_number, start_alpha_code_radio, end_alpha_code_radio,
                                                                 driver_first_name, driver_last_name, email, mobile, adresse, ident_adherent, display_name,
                                                                 id_vehicule_precedent, start_vehic_fleet_prec, end_vehic_fleet_prec, odoo_to_pivotdb_input_date,
                                                                  odoo_to_pivotdb_last_update, pivotdb_to_fleet_sync_date, pivotdb_to_fleet_sync_status, 
                                                                  odoo_to_pivotdb_sync_error_message) 
                                                                  VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s )"""
        
        record_to_insert = (datas.get('user_id'), datas.get('user_client_id'),datas.get('last_name'), datas.get('first_name'),
                   datas.get('email'),datas.get('gsm'),
                   datas.get('adresse'),datas.get('group_client_id'),datas.get('name'),
                   datas1.get('plaque'),datas1.get('brand'),datas1.get('model'),
                   datas1.get('color'),datas1.get('co2'), date.today(), tempstatus, failure_message)

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
    
    



if __name__ == '__main__':
   inserting_datas(None, None, "KO")

    



if __name__ == '__main__':
   inserting_datas(None, None, "KO")
