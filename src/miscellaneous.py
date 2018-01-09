#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ___        InstaBot V 1.2.0 by Trevor                 ___
# ___        Mengotomatiskan aktivitas Instagram Anda   ___

# ___        Copyright 2018 by Trevor            ___

# ___Perangkat lunak ini dilisensikan di bawah Apache 2___
# ___lisensi. Anda mungkin tidak menggunakan file ini  ___
# ___ kecuali sesuai dengan licensi anda               ___



from lxml import etree
import json, itertools, socket
import numpy as np

def internet_connection(host = '8.8.8.8', port = 53, timeout = 3):  
    # check for internet connection
    
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

def return_random_sequence(data, time_in_day):
    # generates random delay values that add up to time in day
                    
    if data == 0:
        return [0]
    random_values = np.random.random(data)
    random_values /= random_values.sum()
    return [int(i*time_in_day) for i in random_values]
