"""
    
    Web resources:
        
        - API:
            * https://cloud.google.com/storage/docs/json_api/v1/buckets
            * https://cloud.google.com/storage/docs/json_api/v1/objects
            
        - examples:
            * https://www.linkedin.com/pulse/use-python-load-local-files-google-cloud-storage-charles-clifford
        


    DESCRIPTION:
    ------------
    
    Script to transfer all files needed for testing. Test data will be added to GCS and also in some cases
    to BQ. The information about what file/tables to add and where is defined in a yaml file.


    USAGE:
    ------------
    
    user@terminal:/path/to/test/directory$ PYTHONPATH=~/Desktop/ocd_repo/DE-atmosphere/python/lib/src python prepare_dataflow_testdata.py

"""

import argparse
import os
import pprint
import logging
import tempfile
import shutil
import hashlib

from testutils.manage_testdata import YamlManager
from utils.datamanager import DataManager
from utils.fileformat_manager import JsonManager
from config.service_config import ServiceConfig



TEMPDIR = tempfile.mkdtemp()



################################################################################

def arg_parser():
    parser = argparse.ArgumentParser(description='Transfer test data from local disk to cloud.')
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
    clientid = cmdargs['clientid']
    runenv = cmdargs['env']
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
    
    
    ## Reformatting json files to be transferred to gcs
    logging.info("Reformatting json files to be transferred to gcs...")
    files_for_gcs = []
    m = hashlib.md5()
    for f in o_yaml.get_files_for_gcs():
        if 'mode' not in f or f['mode'] != 'sync':
            filepath = f['localpath']
            logging.info("Doing {}...".format(filepath))
            m.update(filepath)
            newpath = '{}/{}'.format(TEMPDIR, m.hexdigest())
            JsonManager.format_to_oneline_json(filein=filepath, fileout=newpath)
            f['localpath'] = newpath
        files_for_gcs.append(f)
    
    #pprint.pprint(files_for_gcs)
    
    
    ### buckets
    parent_bucket = o_yaml.get_bucket_name()
    logging.info("Creating and Populating gcs bucket {}...".format(parent_bucket))
    o_datamanager.delete_storage_bucket(bucket=parent_bucket)
    o_datamanager.create_storage_bucket(bucket=parent_bucket)
    o_datamanager.upload_files_to_bucket(bucket=parent_bucket, files=files_for_gcs)
    logging.info("Finished with gcs bucket")
    
    
    ## managing BQ datasets and tables
    tables_for_bq = o_yaml.get_tables_for_bq()
    if len(tables_for_bq) > 0:
        logging.info("Preparing bigquery dataset...")
        
        parent_dataset = o_yaml.get_dataset_name()
    
        o_datamanager.refresh_connection()
        o_datamanager.delete_bigquery_dataset(dataset=parent_dataset)
        o_datamanager.create_bigquery_dataset(dataset=parent_dataset)
        
        for tbl in tables_for_bq:
            logging.info("Loading {}".format(tbl['tablename']))
            schema = JsonManager.read_raw(filein=tbl['schemafile'])
            
            #pprint.pprint(schema)
            o_datamanager.load_bigquery_table_from_gcs(dataset=parent_dataset, 
                                                       table=tbl['tablename'],
                                                       files=tbl['source'],
                                                       schema=schema)
    
        logging.info("Finished with bigquery dataset")
    
    
    logging.info("Cleaning up")
    shutil.rmtree(TEMPDIR)
    
    logging.info("All done")


if __name__ == '__main__':
    main()
