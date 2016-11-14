from testutils.random_generators import random_lower_alphabetic_str
from deploy_config import DeployConfig
import configuration_deployment as CONFIG_DEPLOY

import datetime
import argparse
import logging
import pprint
import os
import tempfile
import re


CLIENTNAME = os.getenv('SERVICE_CLIENTNAME', '_')

BASE_PATHOUT = os.path.join(tempfile.gettempdir(), "-".join([str(datetime.datetime.now().strftime("%Y%m%d%H%M%S")), random_lower_alphabetic_str(5)]))



################################################################################

def arg_parser():
    parser = argparse.ArgumentParser(description='Upload jar to the cloud.')
    parser.add_argument('-v',  '--version',  required=True, type=str, help='Workflow version')
    parser.add_argument('-p',  '--filepath', required=True, type=str, help='Path to taks and workflow files')
    parser.add_argument('-n',  '--name',     required=True, type=str, help='Workflow name')
    parser.add_argument('-e',  '--env',      required=True, type=str, help='Run environment', choices=['local', 'dev', 'sit', 'prd'])
    parser.add_argument('-o', '--output',                  type=str, help='Output directory. Default: {}'.format(BASE_PATHOUT), default=BASE_PATHOUT)
    
    args = parser.parse_args()
    return vars(args)

################################################################################

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s -- %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def read_file(filein=None):
    with open(filein) as f:
        data = f.read()
        f.close()
    return data

def replace_placeholder_with_value(data=None, kv=None):
    for pname, pvalue in kv.iteritems():
        data = re.sub(pname, pvalue, data)
    return data

def write_file(fileout=None, data=None):
    with open(fileout, 'w') as f:
        f.write(data)
        f.close()

def list_files_in_dir(dname=None):
    files = []
    for root, directories, filenames in os.walk(dname):
        for filename in filenames:
            files.append(os.path.join(root,filename))
    return files

def list_pipeline_files(path=None):
    files = []
    for d in ['query', 'task', 'workflow']:
        for f in list_files_in_dir(os.path.join(path, d)):
            bname = os.path.basename(f)
            files.append({"type": d,
                          "name": bname,
                          "source": bname,
                          "target": bname})
    return files


def main():
    ## validate input
    cmdargs = arg_parser()
    logging.info("Validating arguments...")
    runenv = cmdargs['env']
    base_pathout = cmdargs['output']
    workflow_version = cmdargs['version']
    workflow_filepath = cmdargs['filepath']
    workflow_name = cmdargs['name']
    
    o_config = DeployConfig(env=runenv, config=CONFIG_DEPLOY.CONFIG)
    
    ### listing task and workflow files    
    logging.info("Reading tasks and workflows config files from directory...")
    qm_tasks = list_pipeline_files(workflow_filepath)
     
    ## preparing tasks and workflows    
    logging.info("Preparing tasks and workflows...")
    for d_task in qm_tasks:
        pathin  = os.path.join(workflow_filepath, d_task["type"])
        pathout = os.path.join(base_pathout, d_task["type"])
        if not os.path.exists(pathout):
            os.makedirs(pathout)
            logging.info("  Created task folder {}".format(pathout))
    
        logging.info("    Doing {} - {}".format(d_task["type"], d_task["name"]))
        fin  = os.path.join(pathin,  d_task["source"])
        fout = os.path.join(pathout, d_task["target"])
        
        task_info = read_file(fin)
        task_info = replace_placeholder_with_value(data=task_info,
                                                   kv={"__WORKFLOW_NAME__": workflow_name,
                                                       "__WORKFLOW_VERSION__": workflow_version,
                                                       "__CLIENT_NAME__": CLIENTNAME})
        
        if "replace" in d_task:
            task_info = replace_placeholder_with_value(data=task_info,
                                                       kv=d_task["replace"])
        if o_config.exists("replace"):
            task_info = replace_placeholder_with_value(data=task_info,
                                                       kv=o_config.get("replace"))
        write_file(fout, task_info)
        
        #pprint.pprint(task_info)
    
    logging.info("All done...")
 

if __name__ == '__main__':
    main()
    
