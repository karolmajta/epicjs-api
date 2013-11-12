'''
Created on 11 lis 2013

@author: karol
'''
from flask.ext import restful  # @UnresolvedImport

class CorsResource(restful.Resource):
    
    methods = ['HEAD', 'OPTIONS', 'GET', 'POST']
    headers = ['X-Requested-With', 'Accept']
    origins = ['*']
    
    def options(self, *args, **kwargs):
        return {}, 200, self.build_cors_headers()
    
    def get(self, *args, **kwargs):
        retval = self.retrieve(*args, **kwargs)
        cleaned_retval = self.clean_retval(retval)
        cleaned_retval[2].update(self.build_cors_headers())
        return cleaned_retval
    
    def post(self, *args, **kwargs):
        retval = self.create(*args, **kwargs)
        cleaned_retval = self.clean_retval(retval)
        cleaned_retval[2].update(self.build_cors_headers())
        return cleaned_retval
    
    def destroy(self, *args, **kwargs):
        retval = self.destroy(*args, **kwargs)
        cleaned_retval = self.clean_retval(retval)
        cleaned_retval[2].update(self.build_cors_headers())
        return cleaned_retval
    
    def build_cors_headers(self):
        methods = self.lst_to_header(self.__class__.methods, "", str.upper)
        headers = self.lst_to_header(self.__class__.headers, "", str.lower)
        origins = self.lst_to_header(self.__class__.origins, "*", str.lower)
        return {
            'Access-Control-Allow-Headers': headers,
            'Access-Control-Allow-Methods': methods,
            'Access-Control-Allow-Origin': origins
        }
    
    def lst_to_header(self, lst, defval="", transformation=lambda x: x):
        if lst is None: return defval
        elif len(lst) == 0: return ""
        elif len(lst) == 1: return lst[0]
        else: return ", ".join([o.lower() for o in lst])
    
    def clean_retval(self, retval):
        if isinstance(retval, dict):
            return retval, 200, {}
        elif len(retval) == 1:
            return retval, 200, {}
        elif len(retval) == 2:
            return retval[0], retval[1], {}
        else:
            return retval 