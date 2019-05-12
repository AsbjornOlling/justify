""" Code generation script for Mopidy core api functions.
"""

# std lib
from typing import Set
from pathlib import Path

# deps
from requests import post
from pprint import pprint as print
from jinja2 import Template


def get_rpc_methods(rpcurl):
    """ Get JSON of available methods from running
    Mopidy instance, using the JSON RPC via HTTP POST.
    """
    r = post(rpcurl, json={'jsonrpc': '2.0',
                           'id': 0,
                           'method': 'core.describe'})
    assert 200 == r.status_code, f"HTTP {r.status_code} from Mopidy."
    result = r.json()
    methods = result['result']
    return methods


def get_controller_names(methods: dict) -> Set:
    """ Return list of controller names, extracted from
    the 'core.controller.method' format method names.
    """
    # remove 'core.method' format names
    ctrlmethods = filter(lambda x: x.count('.') == 2,
                         methods.keys())
    return {m.split('.')[1] for m in ctrlmethods}


def group_by_controller(methods: dict) -> dict:
    """ Return a dict with methods grouped by controller """
    grouped = {}
    for c in get_controller_names(methods):
        grouped[c] = {m: methods[m] for m in methods.keys() if c in m}
    return grouped


def render_code(name, methods, template, outdir='./code'):
    """ Render code with Jinja2, then write to file. """
    code = template.render(methods=methods)

    assert Path(outdir).is_dir(), f"{outdir} is not a directory."
    with open(f"{name}.py", 'w') as f:
        f.write(code)


if __name__ == '__main__':
    # params (TODO: docopt)
    rpcurl = 'http://localhost:6680/mopidy/rpc'
    tplfile = './controller.tpl'

    methods = get_rpc_methods(rpcurl)
    print(methods)

    grouped = group_by_controller(methods)
    print(grouped)

    # read template
    with open(tplfile) as f:
        tplstr = f.read()
        tpl = Template(tplstr)

    for c in grouped.keys():
        # write to file
        render_code(c, grouped[c], )
