import requests
import endpoints
import authotoken

def new_drivers_to_fleet(datas=None):

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
    response = requests.post(endpoints.url_driver, datas, headers=hed)
    status= response.status_code
    if status==200:
        print("Machallah: that's was a sucess", status) 
    else:
        print("that's was not the case", status)

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
        print("Machallah: that's was a sucess", status) 
    else:
        print("that's was not the case", status)

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
        print("Machallah: that's was a sucess", status) 
    else:
        print("that's was not the case", status)

    #print(json_result)

def new_vehicule_to_fleet(datas=None):

    hed = {'Authorization': 'Bearer ' + authotoken.token}

    datas={   
              "user_id": "driver_151",
              "user_client_id": 12123,
              "last_name": "lopez1",
              "first_name": "titi1D",
              "email": "mtiti.lopez@gmail.com",
              "gsm": "+33940309032",
              "address": "3 rue des tulipes, paris",
              "group_client_id": 121231,
              "name": "group1",
              "vehicle": {
                         "plaque": "XDTXAB262",
                         "brand": "audiF",
                         "model": "r81",
                         "color": "noir",
                         "co2": 12.5
                                
                            }
        }
    response = requests.post(endpoints.url_driver, datas, headers=hed)
    
    print(response.content)
    if  response.status_code==200:
        print("Machallah: that's was a sucess", response.status_code) 
    else:
        print("that's was not the case", response.status_code)

def new_familly_to_fleet(datas=None):
    
    hed = {'Authorization': 'Bearer ' + authotoken.token}
    datas={
            "company_id": "test_1",
            "client_id": 62377,
            "name": "I2C"
        }
    response = requests.post(endpoints.url_company, datas, headers=hed)
    
    print(response.content)
    if  response.status_code==200:
        print("Machallah: that's was a sucess", response.status_code) 
    else:
        print("that's was not the case", response.status_code)


def new_company_contract_to_fleet(datas=None):
    
    hed = {'Authorization': 'Bearer ' + authotoken.token}
    datas= {
            "companycontract_id": "testabonne_2",
            "client_id": 6237001,
            "name": "Abo1",
            "company": "test_1",
            "auth_account": 'true'
         }
    response = requests.post(endpoints.url_abonne, datas, headers=hed)
    
    print(response.content)
    if  response.status_code==200:
        print("Machallah: that's was a sucess", response.status_code) 
    else:
        print("that's was not the case", response.status_code)

def new_sevice_to_fleet(datas=None):
    
    hed = {'Authorization': 'Bearer ' + authotoken.token}
    datas= {
            "companyservice_id": "testservice_2",
            "client_id": 20012,
            "name": "TestODOO2",
            "contract": "testabonne_1",
            "comment_to_call_taker": "attention au numéro fixe",
            "comment_to_driver": "bagage à main"
            }
    response = requests.post(endpoints.url_service, datas, headers=hed)
    
    print(response.content)
    if  response.status_code==200:
        print("Machallah: that's was a sucess", response.status_code) 
    else:
        print("that's was not the case", response.status_code)

if __name__ == "__main__":
    #print(get_drivers())
    #print(get_vehicules())
    #print(get_company())
    print((new_sevice_to_fleet()))