import json
import pprint
import copy
import yaml
import ast
import re

class SqlManager(object):
    """
        Class to handle data in SQL format
    """
    @classmethod
    def read_sql(cls, filein=None):
        datain = cls.read_raw(filein=filein)
        return cls._prepare_sql(basesql=datain)


    @classmethod
    def _prepare_sql(cls, basesql=None):
        sql = cls._remove_sql_comments(basesql=basesql)
        #return cls._format_sql(basesql=sql)
        return sql

    @staticmethod
    def read_raw(filein=None):
        data = []
        with open(filein) as f:
            data = f.read()
            f.close()
        return data


    @staticmethod
    def _remove_sql_comments(basesql=None):
        rgx = re.compile(r'^\s*--')
        sql = []
        for frag in basesql.split('\n'):
            if not rgx.search(frag):
                sql.append(frag)
        return ('\n').join(sql)


    @staticmethod
    def _format_sql(basesql=None):
        sql = basesql.replace('\n', ' ').replace('\r', '')
        return re.sub('\s+', ' ', sql).strip()


    @classmethod
    def pipe_words_for_regex(cls, words=None):
        return cls.join_words(words=words, separator='|')


    @staticmethod
    def join_words(words=None, separator=','):
        return separator.join(words)
    


class JsonManager(object):
    """
        Class to handle data in JSON format
    """
    @classmethod
    def read_json(cls, filein=None):
        datain = cls.read_raw(filein=filein)
        return cls._remove_comments(data=datain)
        

    @classmethod
    def format_to_oneline_json(cls, filein=None, fileout=None):
        no_comments = cls.read_json(filein=filein)
        cls.write_formatted(data=no_comments, fileout=fileout)
        

    @staticmethod
    def read_raw(filein=None):
        data = []
        with open(filein) as f:
            data = ast.literal_eval(f.read())
            f.close()
        return data
        
 
    @staticmethod
    def write_formatted(data=None, fileout=None):
        with open(fileout, 'w') as f:
            for row in data:
                f.write(json.dumps(row) + '\n')
            f.close()
        
 
    @staticmethod
    def _remove_comments(data=None):
        out = []
        for row in data:
            r = copy.deepcopy(row)
            if '_comment' in r:
                del r['_comment']
            out.append(r)
        return out


class OneLineJsonManager(object):
    """
        Class to handle data in file in which each line is a JSON object
    """
    @classmethod
    def read_one_line_json(cls, filein=None):
        data = []
        with open(filein) as f:
            for line in cls.nonblank_lines(f.readlines()):
                data.append(json.loads(line))
            f.close()
        return data

    @staticmethod
    def nonblank_lines(f):
        for l in f:
            line = l.rstrip()
            if line:
                yield line

