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
        title: qsTr('length a')
        text: Globals.Proxies.modelParameterValue('_cell_length_a')
        onEditingFinished: Globals.Proxies.setModelParameterValue('_cell_length_a', text)
    }

    EaElements.Parameter {
        title: qsTr('length b')
        text: Globals.Proxies.modelParameterValue('_cell_length_b')
        onEditingFinished: setParameterValue('_cell_length_b', text)
    }

    EaElements.Parameter {
        title: qsTr('length c')
        text: Globals.Proxies.modelParameterValue('_cell_length_c')
        onEditingFinished: setParameterValue('_cell_length_c', text)
    }

    EaElements.Parameter {
        title: qsTr('angle α')
        text: Globals.Proxies.modelParameterValue('_cell_angle_alpha')
        onEditingFinished: setParameterValue('_cell_angle_alpha', text)
    }

    EaElements.Parameter {
        title: qsTr('angle β')
        text: Globals.Proxies.modelParameterValue('_cell_angle_beta')
        onEditingFinished: setParameterValue('_cell_angle_beta', text)
    }

    EaElements.Parameter {
        title: qsTr('angle γ')
        text: Globals.Proxies.modelParameterValue('_cell_angle_gamma')
        onEditingFinished: setParameterValue('_cell_angle_gamma', text)
    }

}
