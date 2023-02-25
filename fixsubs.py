import sys
import glob

def parseTime(timestamp):
    '''Parses a subtitle file time stamp into an int'''
    hours = timestamp[:2]
    minutes = timestamp[3:5]
    seconds = timestamp[6:12]

    time = 0

    time += int(hours)*60*60*1000
    time += int(minutes)*60*1000
    time += int(seconds.replace(',',''))

    time = int(time)
    time -= int(sys.argv[2])

    h = time // 60 // 60 // 1000 
    m = time // 60 // 1000 % 60
    s = time - (h*60*60*1000) - (m*60*1000)

    ts = 0

    h = str(h)
    m = str(m)
    s = str(s)

    if len(h) == 1:
        h = "0"+h
    if len(m) == 1:
        m = "0"+m
    if len(s) < 5:
        numzeros = 5 -len(s)
        i=0
        s2 = ""
        while i < numzeros:
            s2 +='0'
            i += 1
        s2 += s
        s = s2  

    ts=h + ':' + m + ":" + s[:2] + "," + s[2:]

    return ts

subfile = open(''.join(glob.glob("og/"+sys.argv[1])), 'r', encoding="utf-8")
outfile = open("out/"+''.join(glob.glob("og/"+sys.argv[1]))[2:], 'w', encoding='utf-8')

data = subfile.readlines()

i = 1
curline = 1
edit_flag = False

for line in data:
    if edit_flag:
        ts1, ts2 = line[:12], line[17:]

        ts1 = parseTime(ts1)
        ts2 = parseTime(ts2)

        tsstr = ts1 + " --> " + ts2 + '\n'
        outfile.write(tsstr)

        edit_flag=False

    else:
        outfile.write(line)
        if line.rstrip() == str(curline):
            curline += 1
            edit_flag=True
    i += 1

subfile.close()
outfile.close()