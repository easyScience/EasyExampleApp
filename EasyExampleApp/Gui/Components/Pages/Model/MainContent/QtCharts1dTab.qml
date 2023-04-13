// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Charts as EaCharts

import Gui.Globals as Globals


EaCharts.QtCharts1dMeasVsCalc {
    useOpenGL: EaGlobals.Vars.useOpenGL //Globals.Proxies.main.plotting.useWebGL1d

    xAxisTitle: "x"
    yAxisTitle: "y"

    xMin: -10
    xMax: 10
    yMin: 0
    yMax: 4

    // Data is set in python backend

    Component.onCompleted: {
        Globals.Refs.app.experimentPage.plotView = this
        Globals.Proxies.main.plotting.setQtChartsSerieRef('modelPage',
                                                          'calcSerie',
                                                          this.calcSerie)
    }
}