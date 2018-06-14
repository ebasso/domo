import os

def formatKMBGT(B, fill=' ', align='>', width=0):
    sout = ''
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2)  # 1,048,576
    GB = float(KB ** 3)  # 1,073,741,824
    TB = float(KB ** 4)  # 1,099,511,627,776
    if B < KB:
        sout = '{0} {1}'.format(B, 'Bytes' if 0 == B > 1 else 'Byte')
    elif KB <= B < MB:
        sout = '{0:.2f}KB'.format(B / KB)
    elif MB <= B < GB:
        sout = '{0:.2f}MB'.format(B / MB)
    elif GB <= B < TB:
        sout = '{0:.2f}GB'.format(B / GB)
    elif TB <= B:
        sout = '{0:.2f}TB'.format(B / TB)
    sout = '{message:{fill}{align}{width}}'.format(message=sout, fill=fill, align=align, width=width)
    return sout

def formatPercent(B, fill=' ', align='>', width=0):
    B = float(B)
    sout = '{0:.2f}'.format(B)
    sout = '{message:{fill}{align}{width}}'.format(message=sout, fill=fill, align=align, width=width)
    return sout

def formatPercentFloat(B, fill=' ', align='>', width=0):
    B = float(B)
    sout = '{0:.2f}'.format(B)
    sout = '{message:{fill}{align}{width}}'.format(message=sout, fill=fill, align=align, width=width)
    return float(sout)