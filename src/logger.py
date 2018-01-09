#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ___        InstaBot V 1.2.0 by Trevor                 ___
# ___        Mengotomatiskan aktivitas Instagram Anda   ___

# ___        Copyright 2018 by Trevor            ___

# ___Perangkat lunak ini dilisensikan di bawah Apache 2___
# ___lisensi. Anda mungkin tidak menggunakan file ini  ___
# ___ kecuali sesuai dengan licensi anda               ___

import arrow
from csv import writer
from os import makedirs, path

class Logger:

    def __init__(self, header, backupUnfollows, bucketUnfollow):
        # initialise the logger variables

        self.path = 'cache/log/'
        self.log_temp = ''
        self.new_line = True
        self.backupUnfollows = backupUnfollows
        self.bucketUnfollow = bucketUnfollow
        self.today = arrow.now().format('DD_MM_YYYY')
        
        if not path.isdir(self.path):
            makedirs(self.path)

        self.init_log_name()

        print header

    def init_log_name(self):
        # change log file name

        self.today = arrow.now().format('DD_MM_YYYY')
        self.log_main = []
        self.log_file = self.path + 'activity_log_' + self.today + '.txt'

    def log(self, string):
        # write to log file

        try:
            if self.today != arrow.now().format('DD_MM_YYYY'):
                self.init_log_name()

            self.backup()

            if string.endswith('\,'):
                log = string.replace('\,', '')
                
                if self.new_line or log.startswith('\n'):
                    if log.startswith('\n'):
                        log = log.replace('\n', '')
                        print '\n',
                    log = arrow.now().format('[ YYYY-MM-DD HH:mm:ss ] ') + log
                print log,

                self.new_line = False
                if self.log_temp:
                    try:
                        self.log_temp += log
                    except:
                        pass
                else:
                    self.log_temp = log
                return

            log = string
            print log
            if self.log_temp:
                string = self.log_temp + string
                self.log_temp = ''
                self.new_line = True

            self.log_main.append([string.strip()])

        except Exception as e:
            print 'Error while logging: %s' %(e)

    def backup(self):
        # backs up the log

        self.backupUnfollows()

        try:
            with open(self.log_file, 'w') as log:
                for line in self.log_main:
                    log.writelines(line)
                    log.write('\n')

        except Exception as e:
            print 'Error backing up: %s' %(e)

        try:
            with open('cache/followlist.csv', 'wb') as backup:
                w = writer(backup)
                w.writerows(self.bucketUnfollow)
        except Exception as e:
            print 'Error while saving backup follow list: %s' %(e)
