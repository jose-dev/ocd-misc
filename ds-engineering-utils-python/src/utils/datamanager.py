import datetime
from time import sleep
import json
import pprint
import os

import httplib2
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.file import Storage


DELAY_SECONDS = 5
NUM_RETRIES   = 5
    

class DataManager(object):
    """
        Base class for all classes that run tests that need management of BQ dataset and tables
    """
    DEFAULT_SCOPES = ['https://www.googleapis.com/auth/monitoring',
                      'https://www.googleapis.com/auth/devstorage.full_control',
                      'https://www.googleapis.com/auth/compute',
                      'https://www.googleapis.com/auth/userinfo.email',
                      'https://www.googleapis.com/auth/bigquery',
                      'https://www.googleapis.com/auth/cloud-platform',
                      'https://www.googleapis.com/auth/logging.read',
                      'https://www.googleapis.com/auth/logging.write',
                      'https://www.googleapis.com/auth/logging.admin']

    def __init__(self, project_number=None, project_id=None, account_secrets=None,
                       redirect_uri=None, dat_file=None, account_p12=None, account_email=None):
        self.project_number  = project_number
        self.project_id      = project_id
        self.account_email   = account_email
        self.account_p12     = account_p12
        self.account_secrets = account_secrets
        self.redirect_uri    = redirect_uri
        self.dat_file        = dat_file
        if account_p12 and account_email:
            self._read_key()
        elif redirect_uri and dat_file and account_secrets:
            self._get_flow()
        else:
            raise ValueError('Invalid input values')
        self._establish_connection()
   

    def _get_flow(self):
        self._flow = flow_from_clientsecrets(self.account_secrets,
                                             scope=" ".join(self.DEFAULT_SCOPES),
                                             redirect_uri=self.redirect_uri)
        self._flow.params['prompt'] = 'consent'


    def _get_credentials(self):
        if self.account_p12:
            credentials = ServiceAccountCredentials.from_p12_keyfile(self.account_email,
                                                                     self.account_p12,
                                                                     scopes=self.DEFAULT_SCOPES)
        else:
            storage = Storage(self.dat_file)
            credentials = storage.get()
            if  credentials is None:
                #step 1
                auth_uri = self._flow.step1_get_authorize_url() 
                print 'Go to the following link in your browser: ' + auth_uri
                code = raw_input('Enter verification code: ').strip()
                #step 2
                credentials = self._flow.step2_exchange(code)
            storage.put(credentials)
        return credentials

    
    def _establish_connection(self):
        self._prepare_storage_service()
        self._prepare_bigquery_service()
        self._prepare_dataproc_service()
   
        
    def refresh_connection(self):
        self._establish_connection()
        

    def _read_key(self):
        with file(self.account_p12, 'rb') as f:
            key = f.read()
            f.close()
            self.key = key
        
 
    def _prepare_service(self, service=None, version=None):
        credentials = self._get_credentials()
        
        http = httplib2.Http()
        http = credentials.authorize(http)
        return build(service, version, http=http)
        
 
    def _prepare_storage_service(self):
        self.storage_service = self._prepare_service(service='storage',
                                                     version='v1')
        
 
    def _prepare_bigquery_service(self):
        self.bigquery_service = self._prepare_service(service='bigquery',
                                                     version='v2')

    def _prepare_dataproc_service(self):
        self.dataproc_service = self._prepare_service(service='dataproc',
                                                     version='v1')
        
 
    def bucket_exists(self, bucket=None):
        response = self.storage_service.buckets().list(project=self.project_number).execute()
        if 'items' in response and bucket in [b['name'] for b in response['items']]:
            return True
        else:
            return False
    
    
    def object_exists(self, bucket=None, prefix=None):
        return self.all_objects_exists(bucket=bucket, prefix=prefix, objects=[prefix])
    
    
    def folder_exists(self, bucket=None, prefix=None):
        response = self.list_all_objects(bucket=bucket, prefix=prefix)
        
        if 'items' not in response or len(response['items']) < 1:
            return False
        return True
    
    
    def all_objects_exists(self, bucket=None, prefix=None, objects=None):
        response = self.list_all_objects(bucket=bucket, prefix=prefix)
        
        if 'items' not in response:
            return False
        
        for obj in objects:
            if obj not in [b['name'] for b in response['items']]:
                return False
            
        return True
    
    
    def list_all_objects(self, bucket=None, prefix=None):
        return self.storage_service.objects().list(bucket=bucket, prefix=prefix).execute()
    
    
    def delete_storage_bucket(self, bucket=None, delay=DELAY_SECONDS):
        """
            Delete gcs bucket
        """
        if self.bucket_exists(bucket=bucket):
            self.empty_storage_bucket(bucket=bucket)
            sleep(delay * 2)
            try:
                result = self.storage_service.buckets().delete(bucket=bucket).execute(num_retries=3)
            except HttpError, e:
                print "Bucket could not be deleted: {}".format(e)
                #raise
        
 
    def list_storage_bucket_content(self, bucket=None):
        """
            List the contents of gcs bucket
        """
        return self.storage_service.objects().list(bucket=bucket).execute()
        
 
    def empty_storage_bucket(self, bucket=None, delay=DELAY_SECONDS):
        """
            Empty gcs bucket
        """
        response = self.list_storage_bucket_content(bucket=bucket)
        if 'items' in response:
            for o in response['items']:
                try:
                    self.storage_service.objects().delete(bucket=bucket, object=o['name']).execute(num_retries=3);
                    sleep(1)
                except HttpError, e:
                    raise
        no_iter = 0
        after = self.list_storage_bucket_content(bucket=bucket)
        while 'items' in after:
            sleep(delay)
            after = self.list_storage_bucket_content(bucket=bucket)
            if no_iter > 5:
                break
            else:
                no_iter += 1
            
            
 
    def delete_storage_buckets(self, buckets=None):
        """
            Delete gcs buckets from a list of names
        """
        for b in buckets:
            self.delete_storage_bucket(bucket=b)
        
 
    def empty_storage_buckets(self, buckets=None):
        """
            Empty gcs buckets from a list of names
        """
        for b in buckets:
            self.empty_storage_bucket(bucket=b)


    def create_storage_bucket(self, bucket=None):
        """
            Create a gcs bucket
        """
        try:
            self.storage_service.buckets().insert(project=self.project_number, body={'name': bucket}).execute()
        except HttpError, e:
            raise


    def create_storage_buckets(self, buckets=None):
        """
            Create gcs buckets from a list of names
        """
        for b in buckets:
            self.create_storage_bucket(bucket=b)


    def upload_file_to_bucket(self, bucket=None, filename=None, localpath=None, filetype='application/json'):
        """
            Upload a file to a given gcs bucket
        """
        media = MediaIoBaseUpload(file(localpath, "r"), filetype, resumable=False)
        try: 
            self.storage_service.objects().insert(bucket=bucket, name=filename, media_body=media).execute()
        except HttpError, e:
            raise


    def download_gcs_bucket_to_localdir(self, bucket=None, localdir=None):
        """
            Download a gcs bucket to local directory
        """
        response = self.list_storage_bucket_content(bucket=bucket)
        if 'items' in response:
            for o in response['items']:
                filename = o['name']
                localpath = os.path.join(localdir, filename)
                self.download_gcs_file_to_localdir(bucket=bucket,
                                                   filename=filename,
                                                   localpath=localpath);


    def download_gcs_file_to_localdir(self, bucket=None, filename=None, localpath=None):
        """
            Download a gcs file to local directory
        """
        f = file(localpath, 'w')
        try:
            request = self.storage_service.objects().get_media(bucket=bucket, object=filename)
            media = MediaIoBaseDownload(f, request)

            done = False
            while not done:
                try:
                    progress, done = media.next_chunk()
                    if progress:
                        print('Download %d%%.' % int(progress.progress() * 100))
                except HttpError, e:
                    raise

        except HttpError, e:
            raise    


    def upload_files_to_bucket(self, bucket=None, files=None):
        """
            Upload several files to a given gcs bucket. The input files is a list of dictionaries with the
            localpath and filename defined.
        """
        for f in files:
            self.upload_file_to_bucket(bucket=bucket,
                                       filename=f['gcs_filename'],
                                       localpath=f['localpath'])

    
    def delete_bigquery_dataset(self, dataset=None):
        """
            Delete bigquery dataset
        """
        response = self.bigquery_service.datasets().list(projectId=self.project_number, maxResults=100).execute()
        if 'datasets' in response and '{}:{}'.format(self.project_id, dataset) in [d['id'] for d in response['datasets']]:
            try:
                print "Deleting {}:{}".format(self.project_number, dataset)
                result = self.bigquery_service.datasets().delete(projectId=self.project_number, datasetId=dataset, deleteContents=True).execute()
            except HttpError, e:
                raise
        
 
    def delete_bigquery_datasets(self, datasets=None):
        """
            Delete bigquery datasets from a list of names
        """
        for d in datasets:
            self.delete_bigquery_dataset(dataset=d)




    def create_bigquery_dataset(self, dataset=None):
        """
            Create a bigquery dataset
        """
        bodyParams = {
            "kind": "bigquery#dataset",
            "datasetReference": {
              "datasetId": dataset,
              "projectId": self.project_number
            },
        }
        try:
            self.bigquery_service.datasets().insert(projectId=self.project_number, body=bodyParams).execute()
        except HttpError, e:
            raise


    def create_bigquery_datasets(self, datasets=None):
        """
            Create bigquery datasets from a list of names
        """
        for d in datasets:
            self.create_bigquery_dataset(dataset=d)


    def _populateJobData(self, dataset=None, table=None, files=None, schema=None, file_format='NEWLINE_DELIMITED_JSON'):
        """
            Prepares the JobData structure required for loading files from GCS
            to BigQuery
        """
        if not isinstance(files, list):
            files = [files]
        return {'projectId': self.project_number,
                'configuration':{
                    'load':{
                        'sourceUris': files,
                        'sourceFormat': file_format,
                        'schema':{ 'fields': schema },
                        'destinationTable':{
                           'projectId': self.project_number,
                           'datasetId': dataset,
                           'tableId': table
                           },
                        'createDisposition':'CREATE_IF_NEEDED',
                        'writeDisposition':'WRITE_TRUNCATE',
                        'encoding':'UTF-8'
                        }
                    }
                }
    
    
    def _wait_for_bigquery_completion(self, jobid=None, delay=DELAY_SECONDS):
        """
            Check the status of a bigquery job and sleep until it has been completed
        """
        try:
            while True:
                status = self.bigquery_service.jobs().get(projectId=self.project_number, jobId=jobid).execute()
                if 'DONE' == status['status']['state']:
                    if 'errors' in status['status']:
                        raise ValueError(pprint.pformat(status, indent=4))
                    break
                sleep(delay)
        except ValueError, e:
            raise
        

    def load_bigquery_table_from_gcs(self, dataset=None, table=None, files=None, schema=None, file_format='NEWLINE_DELIMITED_JSON'):
        """
            Load data into a bigquery table from a gcs file
        """
        jobData = self._populateJobData(dataset=dataset,
                                        table=table,
                                        files=files,
                                        schema=schema,
                                        file_format=file_format)
        try:
            result = self.bigquery_service.jobs().insert(projectId=self.project_number, body=jobData).execute()
            jobid = result['jobReference']['jobId']
            self._wait_for_bigquery_completion(jobid)
        except HttpError, e:
            raise
        

    def execute_bigquery_query(self, query=None):
        """
          Runs a SELECT query against BigQuery and returns a JSON string containing:
            - fields: [...]
            - types:  [...]
            - values: [[..], .., [..]]
        """
        try:
            result = self.bigquery_service.jobs().query(projectId=self.project_number, body={'query':query}).execute(num_retries=NUM_RETRIES)
            dataout = {'fields': [fld['name'] for fld in result['schema']['fields']],
                       'types': [fld['type'] for fld in result['schema']['fields']],
                       'values': []}
            for row in result['rows']:
                vals = []
                for v in row['f']:
                    vals.append(v['v'])
                dataout['values'].append(vals)
            return dataout
        except HttpError, e:
            raise
 

    def copy_bigquery_table(self, source_table=None, destination_table=None, source_dataset=None, destination_dataset=None):
        """
            Copy a bigquery table to another table
        """
        jobData = self._createJobData(source_table=source_table,
                                      destination_table=destination_table,
                                      source_dataset=source_dataset,
                                      destination_dataset=destination_dataset)
        try:
            result = self.bigquery_service.jobs().insert(projectId=self.project_number, body=jobData).execute()
            jobid = result['jobReference']['jobId']
            self._wait_for_bigquery_completion(jobid)
        except HttpError, e:
            raise


    def _createJobData(self, source_table=None, destination_table=None, source_dataset=None, destination_dataset=None):
        """
            Prepares the JobData structure required for copying BQ tables 
        """
        return {'projectId': self.project_number,
                'configuration':{
                    "copy": {
                          "sourceTable": {       
                            "projectId": self.project_number,
                            "datasetId": source_dataset, 
                            "tableId": source_table    
                          },
                          "destinationTable": {  
                            "projectId": self.project_number,
                            "datasetId": destination_dataset, 
                            "tableId": destination_table    
                          },
                          "createDisposition": 'CREATE_IF_NEEDED',  
                          "writeDisposition": 'WRITE_TRUNCATE',   
                        },
                    }
                }


    def save_query_results_to_bigquery_table(self, destination_table=None, destination_dataset=None, query=None):
        """
            Save results from a bigquery query into a table
        """
        jobData = self._createJobDataToLoadByQuery(destination_table=destination_table,
                                                   destination_dataset=destination_dataset,
                                                   query=query)
        try: 
            result = self.bigquery_service.jobs().insert(projectId=self.project_number, body=jobData).execute()
            jobid = result['jobReference']['jobId']
            self._wait_for_bigquery_completion(jobid)
        except HttpError, e:
            raise


    def _createJobDataToLoadByQuery(self, source_table=None, destination_table=None, destination_dataset=None, query=None):
        """
            Prepares the JobData structure required for copying BQ tables 
        """
        return {
                   "projectId": self.project_number,
                   "configuration": {
                       "query": {
                           "query": query, 
                           "destinationTable": {
                               "projectId": self.project_number,
                               "datasetId": destination_dataset,
                               "tableId": destination_table,
                           },
                       "createDisposition": "CREATE_IF_NEEDED",
                       "writeDisposition": "WRITE_TRUNCATE"
                       }
                   }
               }


    def download_bigquery_table_to_gcs(self, source_table=None, source_dataset=None, destination_bucket=None,
                                       destination_folder=None, is_compressed=True, file_format="NEWLINE_DELIMITED_JSON"):
        """
            Save results from a bigquery query into a table
        """
        jobData = self._createJobDataToDownloadQigQueryTable(source_table=source_table,
                                                             source_dataset=source_dataset,
                                                             destination_bucket=destination_bucket,
                                                             destination_folder=destination_folder,
                                                             is_compressed=is_compressed,
                                                             file_format=file_format)
        try: 
            result = self.bigquery_service.jobs().insert(projectId=self.project_number, body=jobData).execute()
            jobid = result['jobReference']['jobId']
            self._wait_for_bigquery_completion(jobid)
        except HttpError, e:
            raise


    def _createJobDataToDownloadQigQueryTable(self, source_table=None, source_dataset=None, destination_bucket=None,
                                              destination_folder=None, is_compressed=True, file_format="NEWLINE_DELIMITED_JSON"):
        """
            Prepares the JobData structure required for downloading BQ tables to GCS as JSON files
        """
        compression = "GZIP" if is_compressed else "NONE"
        file_path = destination_bucket
        if destination_folder:
            file_path += '/' + destination_folder
        file_suffix = 'json'
        if file_format == "CSV":
            file_suffix = "csv"
        if is_compressed:
            file_suffix += '.gz'
        return {
                   "projectId": self.project_number,
                   "configuration": {
                       "extract": {
                           "destinationFormat": file_format,
                           "compression": compression,
                           "destinationUris": ['gs://{}/{}-*.{}'.format(file_path, source_table, file_suffix)],
                           "sourceTable": {
                               "projectId": self.project_number,
                               "datasetId": source_dataset,
                               "tableId": source_table,
                           },
                       }
                   }
               }
    


    def create_dataproc_cluster(self, cluster_name=None,
                                      worker_instance_count=2,
                                      master_machine_type="n1-standard-8",
                                      worker_machine_type="n1-standard-4",
                                      image="1.0",
                                      region="global",
                                      zone="europe-west1-c",
                                      network="hadoop-network",
                                      scopes=None):
        """
            Create cluster
        """
        if not self.cluster_exists(cluster_name=cluster_name, region=region):
            master_configuration = {
                "numInstances": 1,
                "machineTypeUri": "https://www.googleapis.com/compute/v1/projects/%s/zones/%s/machineTypes/%s" % (
                    self.project_id, zone, master_machine_type),
                "diskConfig": {},
                "isPreemptible": False
            }
            worker_configuration = {
                "numInstances": worker_instance_count,
                "machineTypeUri": "https://www.googleapis.com/compute/v1/projects/%s/zones/%s/machineTypes/%s" % (
                    self.project_id, zone, worker_machine_type),
                "diskConfig": {},
                "isPreemptible": False
            }
            description = {
                "projectId": self.project_id,
                "clusterName": cluster_name,
                "config": {
                    "gceClusterConfig": {
                        "zoneUri": "https://www.googleapis.com/compute/v1/projects/%s/zones/%s" % (self.project_id, zone),
                        "networkUri": "https://www.googleapis.com/compute/v1/projects/%s/global/networks/%s" %
                                      (self.project_id, network),
                        "serviceAccountScopes": scopes or self.DEFAULT_SCOPES,
                    },
                    "masterConfig": master_configuration,
                    "workerConfig": worker_configuration,
                    "softwareConfig": {
                        "imageVersion": image
                    }
                }
            }

            try: 
                response = self.dataproc_service.projects().regions().clusters().create(projectId=self.project_id, region=region, body=description).execute()
                self._wait_for_cluster_creation(cluster_name=cluster_name, region=region)
            except HttpError, e:
                raise


    def delete_dataproc_cluster(self, cluster_name=None, region="global"):
        """
            Delete cluster
        """
        if self.cluster_exists(cluster_name=cluster_name, region=region):
            try: 
                response = self.dataproc_service.projects().regions().clusters().delete(projectId=self.project_id, region=region, clusterName=cluster_name).execute()
                self._wait_for_cluster_deletion(cluster_name=cluster_name, region=region)
            except HttpError, e:
                raise


    def cluster_exists(self, cluster_name=None, region="global"):
        """
            Check that cluster exists
        """
        response = self.dataproc_service.projects().regions().clusters().list(projectId=self.project_id, region=region).execute()
        if 'clusters' in response and cluster_name in [b['clusterName'] for b in response['clusters']]:
            return True
        else:
            return False


    def _wait_for_cluster_creation(self, cluster_name=None, region=None, delay=DELAY_SECONDS):
        """
            Check the status of a cluster creation job and sleep until cluster is running
        """
        try:
            while True:
                status = self.dataproc_service.projects().regions().clusters().get(projectId=self.project_id, region=region, clusterName=cluster_name).execute()
                if 'ERROR' == status['status']['state']:
                    raise ValueError(pprint.pformat(status, indent=4))
                    break
                if 'RUNNING' == status['status']['state']:
                    break
                sleep(delay)
        except ValueError, e:
            raise


    def _wait_for_cluster_deletion(self, cluster_name=None, region=None, action=None, delay=DELAY_SECONDS):
        """
            Check the status of a cluster deletion job and sleep until cluster still exists
        """
        try:
            while True:
                if not self.cluster_exists(cluster_name=cluster_name, region=region):
                    break
                sleep(delay)
        except ValueError, e:
            raise


    def run_spark_job(self, jar_file_uris=None, main_class=None, args=None, properties=None, cluster_name=None, region="global"):
        """
            Run spark job
        """
        jobData = self._createJobDataForSpark(jar_file_uris=jar_file_uris,
                                              main_class=main_class,
                                              args=args,
                                              properties=properties,
                                              cluster_name=cluster_name)
        
        try: 
            result = self.dataproc_service.projects().regions().jobs().submit(projectId=self.project_id, region=region, body=jobData).execute()
            jobid = result['reference']['jobId']
            self._wait_for_spark_completion(jobid=jobid, region=region)
        except HttpError, e:
            raise


    def _createJobDataForSpark(self, jar_file_uris=None, main_class=None, args=None, properties=None, cluster_name=None):
        """
            Prepares the JobData for Spark 
        """
        if not properties:
            properties = {}
        return {
                   "job": {
                       "placement": { "clusterName": cluster_name },
                       "sparkJob": {
                           "loggingConfig": {
                               "driverLogLevels": {"com.ocado": "INFO", "root": "FATAL", "org.apache": "INFO"},
                           },
                           "jarFileUris": jar_file_uris,
                           "mainClass": main_class,
                           "properties": properties,
                           "args": args
                       }
                   }
               }

    def _wait_for_spark_completion(self, jobid=None, region=None, delay=DELAY_SECONDS):
        """
            Check the status of a spark job and sleep until it has been completed
        """
        try:
            while True:
                status = self.dataproc_service.projects().regions().jobs().get(projectId=self.project_id, region=region, jobId=jobid).execute()
                if 'ERROR' == status['status']['state']:
                    raise ValueError(pprint.pformat(status, indent=4))
                    break
                if 'DONE' == status['status']['state']:
                    break
                sleep(delay)
        except ValueError, e:
            raise

    

