import code
from unicodedata import name
import requests
import endpoints
import authotoken

def new_drivers_to_fleet(datas):

    hed = {'Authorization': 'Bearer ' + authotoken.token}

    '''datass={
            "user_id": "driver_333458",
            "user_client_id": 21212358,
            "last_name": "Cisse",
            "first_name": "Moahamed",
            "email": "mc.lopez@gmail.com",
            "gsm": "+339403090321",
            "address": "3 rue des tulipes, paris",
            "group_client_id": 121221,
            "name": "group1"
        }
    '''

    response = requests.post(endpoints.url_driver, datas, headers=hed)
    status= response.status_code
    
    if status==200:
        return "OK"
    
    else:
        resp=response.json()
        message=  resp["message"] 
        name= resp["name"]
        code= resp["code"]
        context= resp["context"]
        reason=  str(name) + ": "  + str(message) + "  "  + str(code)
        return reason


def updated_drivers_to_fleet(datas=None):

    hed = {'Authorization': 'Bearer ' + authotoken.token}

    datas={
            "user_id": "driver_333458",
            "user_client_id": 21212358,
            "last_name": "Cisse",
            "first_name": "Moahamed",
            "email": "mc.lopez@gmail.com",
            "gsm": "+339403090321",
            "address": "3 rue des tulipes, paris",
            "group_client_id": 121221,
            "name": "group1"
        }
    response = requests.put(endpoints.url_driver, datas, headers=hed)
    status= response.status_code
    
    if status==200:
        return "OK"
 
    else:
        return response.reason


def delete_drivers_to_fleet(datas=None):

    hed = {'Authorization': 'Bearer ' + authotoken.token}

    datas={
            "user_id": "driver_333458",
            "user_client_id": 21212358,
            "last_name": "Cisse",
            "first_name": "Moahamed",
            "email": "mc.lopez@gmail.com",
            "gsm": "+339403090321",
            "address": "3 rue des tulipes, paris",
            "group_client_id": 121221,
            "name": "group1"
        }
    response = requests.delete(endpoints.url_driver, datas, headers=hed)
    status= response.status_code
    if status==200:
        print("Yes: that's was a sucess", status) 
    else:
        print("that's was not the case", status)

    #print(json_result)

def new_vehicule_to_fleet(datas):

    #print("new_vehicule_to_fleet: is ", datas)

    hed = {'Authorization': 'Bearer ' + authotoken.token}

    '''datas= {
    "user_id": "10976",
    "user_client_id": "",
    "last_name": "Mah",
    "first_name": "Folomana",
    "email": "bvmrah1989@hotmail.com",
    "gsm": "+336077986798",
    "adresse": "ATHIS MONS",
    "group_client_id": "19904",
    "name": "Mah Folomana",
    "vehicle": {
        "plaque": "ZvxCG-007-VNYXDF",
        "brand": "Renault11",
        "model": "Renault/RAV41",
        "color": "Gris1",
        "co2": 0.01
             }
    }
    
    '''
   
    response = requests.post(endpoints.url_driver, datas, headers=hed)
  
    if  response.status_code==200:
        return "OK"
    else:
        resp=response.json()
        message=  resp["message"] 
        name= resp["name"]
        code= resp["code"]
        context= resp["context"]
        reason=  str(name) + ": "  + str(message) + "  "  + str(code)
        return reason
        
    

def new_familly_to_fleet(datas):
    
    hed = {'Authorization': 'Bearer ' + authotoken.token}
    
    '''datas={
            "company_id": "test_1",
            "client_id": 62377,
            "name": "I2C"
        }
    '''
    response = requests.post(endpoints.url_company, datas, headers=hed)
    status= response.status_code
    if status==200:
        return "OK"
    else:
        resp=response.json()
        message=  resp["message"] 
        name= resp["name"]
        code= resp["code"]
        context= resp["context"]
        reason=  str(name) + ": "  + str(message) + "  "  + str(code)
        return reason
    
    
def new_company_contract_to_fleet(datas):
    
    hed = {'Authorization': 'Bearer ' + authotoken.token}
    
    '''datas= {
            "companycontract_id": "280410",
            "client_id": "2691",
            "name": "MME DU BOISROUVRAY",
            "company": "249640",
            "auth_account": 'true'
         }
    '''
    
    response = requests.post(endpoints.url_abonne, datas, headers=hed)

    status= response.status_code
    
    if status==200:
        return "OK"
    else:
        resp=response.json()
        message=  resp["message"] 
        name= resp["name"]
        code= resp["code"]
        context= resp["context"]
        reason=  str(name) + ": "  + str(message) + "  "  + str(code)
        return reason
    
def new_sevice_to_fleet(datas):
    
    hed = {'Authorization': 'Bearer ' + authotoken.token}
    
    '''
    datas= {
            "companyservice_id": "testservice_2",
            "client_id": 20012,
            "name": "TestODOO2",
            "contract": "testabonne_1",
            "comment_to_call_taker": "attention au numéro fixe",
            "comment_to_driver": "bagage à main"
            }
    '''

    response = requests.post(endpoints.url_service, datas, headers=hed)
    
    status= response.status_code
    if status==200:
        return "OK"
    else:
        resp=response.json()
        message=  resp["message"] 
        name= resp["name"]
        code= resp["code"]
        context= resp["context"]
        reason=  str(name) + ": "  + str(message) + "  "  + str(code)+ "  "  + str(context)
        return reason

if __name__ == "__main__":
    #print(new_vehicule_to_fleet(datas=None))
    #print(get_vehicules())
    #print(get_company())
    #print((new_sevice_to_fleet()))
    print(new_company_contract_to_fleet(datas=None))
    pass