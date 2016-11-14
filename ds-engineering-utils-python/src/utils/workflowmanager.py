import re
import time

from fileformat_manager import JsonManager
from utils.fileformat_manager import SqlManager

DELAY = 5

class WorkflowManager(object):
    task_types = {
        'BQ_SQL'    : '_task_bq_sql',
        'SPARK_JOB' : '_task_spark_job',
        'GCS_TO_BQ' : '_task_gcs_to_bq',
        'BQ_TO_GCS' : '_task_bq_to_gcs',
    }

    def __init__(self, datamanager=None):
        self.datamanager = datamanager

    def run_workflow(self, workflow_steps=None, delay=DELAY):
        for task in workflow_steps:
            self.run_task(task)
            time.sleep(delay)


    def run_task(self, task=None):
        task_type = task['TASK_TYPE'] 
        if task_type in self.task_types:
            method = getattr(self, self.task_types[task_type])
            return method(task['TASK_INFO'])
        else:
            raise NotImplementedError('There is no method implemented for task type: {}'.format(task_type))


    def _task_bq_sql(self, task_info=None):
        fieldnames = ['SQL_FILE', 'TARGET_DATASET', 'TARGET_TABLE', 'SQL_PARAMS']
        if (    isinstance(task_info, dict)
            and all(fld in task_info for fld in fieldnames)
            and isinstance(task_info['SQL_PARAMS'], dict)
        ):
            ## read SQL from file
            basesql = SqlManager.read_sql(task_info['SQL_FILE'])
            
            ## replace jinja variables by their values
            for pname, pvalue in task_info['SQL_PARAMS'].iteritems():
                basesql = re.sub(pname, pvalue, basesql)
                
            ## run query
            self.datamanager.save_query_results_to_bigquery_table(destination_table=task_info['TARGET_TABLE'],
                                                                  destination_dataset=task_info['TARGET_DATASET'],
                                                                  query=basesql)
        else:
            raise TypeError("Invalid input data")


    def _task_bq_to_gcs(self, task_info=None):
        fieldnames = ['IS_COMPRESSED', 'SOURCE_DATASET', 'SOURCE_TABLE',
                      'DESTINATION_BUCKET', 'DESTINATION_FOLDER', 'FILE_FORMAT']
        if (    isinstance(task_info, dict)
            and all(fld in task_info for fld in fieldnames)
        ):
            self.datamanager.download_bigquery_table_to_gcs(source_table=task_info['SOURCE_TABLE'],
                                                            source_dataset=task_info['SOURCE_DATASET'],
                                                            destination_bucket=task_info['DESTINATION_BUCKET'],
                                                            destination_folder=task_info['DESTINATION_FOLDER'],
                                                            is_compressed=task_info['IS_COMPRESSED'],
                                                            file_format=task_info['FILE_FORMAT'])
        else:
            raise TypeError("Invalid input data")


    def _task_gcs_to_bq(self, task_info=None):
        fieldnames = ['GCS_FILES', 'TARGET_DATASET', 'TARGET_TABLE', 'SCHEMA_FILE', 'FILE_FORMAT']
        if (    isinstance(task_info, dict)
            and all(fld in task_info for fld in fieldnames)
        ):
            ## read schema from file
            schema = JsonManager.read_raw(filein=task_info['SCHEMA_FILE'])
            
            ## load files
            self.datamanager.load_bigquery_table_from_gcs(dataset=task_info['TARGET_DATASET'],
                                                          table=task_info['TARGET_TABLE'],
                                                          files=task_info['GCS_FILES'],
                                                          schema=schema,
                                                          file_format=task_info['FILE_FORMAT'])
        else:
            raise TypeError("Invalid input data")


    def _task_spark_job(self, task_info=None):
        fieldnames = ['JAR_FILE_URIS', 'MAIN_CLASS', 'PROPERTIES', 'ARGS', 'CLUSTER_NAME'] 
        if (    isinstance(task_info, dict)
            and all(fld in task_info for fld in fieldnames)
        ):
            self.datamanager.run_spark_job(jar_file_uris=task_info['JAR_FILE_URIS'],
                                           main_class=task_info['MAIN_CLASS'],
                                           args=task_info['ARGS'],
                                           properties=task_info['PROPERTIES'],
                                           cluster_name=task_info['CLUSTER_NAME'])
        else:
            raise TypeError("Invalid input data")
