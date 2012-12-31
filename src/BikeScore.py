# -*- coding: utf-8 -*-
'''
Created on 2012/07/25
@author: YuK_Ota
'''
import numpy
import pandas  # @UnresolvedImport


class BikeScore(object):
    '''
    compute BikeScore and xPower
    '''

    def __init__(self, dataset, cp):
        '''
        Constructor
        dataset=[(datetime.datetime,power)]
        cp CriticalPower
        '''
        self.dataSet = pandas.Series(dataset)
        self.cp = cp
        #Series型に変換する
        sirializeData = dict([(datum[0], datum[1]) for datum in dataset])
        date = sorted(sirializeData.keys())
        power = [sirializeData[key] for key in date]

        self.timePower = pandas.Series(power, index=date)

        (self.smoothTimePower, self.period) = \
            self._ewmaOfTimePower(self.timePower)

        self.xPower = self._computeXPower()
        self.RI = self._computeRelativeIntensity()
        self.normalizedWork = self._computeNormalizedWork()
        self.bikeScore = self._computeBikeScore()

    def _ewmaOfTimePower(self, time_power):
        '''
        calculate ewma of time_power
        時系列区間N=25s
        return ewmaを適用したSeries, 計測時間
        '''
        #時系列間隔を1sごとに調整
        replot = time_power.asfreq('1S', method='pad')
        smoothTimePower = pandas.ewma(replot, span=25)
        return smoothTimePower, len(replot)

    def _computeXPower(self):
        '''
        xPowerを計算する
        1.smoothTimePowerの4乗を取得する
        2.4乗の平均をとる
        3.平均値の4乗根を取る:
        '''
        fourthMean = numpy.array([i ** 4 for i in self.smoothTimePower]).mean()
        xPower = fourthMean ** (1.0 / 4.0)
        return xPower

    def getXPower(self):
        return self.xPower

    def _computeRelativeIntensity(self):
        '''
        RI = xPower/ CriticalPower
        '''
        return self.xPower / self.cp

    def _computeNormalizedWork(self):
        '''
        7.Multiply the xPower by the duration of the workout
        in seconds to obtain a Multiply the xPower
        by the duration of the workout in seconds to obtain a
        “normalized work” value in joules.
        workout時間にxPowerを掛ける
        '''
        return self.xPower * self.period

    def _computeBikeScore(self):
        '''
        9. Divide the values from step 8 by the amount
        of work performed during an hour at Critical Power.
        10. Multiply the number from step 9
        by 100 to obtain the final BikeScore.
        '''
        rawBikeScore = self.normalizedWork * self.RI
        amountTime = self.period / 60
        hourPower = rawBikeScore / amountTime
        bikeScore = hourPower / 100
        return bikeScore

    def getBikeScore(self):
        return self.bikeScore


import scipy.optimize


class CriticalPower(object):
    def __init__(self, dataset):
        '''
        dataset = [(sec,work J)]
        tuple need more than 2.
        compute CriticalPower
        '''
        seconds = numpy.array([datum[0] for datum in dataset])
        works = numpy.array([datum[1] for datum in dataset])

        fitfunc = lambda p, x: p[0] * x + p[1]
        errfunc = lambda p, x, y: fitfunc(p, x) - y
        p0 = [0, 0]
        self._p1, success = \
            scipy.optimize.leastsq(errfunc, p0, args=(seconds, works))
        if success == False:
            raise ArithmeticError

    def getCP(self):
        '''
        Return CriticalPower
        '''
        return self._p1[0]
