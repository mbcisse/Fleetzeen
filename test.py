import json 
import odoo_to_fleetzeen
import fleet_api 
import conngresql

drivers= [{'id': 55256, 'radio_code': False, 'driver_lastname': 'ABADOU', 'driver_firstname': 'FARID', 'email': 
'sarah94a@hotmail.com', 'mobile': '+33607682434', 'street': '18 RUE LIONEL DUBRAY', 'zip': '91200', 
'city': 'ATHIS MONS', 'ref': '9546102', 'display_name': 'ABADOU FARID'}, 
{'id': 55257, 'radio_code': False, 'driver_lastname': 'ABADOU', 'driver_firstname': 'FARID', 'email': 
'sarah94a@hotmail.com', 'mobile': '+33607682434', 'street': '18 RUE LIONEL DUBRAY', 'zip': '91200', 
'city': 'ATHIS MONS', 'ref': '9546102', 'display_name': 'ABADOU FARID'}]

vehicules=[{'id': 1495, 'name': 'Renault/SCENIC/CG-007-VN1', 'driver_id': [55256, 'LECHABLE1 ERIC1'], 'license_plate': 
'CG-007-VN1', 'brand_id': [521, 'Renault1'], 'model_id': [13111, 'Renault/SCENIC1'], 'color': 'Gris1', 'co2': 0.01}, {'id': 14449, 'name': 'Renault/SCENIC/CG-007-VN', 'driver_id': [55257, 'LECHABLE ERIC'], 
'license_plate': 'CG-007-VN', 'brand_id': [52, 'Renault'], 'model_id': [1311, 'Renault/SCENIC'], 'color': 'Gris', 'co2': 0.0}]

#drivers= odoo_to_fleetzeen.get_drivers()
#vehicules= odoo_to_fleetzeen.get_vehicules()
if __name__ == "__main__":
        
        print("Dtrivers type", type(drivers))
        print("Dtrivers type", type(vehicules))
        odoo_datas_to_fleet= dict()
        temp=dict()

        for driver in drivers:
                vehicule_datas= dict()
                fleet_datas=dict()
                for vehicule in vehicules:
                       if vehicule.get('driver_id')!= False:
                               if driver.get('id')==vehicule.get('driver_id')[0]:     
                                       fleet_datas['id']=driver.get('id')
                                       fleet_datas['radio_code']= driver.get('radio_code')
                                       fleet_datas['driver_lastname']=driver.get('driver_lastname')
                                       fleet_datas['driver_firstname']= driver.get('driver_lastname')
                                       fleet_datas['email']           = driver.get('email')
                                       fleet_datas['mobile'] =        driver.get('mobile')
                                       fleet_datas['city']=  driver.get('city')
                                       fleet_datas['ref']=  driver.get('ref')
                                       fleet_datas['display_name']=  driver.get('display_name')
                                
                                       vehicule_datas['plaque']= vehicule.get('license_plate')
                                       vehicule_datas['brand']= vehicule.get('brand_id')[1]
                                       vehicule_datas['model']= vehicule.get('model_id')[1]
                                       vehicule_datas['plaque']= vehicule.get('license_plate')
                                       vehicule_datas['color']= vehicule.get('color')
                                       vehicule_datas['co2']= vehicule.get('co2')

                                       fleet_datas["vehicle"]=vehicule_datas
                
                tempstatus="In Progress"

                conngresql.inserting_datas(fleet_datas, vehicule_datas,tempstatus)
                json_object = json.dumps(fleet_datas, indent = 4) 
                status= fleet_api.new_vehicule_to_fleet
                
                if status=="OK":
                        tempstatus= "OK"
                        conngresql.update_datas(fleet_datas['id'], tempstatus)

                        print("OK")
                else:
                        tempstatus= "KO"
                        conngresql.update_datas(fleet_datas['id'], tempstatus)
                
                        print("KO")

                print(json_object)

            

        




                        
                                             