// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents

import Gui.Globals as Globals


Rectangle {
    readonly property int commonSpacing: EaStyle.Sizes.fontPixelSize * 1.5

    color: EaStyle.Colors.mainContentBackground

    Column {

        anchors.top: parent.top
        anchors.left: parent.left

        anchors.topMargin: commonSpacing
        anchors.leftMargin: commonSpacing * 1.5

        spacing: commonSpacing

        // Project title

        EaElements.TextInput {
            font.family: EaStyle.Fonts.secondFontFamily
            font.pixelSize: EaStyle.Sizes.fontPixelSize * 3
            font.weight: Font.ExtraLight
            text: Globals.Proxies.mainProxy.project.currentProjectName
        }

        // Project info

        Grid {
            columns: 2
            rowSpacing: 0
            columnSpacing: commonSpacing

            EaElements.Label {
                font.bold: true
                text: qsTr("Description:")
            }
            EaElements.TextInput {
                text: Globals.Proxies.mainProxy.project.currentProjectDescription
            }

            EaElements.Label {
                font.bold: true
                text: qsTr("Location:")
            }
            EaElements.Label {
                text: Globals.Proxies.mainProxy.project.currentProjectLocation
            }

            EaElements.Label {
                font.bold: true
                text: qsTr("Modified:")
            }
            EaElements.Label {
                text: Globals.Proxies.mainProxy.project.currentProjectCreatedDate
            }
        }

        // Project image

        Image {
            //visible: Globals.Proxies.mainProxy.fitting.isFitFinished

            //source: Globals.Proxies.mainProxy.project.currentProjectImage
            width: EaStyle.Sizes.fontPixelSize * 25
            fillMode: Image.PreserveAspectFit
        }

    }

}