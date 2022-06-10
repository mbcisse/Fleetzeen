import json 
import odoo_to_fleetzeen
import fleet_api 
import conngresql

drivers= [{'id': 337799, 'radio_code': 2288, 'driver_lastname': 'Bassirou', 'driver_firstname': 'Cisse', 'email': 
'sarah94a@hotmail.com', 'mobile': '+33607682434', 'street': '18 RUE LIONEL DUBRAY', 'zip': '91200', 
'city': 'ATHIS MONS', 'ref': '9546102', 'display_name': 'Bassirou Cisse'}, 
{'id': 1331177, 'radio_code': 1188, 'driver_lastname': 'Keita', 'driver_firstname': 'Madou', 'email': 
'sarah94a@hotmail.com', 'mobile': '+33607682434', 'street': '18 RUE LIONEL DUBRAY', 'zip': '91200', 
'city': 'ATHIS MONS', 'ref': '9546102', 'display_name': 'ABADOU FARID'}]

vehicules=[{'id': 1495, 'name': 'Renault/SCENIC/CG-007-VN1KXX', 'driver_id': [337799, 'Bassirou Cisse'], 'license_plate': 
'ZCG-007-VN1', 'brand_id': [521, 'Renault1'], 'model_id': [13111, 'Renault/SCENIC1'], 'color': 'Gris1', 'co2': 0.01}, {'id': 14449, 'name': 'Renault/SCENIC/CG-007-VNVV', 'driver_id': [1331177, 'LECHABLE ERIC'], 
'license_plate': 'BXCG-007-VN', 'brand_id': [52, 'Renault'], 'model_id': [1311, 'Renault/SCENIC'], 'color': 'Gris', 'co2': 0.0}]


#drivers= odoo_to_fleetzeen.get_drivers()
#vehicules= odoo_to_fleetzeen.get_vehicules()

print("len()drivers  : ", len(drivers))
print("len()vehicules: ", len(vehicules))

with open("drivers.json", "w") as outfile:
                outfile.write(json.dumps(drivers, indent=4))

with open("vehicules.json", "w") as outfile:
                outfile.write(json.dumps(vehicules, indent=4))


if __name__ == "__main__":
        
        print("Dtrivers type", type(drivers))
        print("Dtrivers type", type(vehicules))
        odoo_datas_to_fleet= dict()
        temp=dict()
        last_result=[]

        for driver in drivers:
                #print("Drivers: " , driver)
                vehicule_datas= dict()
                fleet_datas=dict()
                for vehicule in vehicules:
                        #print("Vehiciule: ", vehicule)

                        if vehicule.get('driver_id')!= False and driver.get('radio_code') !=False:
                               if driver.get('id')==vehicule.get('driver_id')[0]:     
                                       fleet_datas['user_id']=str(driver.get('id'))
                                       fleet_datas['user_client_id']= int(driver.get('radio_code'))
                                       #fleet_datas['user_client_id']= int(driver.get('ref'))
                                       fleet_datas['last_name']=driver.get('driver_lastname')
                                       fleet_datas['first_name']= driver.get('driver_firstname')
                                       fleet_datas['email']           = driver.get('email')
                                       fleet_datas['gsm'] =        driver.get('mobile')
                                       fleet_datas['adresse']=  driver.get('street') + ' '+ driver.get('zip') + ' '+ driver.get('city')
                                       fleet_datas['group_client_id']=  int(driver.get('ref'))
                                       #fleet_datas['group_client_id']=  int(driver.get('radio_code'))
                                       fleet_datas['name']=  driver.get('display_name')
                                
                                       vehicule_datas['plaque']= vehicule.get('license_plate')
                                       vehicule_datas['brand']= vehicule.get('brand_id')[1]
                                       vehicule_datas['model']= vehicule.get('model_id')[1].split('/')[1]
                                       vehicule_datas['color']= vehicule.get('color')
                                       vehicule_datas['co2']= vehicule.get('co2')

                                       fleet_datas["vehicle"]=vehicule_datas

                                       last_result.append(fleet_datas)
                
                #tempstatus="In Progress"
                #fleet_data= fleet_datas
                #vehicule_data=vehicule_datas

        print(len(last_result))
        if len(last_result)==0:
                #No macthing datas to process
                pass
        
        
        with open("output.json", "w") as outfile:
                outfile.write(json.dumps(last_result, indent=4))
        
        for fleet_data in last_result:
                tempstatus="In Progress"
                vehicule_datas= fleet_data.get("vehicle")
                conngresql.inserting_datas(fleet_data, vehicule_datas, tempstatus, tempstatus)
                json_object = json.dumps(fleet_data, indent = 4) 
                if json_object is not None:
                        status= fleet_api.new_vehicule_to_fleet(json_object)
                        if status=="OK":
                                tempstatus= "OK"
                                conngresql.update_datas(str(fleet_data['user_id']), tempstatus, 'No error')
                                #print("OK")
                        else:
                                tempstatus= "KO"
                                faillure_message= status
                                conngresql.update_datas(str(fleet_data['user_id']), tempstatus,faillure_message )
                                #print("KO")                   
                                          