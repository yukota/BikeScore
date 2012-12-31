# -*- coding: utf-8 -*-
'''
Created on 2012/07/25
Test for BikeScore class
@author: YuK_Ota
'''

import sys, os
sys.path.append(os.pardir + "/src")
import BikeScore

import unittest
import datetime
import time
import matplotlib.pyplot as plot
import csv
import math

class TestBikeScore(unittest.TestCase):


#    def setUp(self):
#        pass

#    def tearDown(self):
        # pass

    def testInit(self):
        '''
        データセットの作成
        PowerSample.csvの計測結果
        CP262W
        xPower217W
        AvePower152W
        BikeScore133
        '''

        # ヘッダ
        # Minutes:0
        # Watts:4
        SAMPLE_DATA = "./resources/PowerSample.csv"
        CRITICAL_POWER = 262
        csvfile = open(SAMPLE_DATA, "rb")
        dialect = csv.Sniffer().sniff((csvfile.read()))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        dataset = []
        for i in reader:
            try:
                minOrd = float(i[0])
                imin = int(math.floor(minOrd))
                isec = int((minOrd - imin) * 60)
                imsec = int(minOrd - imin - isec / 60)
                date = datetime.datetime(2012, 1, 1, 0, imin, isec, imsec)
                dataset.append((date, i[1]))
            except ValueError:
                pass

        # test
        bikeScore = BikeScore.BikeScore(dataset, CRITICAL_POWER)
        xPower = bikeScore.getXPower()
        # xPower217
        self.assertLessEqual(xPower / 217, 1.2)
        self.assertGreaterEqual(xPower / 217, 0.8)
        resultBikeScore = bikeScore.getBikeScore()
        # BikeScore133
        self.assertLessEqual(resultBikeScore / 133, 1.2)
        self.assertGreaterEqual(resultBikeScore / 133, 0.8)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
