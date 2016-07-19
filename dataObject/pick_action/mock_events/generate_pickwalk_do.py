import random_generators as rg
import pprint
from datetime import datetime, timedelta
import copy
import json



CONTAINER_TYPES = ['TRAY']
QUANTITY_TYPES  = ['EACH', 'KILO', 'LITRE']
REGIME_TYPES    = ['AMBIENT']
#REGIME_TYPES    = ['AMBIENT', 'CHILLED', 'FREEZER']
NUMBER_POSITIONS = 3

def random_string(length=8):
    return rg.random_lower_alphabetic_str(length)


def random_element(s):
    return rg.random_from_sequence(s)


def random_integer(n):
    return rg.random_integer_by_range(1, n+1)


def define_catalogue(n=20):
    catalogue = {}
    for n in range(1, n):
        catalogue[n] = {"sku_id": random_string(),
                        "layout_id": random_string(4)}
    return catalogue


def define_trolley():
    routes = [];
    for i in range(1, 3):
        routes.append(random_string(8))

    orders = {};
    for i in range(1, random_integer(6)+1):
        orders[random_string(4)] = random_element(routes)
        
    trolley = {}
    for n in range(1, 7):
        order_id = random_element(orders.keys())
        trolley[n] = {"order_id": order_id,
                      "container_id": random_string(),
                      "route_id": orders[order_id]}
    return trolley


def get_sku(catalogue=None, done=None):
    while(True):
        i = random_element(catalogue.keys())
        if i not in done:
            done[i] = True
            return i


def generate_pick_item_data(ContainerId=random_string(),
                            ContainerPosition=random_integer(6),
                            ContainerType=random_element(CONTAINER_TYPES),
                            OrderId=None,
                            RouteId=None,
                            PickTime=None           ,
                            QuantityType=random_element(QUANTITY_TYPES),
                            QuantityToPick=None,
                            QuantityPicked=None):
   return {
                "ContainerId": ContainerId,
                "ContainerPosition": str(ContainerPosition),
                "ContainerType": ContainerType,
                "OrderId":     OrderId,
                "RouteId":     RouteId,
                "PickTime": PickTime,
                "QuantityType": QuantityType,
                "QuantityToPick": QuantityToPick,
                "QuantityPicked": QuantityPicked
            }


def generate_pick_object_data(StoreId=None,
                              PickwalkId=None,
                              PickerId=None,
                              layoutPositionId=None,
                              SkuId=None,
                              Regime=None,
                              StartClientTimestamp=None,
                              EndClientTimestamp=None,
                              PickingDurationInSeconds=None,
                              _NamePartition=None,
                              _createdAt=None,
                              PickedItems=None):
    return {
                #"StoreId":    StoreId,
                #"PickwalkId":  PickwalkId,
                "PickerId":   PickerId,
                "layoutPositionId": layoutPositionId,
                "SkuId":      SkuId,
                "Regime":     Regime,
                "StartClientTimestamp": StartClientTimestamp,
                "EndClientTimestamp": EndClientTimestamp,
                "PickingDurationInSeconds": int(PickingDurationInSeconds),
                #"_NamePartition": _NamePartition,
                #"_createdAt": _createdAt,
                "PickedItems": PickedItems
            }


def generate_pickwalk_object_data(StoreId=None,
                                  PickwalkId=None,
                                  PickerIds=None,
                                  StartClientTimestamp=None,
                                  EndClientTimestamp=None,
                                  PicksDurationInSeconds=None,
                                  IdleTimeInSeconds=None,
                                  PickwalkDurationInSeconds=None,
                                  _NamePartition=None,
                                  _createdAt=None,
                                  Picks=None):
    return {
                "StoreId":    StoreId,
                "PickwalkId":  PickwalkId,
                "PickerIds":   PickerIds,
                "StartClientTimestamp": StartClientTimestamp,
                "EndClientTimestamp": EndClientTimestamp,
                "PicksDurationInSeconds": int(PicksDurationInSeconds),
                "IdleTimeInSeconds": int(IdleTimeInSeconds),
                "PickwalkDurationInSeconds": int(PickwalkDurationInSeconds),
                "_NamePartition": _NamePartition,
                "_createdAt": _createdAt,
                "Picks": Picks
            }

        
def generate_pick_objects(no_objects=None, store_id=None, pickwalk_id=None, catalogue=None,
                         trolley=None, picker_id=None, start_time=None):
    pick_objects = []
    
    sku_done = {}
    running_time = copy.deepcopy(start_time)
    for n in range(0, no_objects):
        
        catalogue_item = get_sku(catalogue=catalogue, done=sku_done)
        sku = catalogue[catalogue_item]["sku_id"]
        layout = catalogue[catalogue_item]["layout_id"]
        regime = random_element(REGIME_TYPES)
        container_type = random_element(CONTAINER_TYPES)
        quantity_type = random_element(QUANTITY_TYPES)
        
        start_client_timestamp = copy.deepcopy(running_time)
        running_time += timedelta(seconds=random_integer(180))
        
        picks = []
        for tray in trolley.keys():
            quantity = random_integer(4) - 1
            if quantity > 0:
                container_position = random_integer(NUMBER_POSITIONS)
                running_time += timedelta(seconds=random_integer(20))
                picks.append(generate_pick_item_data(ContainerId=trolley[tray]["container_id"],
                                                     ContainerPosition=container_position,
                                                     ContainerType=container_type,
                                                     OrderId=trolley[tray]["order_id"],
                                                     RouteId=trolley[tray]["route_id"],
                                                     PickTime=running_time.strftime("%Y-%m-%d %H:%M:%S"),
                                                     QuantityType=quantity_type,
                                                     QuantityToPick=quantity,
                                                     QuantityPicked=quantity))
                
        pick_object = generate_pick_object_data(StoreId=store_id,
                                                PickwalkId=pickwalk_id,
                                                PickerId=picker_id,
                                                layoutPositionId=layout,
                                                SkuId=sku,
                                                Regime=regime,
                                                StartClientTimestamp=start_client_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                                                EndClientTimestamp=running_time.strftime("%Y-%m-%d %H:%M:%S"),
                                                PickingDurationInSeconds=(running_time - start_client_timestamp).total_seconds(),
                                                _NamePartition=start_client_timestamp.strftime("%Y%m%d"),
                                                _createdAt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                PickedItems=picks)
        
        pick_objects.append(pick_object)
        
        # adding idle time
        running_time += timedelta(seconds=random_integer(10))
        
    return pick_objects


        
def generate_pickwalk_object(no_objects=None, store_id=None, pickwalk_id=None, catalogue=None,
                             trolley=None, picker_id=None, start_time=None):
    pick_objects = generate_pick_objects(no_objects=10,
                                        store_id=store_id,
                                        pickwalk_id=pickwalk_id,
                                        picker_id=picker_id,
                                        trolley=trolley,
                                        catalogue=catalogue,
                                        start_time=copy.deepcopy(start_time))
    
    return generate_pickwalk_object_data(StoreId=None,
                                         PickwalkId=None,
                                         PickerIds=[picker_id],
                                         StartClientTimestamp=pick_objects[0]["StartClientTimestamp"],
                                         EndClientTimestamp=pick_objects[-1]["EndClientTimestamp"],
                                         PicksDurationInSeconds=0.0,
                                         IdleTimeInSeconds=0.0,
                                         PickwalkDurationInSeconds=0.0,
                                         _NamePartition=start_time.strftime("%Y%m%d"),
                                         _createdAt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                         Picks=pick_objects)
 

def main():
    store_id = random_string()
    start_time = datetime.today() - timedelta(days=1)
    catalogue = define_catalogue()
    
    pickwalk_objects = []
    for i in range(0, 4):
        pickwalk_id = random_string()
        picker_id = random_string()
        trolley = define_trolley()
        pickwalk_objects.append(generate_pickwalk_object(no_objects=10,
                                                         store_id=store_id,
                                                         pickwalk_id=pickwalk_id,
                                                         picker_id=picker_id,
                                                         trolley=trolley,
                                                         catalogue=catalogue,
                                                         start_time=copy.deepcopy(start_time) + timedelta(minutes=random_integer(60))))
    
    pprint.pprint(pickwalk_objects)
    #for pdo in pick_objects:
    #    print(json.dumps(pdo))


if __name__ == '__main__':
    main()



