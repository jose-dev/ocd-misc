import argparse
import pprint
from datetime import datetime, timedelta
import copy
import json
import logging
import pickwalk_do as opw
import pickwalk_random_generators as prg
from random import shuffle


CATALOGUE_SIZE = 1000
NUMBER_PICKERS = 5
NUMBER_DAYS = 5
NUMBER_PICKS = 20


################################################################################

def arg_parser():
    parser = argparse.ArgumentParser(description='Transfer test data from local disk to cloud.')
    parser.add_argument('-p', '--number_pickers',  type=int, help='Number of pickers. Default: {}'.format(str(NUMBER_PICKERS)), default=NUMBER_PICKERS)
    parser.add_argument('-c', '--catalogue_size',  type=int, help='Catalogue size.    Default: {}'.format(str(CATALOGUE_SIZE)), default=CATALOGUE_SIZE)
    parser.add_argument('-d', '--number_days',     type=int, help='Number of days.    Default: {}'.format(str(NUMBER_DAYS)),    default=NUMBER_DAYS)
    parser.add_argument('-n', '--number_picks',    type=int, help='Number of picks per pickwalk. Default: {}'.format(str(NUMBER_PICKS)), default=NUMBER_PICKS)
    parser.add_argument('-o', '--output_file',     required=True, type=str, help='Name of output file')
    
    args = parser.parse_args()
    return vars(args)

################################################################################

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s -- %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    
    logging.info("Validating arguments...")
    cmdargs = arg_parser()
    number_pickers = cmdargs['number_pickers'] 
    catalogue_size = cmdargs['catalogue_size'] 
    number_days    = cmdargs['number_days']    
    number_picks   = cmdargs['number_picks']
    fileout        = cmdargs['output_file']


    logging.info("Running modelling...")
    pickwalk_objects = []
    store_id = prg.random_string()
    devices = opw.define_devices(n=number_pickers)
    pickers = opw.define_pickers(number_pickers)
    catalogue = opw.define_catalogue(catalogue_size)
    device_indexes = range(0, len(devices))
    for day_delta in reversed(range(0, number_days)):
        start_time = datetime.today() - timedelta(days=day_delta)
        routes = opw.define_routes()
        orders = opw.define_orders(routes=routes)

        shuffle(device_indexes)
        index = 0
        for picker_id in pickers.keys():
            device = devices[device_indexes[index]]
            pickwalk_id = prg.random_string()
            delay = pickers[picker_id]
            trolley = opw.define_trolley(orders)
            pickwalk_objects.append(opw.generate_pickwalk_object(delay=delay,
                                                                 device=device,
                                                                 no_objects=number_picks,
                                                                 store_id=store_id,
                                                                 pickwalk_id=pickwalk_id,
                                                                 picker_id=picker_id,
                                                                 trolley=trolley,
                                                                 catalogue=catalogue,
                                                                 start_time=copy.deepcopy(start_time) + timedelta(minutes=prg.random_integer(60))))
            index += 1

    logging.info("Printing output...")
    #pprint.pprint(pickwalk_objects)
    with open(fileout, 'w') as f:
        for pwdo in pickwalk_objects:
            f.write(json.dumps(pwdo) + '\n')
        f.close()

    logging.info("All done")


if __name__ == '__main__':
    main()



