import datetime
import pprint
import copy
import yaml

        

class YamlManager(object):
    """
        Class to handle test data in YAML format
    """
    def __init__(self, filein=None, abspath=None, env=None, clientid=None):
        self.abspath = abspath
        self.data = self.read_raw(filein=filein)
        self._set_bucket_name(env=env, clientid=clientid)
        self._set_dataset_name(env=env, clientid=clientid)
        self._define_files_for_gcs_and_tables_for_bq()
        
    
    @staticmethod
    def read_raw(filein=None):
        data = {}
        with open(filein) as f:
            data = yaml.load(f)
            f.close()
        return data
        
 
    def _set_bucket_name(self, env=None, clientid=None):
        self.bucket_name = self.data['bucket'].format(env=env, clientid=clientid)
        
 
    def _set_dataset_name(self, env=None, clientid=None):
        self.dataset_name = self.data['dataset'].format(env=env, clientid=clientid)
        
 
    def get_bucket_name(self):
        return self.bucket_name
        
 
    def get_dataset_name(self):
        return self.dataset_name
 
 
    def get_path_to_tests(self):
        return self._format_abs_path(self.data['testpath'])
 
 
    def get_path_to_schemas(self):
        return self._format_abs_path(self.data['schemapath'])
    
    
    def _format_abs_path(self, relpath=None):
        return '{}/{}'.format(self.abspath, relpath)


    def get_files_for_gcs(self):
        return self.files_for_gcs


    def get_tables_for_bq(self):
        return self.tables_for_bq
  
    
    def _define_files_for_gcs_and_tables_for_bq(self):
        files_for_gcs = []
        tables_for_bq = []
        for dfname in self.data['files']:
            for testname in self.data['files'][dfname]:
                for datatype in self.data['files'][dfname][testname]:
                    for dataname in self.data['files'][dfname][testname][datatype]:
                        mode = None
                        if 'mode' in self.data['files'][dfname][testname][datatype][dataname]:
                            mode = self.data['files'][dfname][testname][datatype][dataname]['mode']
                        if mode == 'sync':
                            prefix = ''
                            if 'prefix' in self.data['files'][dfname][testname][datatype][dataname]:
                                if self.data['files'][dfname][testname][datatype][dataname]['prefix']:
                                    prefix = self.data['files'][dfname][testname][datatype][dataname]['prefix'] + '/'
                            for local_filename in self.data['files'][dfname][testname][datatype][dataname]['paths']:
                                localpath = '{}{}/{}/{}'.format(self.get_path_to_tests(), dfname, testname, local_filename)
                                gcs_filename = prefix + local_filename
                                files_for_gcs.append({'localpath' : localpath, 'gcs_filename': gcs_filename, 'mode': mode})
                        else:
                            local_filename = self.data['files'][dfname][testname][datatype][dataname]['local']['filepath']
                            localpath = '{}{}/{}/{}'.format(self.get_path_to_tests(), dfname, testname, local_filename)
                            gcs_filename = self.data['files'][dfname][testname][datatype][dataname]['gcs']['filename']
                            files_for_gcs.append({'localpath' : localpath, 'gcs_filename': gcs_filename})

                            if 'bq' in self.data['files'][dfname][testname][datatype][dataname]:
                                 tables_for_bq.append({'tablename': self.data['files'][dfname][testname][datatype][dataname]['bq']['tablename'],
                                                      'source': 'gs://{}/{}'.format(self.get_bucket_name(),
                                                                                    gcs_filename),
                                                      'schemafile': '{}{}'.format(self.get_path_to_schemas(),
                                                                                  self.data['files'][dfname][testname][datatype][dataname]['bq']['schema'])})
        self.files_for_gcs = files_for_gcs
        self.tables_for_bq = tables_for_bq

