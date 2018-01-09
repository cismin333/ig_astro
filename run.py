#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ___        InstaBot V 1.2.0 by Trevor                 ___
# ___        Mengotomatiskan aktivitas Instagram Anda   ___

# ___        Copyright 2018 by Trevor            ___

# ___Perangkat lunak ini dilisensikan di bawah Apache 2___
# ___lisensi. Anda mungkin tidak menggunakan file ini  ___
# ___ kecuali sesuai dengan licensi anda               ___



from src.instabot import InstaBot
from src.instaprofile import InstaProfile
import json

def parse_config(path):
    # parses config file to load parameters
    
    try:
        raw = [line.strip() for line in open(path, 'r')]
        return json.loads(''.join(raw))
    except:
        print 'Could not open config file, check parameters.'

def main():
    # main operations

    data = parse_config('config.json')
    profile = InstaProfile(path='cache/', params=data)
    instabot = InstaBot(profile, data = data)
    instabot.main()

if __name__ == '__main__':
    main()
