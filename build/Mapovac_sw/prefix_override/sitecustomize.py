import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/havlian/Documents/Mapovac_code/install/Mapovac_sw'
