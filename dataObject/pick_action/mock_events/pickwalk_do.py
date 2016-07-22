import argparse
import pickwalk_random_generators as prg
import pprint
from datetime import datetime, timedelta
import copy
import json
import logging



CONTAINER_TYPES = ['TRAY']
QUANTITY_TYPES  = ['EACH', 'KILO', 'LITRE']
REGIME_TYPES    = ['AMBIENT']
#REGIME_TYPES    = ['AMBIENT', 'CHILLED', 'FREEZER']
NUMBER_POSITIONS = 3
MIN_SECONDS_BETWEEN_PICKS = 30


def define_catalogue(n=200):
    catalogue = {}
    for n in range(0, n):
        catalogue[n] = {"sku_id": prg.random_string(),
                        "quantity_type": prg.random_element(QUANTITY_TYPES),
                        "layout_id": prg.random_string(4)}
    return catalogue


def define_routes(n=3):
    routes = [];
    for i in range(0, n):
        routes.append(prg.random_string(8))
    return routes


def define_orders(routes=None, n=6):
    orders = {};
    for i in range(0, n):
        orders[prg.random_string(4)] = prg.random_element(routes)

    return orders


def define_trolley(orders=None):
    trolley = {}
    for n in range(1, 7):
        order_id = prg.random_element(orders.keys())
        trolley[n] = {"order_id": order_id,
                      "container_id": prg.random_string(),
                      "route_id": orders[order_id]}
    return trolley


def define_pickers(n=4):
    pickers = {}
    for i in range(0, n):
        delay = 0
        if i == 0:
            delay = MIN_SECONDS_BETWEEN_PICKS
        elif i == n - 1:
            delay = int(-MIN_SECONDS_BETWEEN_PICKS/2)
        pickers[prg.random_string()] = delay
    return pickers



def get_sku(catalogue=None, done=None):
    while(True):
        i = prg.random_element(catalogue.keys())
        if i not in done:
            done[i] = True
            return i


def generate_pick_item_data(ContainerId=None,
                            ContainerPosition=None,
                            ContainerType=None,
                            OrderId=None,
                            RouteId=None,
                            PickTime=None,
                            QuantityType=None,
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


def generate_pick_object_data(PickerId=None,
                              layoutPositionId=None,
                              SkuId=None,
                              Regime=None,
                              StartClientTimestamp=None,
                              EndClientTimestamp=None,
                              PickingDurationInSeconds=None,
                              PickedItems=None):
    return {
                "PickerId":   PickerId,
                "layoutPositionId": layoutPositionId,
                "SkuId":      SkuId,
                "Regime":     Regime,
                "StartClientTimestamp": StartClientTimestamp,
                "EndClientTimestamp": EndClientTimestamp,
                "PickingDurationInSeconds": int(PickingDurationInSeconds),
                "PickedItems": PickedItems
            }


def generate_pickwalk_object_data(StoreId=None,
                                  PickwalkId=None,
                                  PickerIds=None,
                                  StartClientTimestamp=None,
                                  EndClientTimestamp=None,
                                  _NamePartition=None,
                                  _createdAt=None,
                                  Picks=None):

    picks_duration = sum_picks_duration(Picks)
    pickwalk_duration = calculate_pickwalk_duration(Picks)
    return {
                "StoreId":    StoreId,
                "PickwalkId":  PickwalkId,
                "PickerIds":   PickerIds,
                "StartClientTimestamp": StartClientTimestamp,
                "EndClientTimestamp": EndClientTimestamp,
                "PicksDurationInSeconds": int(picks_duration),
                "IdleTimeInSeconds": int(pickwalk_duration - picks_duration),
                "PickwalkDurationInSeconds": int(pickwalk_duration),
                "_NamePartition": _NamePartition,
                "_createdAt": _createdAt,
                "Picks": Picks
            }

        
def generate_pick_objects(delay=None, no_objects=None, catalogue=None,
                         trolley=None, picker_id=None, start_time=None):
    pick_objects = []
    
    sku_done = {}
    running_time = copy.deepcopy(start_time)
    for n in range(0, no_objects):
        
        catalogue_item = get_sku(catalogue=catalogue, done=sku_done)
        sku = catalogue[catalogue_item]["sku_id"]
        layout = catalogue[catalogue_item]["layout_id"]
        quantity_type = catalogue[catalogue_item]["quantity_type"]
        regime = prg.random_element(REGIME_TYPES)
        container_type = prg.random_element(CONTAINER_TYPES)
        
        start_client_timestamp = copy.deepcopy(running_time)
        running_time += timedelta(seconds=delay + prg.random_second(min=MIN_SECONDS_BETWEEN_PICKS, max=180))
        
        picks = []
        for tray in trolley.keys():
            quantity = prg.random_integer(4) - 1
            if quantity > 0:
                container_position = prg.random_integer(NUMBER_POSITIONS)
                running_time += timedelta(seconds=prg.random_second(max=20))
                picks.append(generate_pick_item_data(ContainerId=trolley[tray]["container_id"],
                                                     ContainerPosition=container_position,
                                                     ContainerType=container_type,
                                                     OrderId=trolley[tray]["order_id"],
                                                     RouteId=trolley[tray]["route_id"],
                                                     PickTime=running_time.strftime("%Y-%m-%d %H:%M:%S"),
                                                     QuantityType=quantity_type,
                                                     QuantityToPick=quantity,
                                                     QuantityPicked=quantity))
                
        pick_object = generate_pick_object_data(PickerId=picker_id,
                                                layoutPositionId=layout,
                                                SkuId=sku,
                                                Regime=regime,
                                                StartClientTimestamp=start_client_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                                                EndClientTimestamp=running_time.strftime("%Y-%m-%d %H:%M:%S"),
                                                PickingDurationInSeconds=(running_time - start_client_timestamp).total_seconds(),
                                                PickedItems=picks)
        
        pick_objects.append(pick_object)
        
        # adding idle time
        if delay > 0:
            running_time += timedelta(seconds=delay)
        elif not delay < 0:
            running_time += timedelta(seconds=prg.random_second(max=10))


        
    return pick_objects


def sum_picks_duration(pick_objects=None):
    tot = 0
    for pdo in pick_objects:
        tot += pdo["PickingDurationInSeconds"]
    return tot


def calculate_pickwalk_duration(pick_objects=None):
    start = datetime.strptime(pick_objects[0]["StartClientTimestamp"], "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(pick_objects[-1]["EndClientTimestamp"], "%Y-%m-%d %H:%M:%S")
    return (end - start).total_seconds()


def generate_pickwalk_object(delay=None, no_objects=None, store_id=None, pickwalk_id=None, catalogue=None,
                             trolley=None, picker_id=None, start_time=None):
    pick_objects = generate_pick_objects(delay=delay,
                                         no_objects=10,
                                        picker_id=picker_id,
                                        trolley=trolley,
                                        catalogue=catalogue,
                                        start_time=copy.deepcopy(start_time))

    return generate_pickwalk_object_data(StoreId=store_id,
                                         PickwalkId=pickwalk_id,
                                         PickerIds=[picker_id],
                                         StartClientTimestamp=pick_objects[0]["StartClientTimestamp"],
                                         EndClientTimestamp=pick_objects[-1]["EndClientTimestamp"],
                                         _NamePartition=start_time.strftime("%Y%m%d"),
                                         _createdAt=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                         Picks=pick_objects)
 




