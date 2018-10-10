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
def coords_to_parts(coords):
    coords = coords.replace('[','')
    coords = coords.replace(']','')
    coords = coords.split(',')
    coords[0] = int(coords[0])
    coords[1] = int(coords[1])
    return coords
########################################################################################
def process_align_file(fileName):
    res = {}
    res['fileName'] = fileName
    res['fileNamePart'] = fileName.split('/')[-1]
    
    fileLines = []
    inFile = open(fileName,'r')
    for line in inFile:
        line = line.rstrip()
        line = line.replace('\'','')
        line = line.split()
        fileLines.append(line)
    inFile.close()
#    print 'read %i lines' % len(fileLines)

    # get info on the seqs
    seqInfo = fileLines[3]
    if seqInfo[0] != 'First':
        print 'not first'
        sys.exit()
    res['seq1Name'] = seqInfo[6]
    coords = seqInfo[2]
    coords  = coords_to_parts(coords)
    res['seq1Dir'] = seqInfo[3]
    res['seq1Start'] = coords[0]
    res['seq1End'] = coords[1]
    
    seqInfo = fileLines[4]
    if seqInfo[0] != 'Second':
        print 'not first'
        sys.exit()
    res['seq2Name'] = seqInfo[6]
    coords = seqInfo[2]
    coords  = coords_to_parts(coords)
    res['seq2Dir'] = seqInfo[3]
    res['seq2Start'] = coords[0]
    res['seq2End'] = coords[1]

    
    # get the align info
    if fileLines[11][0] != 'Alignment:':
         print 'no align?'
         print fileLines[11]
         sys.exit()
    
    align = fileLines[12]
    res['align'] = {}
    res['align']['s1Dir'] = align[2]
    coords = align[3]
    coords  = coords_to_parts(coords)
    res['align']['s1Left'] = coords
    coords = align[6]
    coords  = coords_to_parts(coords)
    res['align']['s1Right'] = coords

    align = fileLines[13]
    res['align']['s2Dir'] = align[2]
    coords = align[3]
    coords  = coords_to_parts(coords)
    res['align']['s2Left'] = coords
    coords = align[6]
    coords  = coords_to_parts(coords)
    res['align']['s2Right'] = coords

    # get the excised regions info
    if fileLines[15][0] != 'EXCISED':
         print 'no excised?'
         print fileLines[15]
         sys.exit()
    
    res['excised'] = {}
    excised = fileLines[16]
    res['excised']['s1Dir'] = excised[2]
    el = int(excised[3])
    res['excised']['s1Len'] = el
    if el == 0:
        res['excised']['s1Coords'] = [0,0]
    else:
        coords = excised[5]
        coords  = coords_to_parts(coords)
        res['excised']['s1Coords'] = coords
    excised = fileLines[17]
    res['excised']['s2Dir'] = excised[2]
    el = int(excised[3])
    res['excised']['s2Len'] = el
    if el == 0:
        res['excised']['s2Coords'] = [0,0]
    else:
        coords = excised[5]
        coords  = coords_to_parts(coords)
        res['excised']['s2Coords'] = coords
        
        
    # identity at breakpoints
    res['IDat'] = {}
    id = fileLines[19]
    if id[1] != 'at':
         print 'no at?'
         print id
         print res['fileName']
         sys.exit()

    id = fileLines[20]
    res['IDat']['s1Dir'] = id[2]     
    el = int(id[3])
    res['IDat']['s1Len'] = el
    if el == 0:
        res['IDat']['s1Coords'] = [[0,0],[0,0]]
    else:
        c1 = id[5]
        c2 = id[7]
        c1 = coords_to_parts(c1)
        c2 = coords_to_parts(c2)
        res['IDat']['s1Coords'] = [c1,c2]

    id = fileLines[21]
    res['IDat']['s2Dir'] = id[2]     
    el = int(id[3])
    res['IDat']['s2Len'] = el
    if el == 0:
        res['IDat']['s2Coords'] = [[0,0],[0,0]]
    else:
        c1 = id[5]
        c2 = id[7]
        c1 = coords_to_parts(c1)
        c2 = coords_to_parts(c2)
        res['IDat']['s2Coords'] = [c1,c2]
    
    
    # identity outside breakpoints
    res['IDout'] = {}
    id = fileLines[22]
    if id[1] != 'outside':
         print 'no outside?'
         print id
         sys.exit()

    id = fileLines[23]
    res['IDout']['s1Dir'] = id[2]     
    el = int(id[3])
    res['IDout']['s1Len'] = el
    if el == 0:
        res['IDout']['s1Coords'] = [[0,0],[0,0]]
    else:
        c1 = id[5]
        c2 = id[7]
        c1 = coords_to_parts(c1)
        c2 = coords_to_parts(c2)
        res['IDout']['s1Coords'] = [c1,c2]

    id = fileLines[24]
    res['IDout']['s2Dir'] = id[2]     
    el = int(id[3])        
    res['IDout']['s2Len'] = el
    if el == 0:
        res['IDout']['s2Coords'] = [[0,0],[0,0]]
    else:
        c1 = id[5]
        c2 = id[7]
        c1 = coords_to_parts(c1)
        c2 = coords_to_parts(c2)
        res['IDout']['s2Coords'] = [c1,c2]
    
    # identity inside breakpoints
    res['IDin'] = {}
    id = fileLines[25]
    if id[1] != 'inside':
         print 'no inside?'
         print id
         sys.exit()

    id = fileLines[26]
    res['IDin']['s1Dir'] = id[2]     
    el = int(id[3])
    res['IDin']['s1Len'] = el
    if el == 0:
        res['IDin']['s1Coords'] = [[0,0],[0,0]]
    else:
        c1 = id[5]
        c2 = id[7]
        c1 = coords_to_parts(c1)
        c2 = coords_to_parts(c2)
        res['IDin']['s1Coords'] = [c1,c2]

    id = fileLines[27]
    res['IDin']['s2Dir'] = id[2]     
    el = int(id[3])
    res['IDin']['s2Len'] = el
    if el == 0:
        res['IDin']['s2Coords'] = [[0,0],[0,0]]
    else:
        c1 = id[5]
        c2 = id[7]
        c1 = coords_to_parts(c1)
        c2 = coords_to_parts(c2)
        res['IDin']['s2Coords'] = [c1,c2]
    return res
########################################################################################
def prepare_row(res):
    header = []
    row = []
    
    header.append('fileName')
    row.append(res['fileNamePart'])
    
    header.extend(['seq1Name','seq1Dir','seq1Start','seq1End'])
    row.extend([res['seq1Name'],res['seq1Dir'],res['seq1Start'],res['seq1End']])


    header.extend(['seq2Name','seq2Dir','seq2Start','seq2End'])
    row.extend([res['seq2Name'],res['seq2Dir'],res['seq2Start'],res['seq2End']])
    
    header.extend(['s1AlignDir','s1AlignLeftStart','s1AlignLeftEnd','s1AlignRightStart','s1AlignRightEnd'])    
    row.extend([res['align']['s1Dir'],res['align']['s1Left'][0],res['align']['s1Left'][1],res['align']['s1Right'][0],res['align']['s1Right'][1]])

    header.extend(['s2AlignDir','s2AlignLeftStart','s2AlignLeftEnd','s2AlignRightStart','s2AlignRightEnd'])    
    row.extend([res['align']['s2Dir'],res['align']['s2Left'][0],res['align']['s2Left'][1],res['align']['s2Right'][0],res['align']['s2Right'][1]])
    
    header.extend(['s1ExcisedDir','s1ExcisedLen','s1ExcisedStart','s1ExcisedEnd'])
    row.extend([res['excised']['s1Dir'],res['excised']['s1Len'],res['excised']['s1Coords'][0],res['excised']['s1Coords'][1]])

    header.extend(['s2ExcisedDir','s2ExcisedLen','s2ExcisedStart','s2ExcisedEnd'])
    row.extend([res['excised']['s2Dir'],res['excised']['s2Len'],res['excised']['s2Coords'][0],res['excised']['s2Coords'][1]])

    header.extend(['s1IDAtLen','s1IDAtStart','s1IDAtEnd'])
    a = [str(j) for j in res['IDat']['s1Coords'][0]]
    a = '-'.join(a)
    b = [str(j) for j in res['IDat']['s1Coords'][1]]
    b = '-'.join(b)    
    row.extend([res['IDat']['s1Len'],a,b])

    header.extend(['s2IDAtLen','s2IDAtStart','s2IDAtEnd'])
    a = [str(j) for j in res['IDat']['s2Coords'][0]]
    a = '-'.join(a)
    b = [str(j) for j in res['IDat']['s2Coords'][1]]
    b = '-'.join(b)
    row.extend([res['IDat']['s2Len'],a,b])


    header.extend(['s1IDOutLen','s1IDOutStart','s1IDOutEnd'])
    a = [str(j) for j in res['IDout']['s1Coords'][0]]
    a = '-'.join(a)
    b = [str(j) for j in res['IDout']['s1Coords'][1]]
    b = '-'.join(b)    
    row.extend([res['IDout']['s1Len'],a,b])

    header.extend(['s2IDOutLen','s2IDOutStart','s2IDOutEnd'])
    a = [str(j) for j in res['IDout']['s2Coords'][0]]
    a = '-'.join(a)
    b = [str(j) for j in res['IDout']['s2Coords'][1]]
    b = '-'.join(b)
    row.extend([res['IDout']['s2Len'],a,b])


    header.extend(['s1IDInLen','s1IDInStart','s1IDInEnd'])
    a = [str(j) for j in res['IDin']['s1Coords'][0]]
    a = '-'.join(a)
    b = [str(j) for j in res['IDin']['s1Coords'][1]]
    b = '-'.join(b)    
    row.extend([res['IDin']['s1Len'],a,b])

    header.extend(['s2IDInLen','s2IDInStart','s2IDinEnd'])
    a = [str(j) for j in res['IDin']['s2Coords'][0]]
    a = '-'.join(a)
    b = [str(j) for j in res['IDin']['s2Coords'][1]]
    b = '-'.join(b)
    row.extend([res['IDin']['s2Len'],a,b])
        
    return(header,row)

########################################################################################

#print 'doing',options.inFile

res = process_align_file(options.inFile)


header, row = prepare_row(res)

outFileName = options.inFile + '.parse'
#print 'writing to',outFileName
outFile = open(outFileName,'w')
nl = '\t'.join(header) + '\n'
outFile.write(nl)
row = [str(j) for j in row]
nl = '\t'.join(row) + '\n'
outFile.write(nl)
outFile.close()


