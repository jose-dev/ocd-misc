import argparse
import os
import pprint
import logging
import shutil
import hashlib

from testutils.manage_testdata import YamlManager
from utils.datamanager import DataManager
from utils.fileformat_manager import JsonManager
from config.service_config import ServiceConfig





################################################################################

def arg_parser():
    parser = argparse.ArgumentParser(description='Clean up test data from cloud.')
    parser.add_argument('-e',  '--env',      required=True, type=str, help='Run environment', choices=['local', 'dev', 'sit'])
    parser.add_argument('-c',  '--clientid', required=True, type=str, help='Client Id')
    parser.add_argument('-i',  '--infile',   required=True, type=str, help='Yaml file with information about data files for test')
    parser.add_argument('-p',  '--path',     required=True, type=str, help='Main path to test folder')
    
    args = parser.parse_args()
    return vars(args)

################################################################################

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s -- %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    
    # fetch a dict like view of all commandline arguments and attributes
    cmdargs = arg_parser()
    logging.info("Validating arguments...")
    runenv = cmdargs['env']
    clientid = cmdargs['clientid']
    file_tree = cmdargs['infile']
    main_path = cmdargs['path']
    
    
    #
    #
    ### connecting to service to host the test data
    o_servconfig  = ServiceConfig(env=runenv, auth='sa')
    o_datamanager = DataManager(project_number=o_servconfig.project_number,
                                project_id=o_servconfig.project_id,
                                account_email=o_servconfig.service_account_email,
                                account_p12=o_servconfig.service_account_p12)
    
    
    ## read the yaml file into object
    logging.info("Reading the yaml file that defines test data...")
    o_yaml = YamlManager(filein=file_tree, abspath=main_path, env=runenv, clientid=clientid)
    
    #pprint.pprint(o_yaml.__dict__)
    
    
    ### buckets
    parent_bucket = o_yaml.get_bucket_name()
    logging.info("Deleting gcs bucket {}...".format(parent_bucket))
    o_datamanager.delete_storage_bucket(bucket=parent_bucket)
    logging.info("Finished with gcs bucket")
    
    
    ## managing BQ datasets and tables
    tables_for_bq = o_yaml.get_tables_for_bq()
    if len(tables_for_bq) > 0:
        logging.info("Deleting bigquery dataset...")
        parent_dataset = o_yaml.get_dataset_name()
        o_datamanager.refresh_connection()
        o_datamanager.delete_bigquery_dataset(dataset=parent_dataset)
    
        logging.info("Finished with bigquery dataset")
    

    logging.info("All done")


if __name__ == '__main__':
    main()
