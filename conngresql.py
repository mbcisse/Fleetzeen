from config import config
import psycopg2
import datetime

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

def connect():
    conn = None
    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        cur = conn.cursor()  

        return (conn, cur)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

    return (conn, cur)


def update_datas(driver_id, tempstatus):
    conn, cur= connect()
    sql_update_query = """Update new_vehdri_to_fleet set status = %s where id = %s"""
    cur.execute(sql_update_query, (tempstatus, driver_id))
    conn.commit()
    close_connect(conn, cur)
    


def inserting_datas(datas, datas1, tempstatus):
    
    conn, cur= connect()
    postgres_insert_query= """ INSERT INTO new_vehdri_to_fleet (driver_id, radio_code, driver_firstname, driver_lastname, 
    email, mobile, city, ref,name, plaque, brand, model, color, co2, status, input_date) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
   
    record_to_insert = """(datas.get('id'), datas.get('radio_code'),datas.get('driver_lastname'), datas.get('driver_firstname'),
                   datas.get('email'),datas.get('mobile'),
                   datas.get('city'),datas.get('ref'),datas.get('display_name'),
                   datas1.get('plaque'),datas.get('brand'),datas.get('model'),
                   datas1.get('color'),datas.get('co2')), tempstatus, today = datetime.date.today()"""
  
    cur.execute(postgres_insert_query, record_to_insert)
    conn.commit()
    count = cur.rowcount
    print(count, "Record inserted successfully")

    close_connect(conn, cur)



if __name__ == '__main__':

    a, b=connect()
    print(a,b)
