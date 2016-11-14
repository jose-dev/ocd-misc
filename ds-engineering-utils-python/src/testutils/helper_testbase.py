from random import randint, choice, random
import string
import unittest
import os
import re

from testutils.random_generators import random_lower_alphabetic_str
from utils.datamanager import DataManager
from utils.workflowmanager import WorkflowManager
from utils.fileformat_manager import SqlManager
from config.service_config import ServiceConfig


RUNENV = os.getenv('E2E_TEST_ENV', 'local')
CLUSTER_NAME  = 'test-cluster-{}-{}'.format(random_lower_alphabetic_str(5),
                                            random_lower_alphabetic_str(5))

o_servconfig  = ServiceConfig(env=RUNENV, auth='sa')
o_datamanager = DataManager(project_number=o_servconfig.project_number,
                            project_id=o_servconfig.project_id,
                            account_email=o_servconfig.service_account_email,
                            account_p12=o_servconfig.service_account_p12)



class HelperTestBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(HelperTestBase, self).__init__(*args, **kwargs)

        self.project_number  = o_servconfig.project_number
        self.project_id      = o_servconfig.project_id
        self.datamanager     = o_datamanager
        self.workflowmanager = WorkflowManager(o_datamanager)


    def full_bq_tablename(self, project=None, dataset=None, table=None):
        return project + ':' + dataset + '.' + table


    def parse_bq_tablename(self, full_name=None):
        if all(c in full_name for c in [':', '.']):
            project, short_table = full_name.split(':')
            dataset, table = short_table.split('.')
            return [project, dataset, table]
        else:
            raise ValueError("Invalid input data")
   

    def run_workflow(self, workflow_steps=None):
        self.workflowmanager.run_workflow(workflow_steps=workflow_steps)



class WithClusterHelperTestBase(HelperTestBase):

    def __init__(self, *args, **kwargs):
        super(WithClusterHelperTestBase, self).__init__(*args, **kwargs)
        self.cluster_name = CLUSTER_NAME

    @classmethod
    def setUpClass(cls):
        o_datamanager.create_dataproc_cluster(cluster_name=CLUSTER_NAME)
    
    @classmethod
    def tearDownClass(cls):
        o_datamanager.delete_dataproc_cluster(cluster_name=CLUSTER_NAME)

