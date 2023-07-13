# SPDX-FileCopyrightText: 2023 EasyExample contributors
# SPDX-License-Identifier: BSD-3-Clause
# © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import numpy as np
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6 import QtCharts

from EasyApp.Logic.Logging import console
from Logic.Helpers import Converter, IO, WebEngine


_LIBS_1D = ['QtCharts', 'Plotly']

class Plotting(QObject):
    currentLib1dChanged = Signal()
    useAcceleration1dChanged = Signal()
    chartRefsChanged = Signal()
    chartRangesChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._proxy = parent
        self._currentLib1d = 'QtCharts'
        self._useAcceleration1d = True
        self._chartRanges = {}
        self._chartRefs = {
            'Plotly': {
                'experimentPage': None,
                'modelPage': None,
                'analysisPage': None
            },
            'QtCharts': {
                'experimentPage': {
                    'measSerie': QtCharts.QXYSeries,
                    'bkgSerie': QtCharts.QXYSeries
                },
                'modelPage': {
                    'calcSerie': QtCharts.QXYSeries,
                    'braggSerie': QtCharts.QXYSeries
                },
                'analysisPage': {
                    'measSerie': QtCharts.QXYSeries,
                    'bkgSerie': QtCharts.QXYSeries,
                    'totalCalcSerie': QtCharts.QXYSeries,
                    'residSerie': QtCharts.QXYSeries,
                    'braggSerie': QtCharts.QXYSeries
                }
            }
        }

    # Frontend/Backend public properties

    @Property(str, notify=currentLib1dChanged)
    def currentLib1d(self):
        return self._currentLib1d

    @currentLib1d.setter
    def currentLib1d(self, newValue):
        if self._currentLib1d == newValue:
            return
        self._currentLib1d = newValue
        self.currentLib1dChanged.emit()

    @Property(bool, notify=useAcceleration1dChanged)
    def useAcceleration1d(self):
        return self._useAcceleration1d

    @useAcceleration1d.setter
    def useAcceleration1d(self, newValue):
        if self._useAcceleration1d == newValue:
            return
        self._useAcceleration1d = newValue
        self.useAcceleration1dChanged.emit()

    @Property('QVariant', notify=chartRangesChanged)
    def chartRanges(self):
        return self._chartRanges

    @Property('QVariant', notify=chartRefsChanged)
    def chartRefs(self):
        return self._chartRefs

    # Frontend/Backend public methods

    @Slot(str, str, 'QVariant')
    def setQtChartsSerieRef(self, page, serie, ref):
        if self._chartRefs['QtCharts'][page][serie] == ref:
            return
        self._chartRefs['QtCharts'][page][serie] = ref
        self.chartRefsChanged.emit()

    @Slot(str, 'QVariant')
    def setPlotlyChartRef(self, page, ref):
        if self._chartRefs['Plotly'][page] == ref:
            return
        self._chartRefs['Plotly'][page] = ref
        self.chartRefsChanged.emit()

    # Backend public methods

    # Experiment

    def drawMeasuredOnExperimentChart(self):
        lib = self._proxy.plotting.currentLib1d
        if lib == 'QtCharts':
            self.qtchartsReplaceMeasuredOnExperimentChartAndRedraw()
        elif lib == 'Plotly':
            self.plotlyReplaceXOnExperimentChart()
            self.plotlyReplaceMeasuredYOnExperimentChart()
            self.plotlyRedrawExperimentChart()

    def drawBackgroundOnExperimentChart(self):
        lib = self._proxy.plotting.currentLib1d
        if lib == 'QtCharts':
            self.qtchartsReplaceBackgroundOnExperimentChartAndRedraw()
        elif lib == 'Plotly':
            pass

    # Analysis

    def drawMeasuredOnAnalysisChart(self):
        lib = self._proxy.plotting.currentLib1d
        if lib == 'QtCharts':
            self.qtchartsReplaceMeasuredOnAnalysisChartAndRedraw()
        elif lib == 'Plotly':
            self.plotlyReplaceXOnAnalysisChart()
            self.plotlyReplaceMeasuredYOnAnalysisChart()

    def drawBackgroundOnAnalysisChart(self):
        lib = self._proxy.plotting.currentLib1d
        if lib == 'QtCharts':
            self.qtchartsReplaceBackgroundOnAnalysisChartAndRedraw()
        elif lib == 'Plotly':
            pass

    def drawCalculatedOnAnalysisChart(self):
        lib = self._proxy.plotting.currentLib1d
        if lib == 'QtCharts':
            self.qtchartsReplaceTotalCalculatedOnAnalysisChartAndRedraw()
        elif lib == 'Plotly':
            self.plotlyReplaceTotalCalculatedYOnAnalysisChartAndRedraw()

    def drawResidualOnAnalysisChart(self):
        lib = self._proxy.plotting.currentLib1d
        if lib == 'QtCharts':
            self.qtchartsReplaceResidualOnAnalysisChartAndRedraw()
        elif lib == 'Plotly':
            pass

    # Backend private methods

    # QtCharts: Experiment

    def qtchartsReplaceMeasuredOnExperimentChartAndRedraw(self):
        index = self._proxy.experiment.currentIndex
        xArray = self._proxy.experiment._xArrays[index]
        yMeasArray = self._proxy.experiment._yMeasArrays[index]
        measSerie = self._chartRefs['QtCharts']['experimentPage']['measSerie']
        measSerie.replaceNp(xArray, yMeasArray)
        console.debug(IO.formatMsg('sub', 'Meas curve', f'{xArray.size} points', 'on experiment page', 'replaced'))

    def qtchartsReplaceBackgroundOnExperimentChartAndRedraw(self):
        index = self._proxy.experiment.currentIndex
        xArray = self._proxy.experiment._xArrays[index]
        yBkgArray = self._proxy.experiment._yBkgArrays[index]
        bkgSerie = self._chartRefs['QtCharts']['experimentPage']['bkgSerie']
        bkgSerie.replaceNp(xArray, yBkgArray)
        console.debug(IO.formatMsg('sub', 'Bkg curve', f'{xArray.size} points', 'on experiment page', 'replaced'))

    # QtCharts: Model

    def qtchartsReplaceCalculatedOnModelChartAndRedraw(self):
        index = self._proxy.model.currentIndex
        xArray = np.empty(0)
        yCalcArray = np.empty(0)
        if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
            xArray = self._proxy.experiment._xArrays[0]  # NEED FIX
            yCalcArray = self._proxy.model._yCalcArrays[index]
        calcSerie = self._chartRefs['QtCharts']['modelPage']['calcSerie']
        calcSerie.replaceNp(xArray, yCalcArray)
        console.error(' - This method is outdated')

    # QtCharts: Analysis

    def qtchartsReplaceMeasuredOnAnalysisChartAndRedraw(self):
        index = self._proxy.experiment.currentIndex
        xArray = self._proxy.experiment._xArrays[index]
        yMeasArray = self._proxy.experiment._yMeasArrays[index]
        measSerie = self._chartRefs['QtCharts']['analysisPage']['measSerie']
        measSerie.replaceNp(xArray, yMeasArray)
        console.debug(IO.formatMsg('sub', 'Meas curve', f'{xArray.size} points', 'on analysis page', 'replaced'))

    def qtchartsReplaceBackgroundOnAnalysisChartAndRedraw(self):
        index = self._proxy.experiment.currentIndex
        xArray = self._proxy.experiment._xArrays[index]
        yBkgArray = self._proxy.experiment._yBkgArrays[index]
        bkgSerie = self._chartRefs['QtCharts']['analysisPage']['bkgSerie']
        bkgSerie.replaceNp(xArray, yBkgArray)
        console.debug(IO.formatMsg('sub', 'Bkg curve', f'{xArray.size} points', 'on analysis page', 'replaced'))

    def qtchartsReplaceTotalCalculatedOnAnalysisChartAndRedraw(self):
        index = self._proxy.experiment.currentIndex
        xArray = self._proxy.experiment._xArrays[index]
        yCalcTotalArray = self._proxy.experiment._yCalcTotalArrays[index]
        calcSerie = self._chartRefs['QtCharts']['analysisPage']['totalCalcSerie']
        calcSerie.replaceNp(xArray, yCalcTotalArray)
        console.debug(IO.formatMsg('sub', 'Calc (total) curve', f'{xArray.size} points', 'on analysis page', 'replaced'))

    def qtchartsReplaceResidualOnAnalysisChartAndRedraw(self):
        index = self._proxy.experiment.currentIndex
        xArray = self._proxy.experiment._xArrays[index]
        yResidArray = self._proxy.experiment._yResidArrays[index]
        residSerie = self._chartRefs['QtCharts']['analysisPage']['residSerie']
        residSerie.replaceNp(xArray, yResidArray)
        console.debug(IO.formatMsg('sub', 'Resid curve', f'{xArray.size} points', 'on analysis page', 'replaced'))


    # Plotly: Experiment

    def plotlyReplaceXOnExperimentChart(self):
        index = self._proxy.experiment.currentIndex
        xArray = np.empty(0)
        if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
            xArray = self._proxy.experiment._xArrays[index]
        arrayStr = Converter.dictToJson(xArray)
        script = f'setXData({arrayStr})'
        chart = self._chartRefs['Plotly']['experimentPage']
        WebEngine.runJavaScriptWithoutCallback(chart, script)

    def plotlyReplaceMeasuredYOnExperimentChart(self):
        index = self._proxy.experiment.currentIndex
        yMeasArray = np.empty(0)
        if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
            yMeasArray = self._proxy.experiment._yMeasArrays[index]
        arrayStr = Converter.dictToJson(yMeasArray)
        script = f'setMeasuredYData({arrayStr})'
        chart = self._chartRefs['Plotly']['experimentPage']
        WebEngine.runJavaScriptWithoutCallback(chart, script)

    def plotlyRedrawExperimentChart(self):
        chart = self._chartRefs['Plotly']['experimentPage']
        script = 'redrawPlot()'
        WebEngine.runJavaScriptWithoutCallback(chart, script)

    # Plotly: Model

    def plotlyReplaceXOnModelChart(self):
        index = self._proxy.experiment.currentIndex
        xArray = np.empty(0)
        if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
            xArray = self._proxy.experiment._xArrays[index]
        arrayStr = Converter.dictToJson(xArray)
        script = f'setXData({arrayStr})'
        chart = self._chartRefs['Plotly']['modelPage']
        WebEngine.runJavaScriptWithoutCallback(chart, script)

    def plotlyReplaceCalculatedYOnModelChart(self):
        index = self._proxy.model.currentIndex
        yCalcArray = np.empty(0)
        if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
            yCalcArray = self._proxy.model._yCalcArrays[index]
        arrayStr = Converter.dictToJson(yCalcArray)
        script = f'setCalculatedYData({arrayStr})'
        chart = self._chartRefs['Plotly']['modelPage']
        WebEngine.runJavaScriptWithoutCallback(chart, script)

    def plotlyRedrawModelChart(self):
        chart = self._chartRefs['Plotly']['modelPage']
        script = 'redrawPlot()'
        WebEngine.runJavaScriptWithoutCallback(chart, script)

    def plotlyReplaceCalculatedYOnModelChartAndRedraw(self):
        chart = self._chartRefs['Plotly']['modelPage']
        array = self._proxy.model.calculated[self._proxy.model.currentIndex]['yArray']
        arrayStr = Converter.dictToJson(array)
        script = f'redrawPlotWithNewCalculatedYJson({{ y:[{arrayStr}] }})'
        WebEngine.runJavaScriptWithoutCallback(chart, script)

    # Plotly: Analysis

    def plotlyReplaceXOnAnalysisChart(self):
        index = self._proxy.experiment.currentIndex
        xArray = np.empty(0)
        if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
            xArray = self._proxy.experiment._xArrays[index]
        arrayStr = Converter.dictToJson(xArray)
        script = f'setXData({arrayStr})'
        chart = self._chartRefs['Plotly']['analysisPage']
        WebEngine.runJavaScriptWithoutCallback(chart, script)

    def plotlyReplaceMeasuredYOnAnalysisChart(self):
        index = self._proxy.experiment.currentIndex
        yMeasArray = np.empty(0)
        if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
            yMeasArray = self._proxy.experiment._yMeasArrays[index]
        arrayStr = Converter.dictToJson(yMeasArray)
        script = f'setMeasuredYData({arrayStr})'
        chart = self._chartRefs['Plotly']['analysisPage']
        WebEngine.runJavaScriptWithoutCallback(chart, script)

    def plotlyReplaceTotalCalculatedYOnAnalysisChart(self):
        index = self._proxy.experiment.currentIndex
        yTotalCalcArray = np.empty(0)
        if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
            yTotalCalcArray = self._proxy.analysis._yCalcTotal
        arrayStr = Converter.dictToJson(yTotalCalcArray)
        script = f'setCalculatedYData({arrayStr})'
        chart = self._chartRefs['Plotly']['analysisPage']
        WebEngine.runJavaScriptWithoutCallback(chart, script)

    def plotlyRedrawAnalysisChart(self):
        chart = self._chartRefs['Plotly']['analysisPage']
        script = 'redrawPlot()'
        WebEngine.runJavaScriptWithoutCallback(chart, script)

    def plotlyReplaceTotalCalculatedYOnAnalysisChartAndRedraw(self):
        if not self._proxy.analysis.defined:
            return
        index = self._proxy.experiment.currentIndex
        yTotalCalcArray = np.empty(0)
        if index > -1 and len(self._proxy.experiment._xArrays):  # NEED FIX
            yTotalCalcArray = self._proxy.analysis._yCalcTotal
        arrayStr = Converter.dictToJson(yTotalCalcArray)
        script = f'redrawPlotWithNewCalculatedYJson({{ y:[{arrayStr}] }})'
        chart = self._chartRefs['Plotly']['analysisPage']
        WebEngine.runJavaScriptWithoutCallback(chart, script)
