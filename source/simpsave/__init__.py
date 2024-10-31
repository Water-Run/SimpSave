import sys
import importlib.util

def _path_parser_(path: str) -> str:
    if not path.endswith('.ini'):
        raise NameError(f'Simpsave can only operate .ini file: {path} unsupported.')
    
    if path.startswith('::py?'):
        return sys.exec_prefix + '\\ssdatas\\' + path.replace('::py?', '', 1)
    elif path.startswith('::ss?'):
        sspath = importlib.util.find_spec('simpsave')
        if sspath is not None and sspath.submodule_search_locations:
            return sspath.submodule_search_locations[0] + '\\ssdatas\\' + path.replace('::ss?', '', 1)
        else:
            raise RuntimeError('Can not find the path of simpsave package. Have you installed using pip?')

    return path

path = '::py?example.ini'
print(_path_parser_(path))

#path = '::ss?apc.ini'
#print(_path_parser_(path))
#from .simpsave import ready, clear_ss, init, has, read, write, remove