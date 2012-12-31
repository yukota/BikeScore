# -*- coding: utf-8 -*-
'''
Created on 2012/07/25
Test for CriticalPower class
@author: YuK_Ota
'''

import sys, os
sys.path.append(os.pardir + "/src")
import BikeScore

import unittest
import datetime
import time

class TestCriticalPower(unittest.TestCase):

#    def setUp(self):
#        pass

#    def tearDown(self):
        #pass

    def testInitThoretical1(self):
        '''
        initTest
        最小二乗法のテスト
        理論値を使用
        '''
        dataset = [(0, 0), (1, 1)]
        #test
        cp = BikeScore.CriticalPower(dataset)
        self.assertEqual(cp.getCP(), 1, "This is 1")

    def testInitThoretical2(self):
        '''
        initTest
        最小二乗法のテスト
        理論値を使用
        '''
        dataset = [(0, 0), (1, 2)]
        testplot = []
        for test in dataset:
            testplot.append(test[1])

        cp = BikeScore.CriticalPower(dataset)
        self.assertEqual(cp.getCP(), 2, "This is 2")

    def testInitReal(self):
        '''
        initTest
        最小二乗法のテスト
        実測値使用
        '''
        dataset = [(60, 516), (360, 1881), (720, 3218)]
        cp = BikeScore.CriticalPower(dataset)
        self.assertAlmostEqual(cp.getCP(), 4.1, places=1)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
