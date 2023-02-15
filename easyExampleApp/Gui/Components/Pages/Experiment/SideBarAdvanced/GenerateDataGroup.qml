// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as ExGlobals


Row {
    spacing: EaStyle.Sizes.fontPixelSize

    EaElements.Parameter {
        id: inputField

        width: generateDataButton.width
        focus: true

        placeholderText: qsTr('Array length in')
        units: qsTr('points')
        validator: IntValidator { bottom: 2; top: 1000001 }

        Component.onCompleted: text = ExGlobals.Proxies.mainProxy.experiment.measuredDataLength
    }

    EaElements.SideBarButton {
        id: generateDataButton

        text: qsTr('Generate data')
        onClicked: ExGlobals.Proxies.mainProxy.experiment.measuredDataLength = parseInt(inputField.text)
    }

}
