// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements

import Gui.Globals as Globals


EaElements.GroupRow {

    EaElements.Parameter {
        enabled: false
        title: qsTr('name H-M alt')
        text: Globals.Proxies.modelParameterValue('_space_group_name_H-M_alt')
        horizontalAlignment: TextField.AlignLeft
    }

    EaElements.Parameter {
        enabled: false
        title: qsTr('IT coordinate system code')
        text: Globals.Proxies.modelParameterValue('_space_group_IT_coordinate_system_code')
        horizontalAlignment: TextField.AlignLeft
    }

}