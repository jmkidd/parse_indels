import sys
import age_parse
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

#print 'doing',options.inFile

res = age_parse.process_align_file(options.inFile)


header, row = age_parse.prepare_row(res)

outFileName = options.inFile + '.parse'
#print 'writing to',outFileName
outFile = open(outFileName,'w')
nl = '\t'.join(header) + '\n'
outFile.write(nl)
row = [str(j) for j in row]
nl = '\t'.join(row) + '\n'
outFile.write(nl)
outFile.close()


