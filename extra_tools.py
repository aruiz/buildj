import os

from Configure import conf
from Constants import *
import Utils

# Things here should probably go into waf at some point

@conf
def write_config_vapi(self, configfile='', env=''):
	if not configfile: configfile = 'config.vapi'
	if not env: env = self.env

	vapi = '[CCode (cprefix = "", lower_case_cprefix = "", cheader_filename = "config.h")] \n' + \
	       'namespace Config {\n'

	defs = self.env[DEFINES] or Utils.ordered_dict()
	for key in defs.allkeys:
		val = defs[key]
		if isinstance(val, int):
			vapi += "\tpublic const int %s;\n" % key
		else:
			vapi += "\tpublic const string %s;\n" % key

	vapi += '}'

	path = os.sep.join([self.blddir, env.variant(), configfile])
	(dir, base) = os.path.split(path)
	Utils.check_dir(dir)

	dest = open(path, 'w')
	dest.write(vapi)
	env.append_unique(CFG_FILES, configfile)
	dest.close()

	env.append_unique('VALAFLAGS', "--vapidir=%s" % dir)
	env.append_unique('VALAFLAGS', "--pkg=config")

