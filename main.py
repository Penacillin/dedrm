import os, sys
import unittest.mock as mock
def add_to_path(p):
    if p not in sys.path:
        sys.path.insert(0, p)
dedrm_tools = os.path.abspath('./DeDRM_tools/DeDRM_plugin')
add_to_path(dedrm_tools)

sys.modules.update({
    'calibre.customize': mock.MagicMock(),
    'calibre.constants': mock.MagicMock(),
    'calibre.gui2': mock.MagicMock(),
    'calibre.utils.config': mock.MagicMock(),
})
import DeDRM_tools.DeDRM_plugin as dedrm_plugin

import DeDRM_tools.DeDRM_plugin.zipfix as zipfix
sys.modules.update({
    'calibre_plugins': mock.MagicMock(),
    'calibre_plugins.dedrm': dedrm_plugin,
    'calibre_plugins.dedrm.zipfix': zipfix,
    'zipfix': zipfix,
})
from dedrm import decryptepub

# TODO: Figure out if this is possible
# from DeDRM_tools.DeDRM_plugin.scriptinterface import decryptepub

import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True, help='Input file (.epub)')
    parser.add_argument('-O', '--output-dir', required=True, help='Output Directory')
    parser.add_argument('-k', '--key', required=True, help='Directory with key in it (.der)')
    args = parser.parse_args()

    decryptepub(args.input, args.output_dir, args.key)
