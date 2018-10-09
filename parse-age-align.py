import sys
from optparse import OptionParser




########################################################################################

USAGE = """
python2 parse-age-align.py --in <age align file>

will parse output to file

"""
parser = OptionParser(USAGE)
parser.add_option('--in',dest='inFile', help = 'age align file')


(options, args) = parser.parse_args()


if options.inFile is None:
    parser.error('align in not given')
########################################################################################



print 'doing',options.inFile


