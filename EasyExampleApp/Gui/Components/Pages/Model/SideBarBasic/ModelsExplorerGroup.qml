// SPDX-FileCopyrightText: 2022 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals


Column {
    spacing: EaStyle.Sizes.fontPixelSize

    // Table

    EaComponents.TableView {

        defaultInfoText: qsTr("No models loaded")

        // Table model

        model: EaComponents.JsonListModel {
            json: Globals.Proxies.mainProxy.model.isCreated ?
                      JSON.stringify(Globals.Proxies.mainProxy.model.asJson) :
                      ""
            query: "$[*]"
        }

        // Table rows

        delegate: EaComponents.TableViewDelegate {

            EaComponents.TableViewLabel {
                width: EaStyle.Sizes.fontPixelSize * 2.5
                headerText: "No."
                text: model.index + 1
            }

            EaComponents.TableViewTextInput {
                horizontalAlignment: Text.AlignLeft
                width: EaStyle.Sizes.fontPixelSize * 27.9
                headerText: "Label"
                text: model.label
            }

            EaComponents.TableViewLabel {
                headerText: "Color"
                backgroundColor: EaStyle.Colors.chartForegrounds[0]
            }

            EaComponents.TableViewButton {
                id: deleteRowColumn
                headerText: "Del."
                fontIcon: "minus-circle"
                ToolTip.text: qsTr("Remove this model")
                onClicked: {
                    Globals.Proxies.mainProxy.experiment.emptyMeasuredData()
                    Globals.Proxies.mainProxy.model.emptyCalculatedData()
                    Globals.Vars.experimentPageEnabled = false
                    Globals.Vars.analysisPageEnabled = false
                    Globals.Vars.summaryPageEnabled = false
                }
            }

        }

    }

    // Control buttons below table

    Row {
        spacing: EaStyle.Sizes.fontPixelSize

        EaElements.SideBarButton {
            enabled: false
            fontIcon: "upload"
            text: qsTr("Load new model from file")
        }

        EaElements.SideBarButton {
            enabled: !Globals.Proxies.mainProxy.model.isCreated
            fontIcon: "plus-circle"
            text: qsTr("Add new model manually")
            onClicked: Globals.Proxies.mainProxy.model.generateCalculatedData()
            Component.onCompleted: Globals.Refs.app.modelPage.addNewModelManuallyButton = this
        }
    }

}