import re
import cProfile
cProfile.run('re.compile("foo|bar")', 'restats')