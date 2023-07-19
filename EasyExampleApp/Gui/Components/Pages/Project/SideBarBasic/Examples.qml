// SPDX-FileCopyrightText: 2022 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2022 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

import QtQuick
import QtQuick.Controls

import EasyApp.Gui.Globals as EaGlobals
import EasyApp.Gui.Style as EaStyle
import EasyApp.Gui.Elements as EaElements
import EasyApp.Gui.Components as EaComponents
import EasyApp.Gui.Logic as EaLogic

import Gui.Globals as Globals


EaComponents.TableView {
    id: tableView

    maxRowCountShow: 9
    defaultInfoText: qsTr("No examples available")

    // Table model
    /*
    model: EaComponents.JsonListModel {
        json: JSON.stringify(Globals.Proxies.main.project.examples)
        query: "$[*]"
    }
    */
    // We only use the length of the model object defined in backend logic and
    // directly access that model in every row using the TableView index property.
    model: Globals.Proxies.main.project.examples
    // Table model

    // Header row
    header: EaComponents.TableViewHeader {

        EaComponents.TableViewLabel {
            enabled: false
            width: EaStyle.Sizes.fontPixelSize * 2.5
            //text: qsTr("No.")
        }

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.fontPixelSize * 10
            horizontalAlignment: Text.AlignLeft
            color: EaStyle.Colors.themeForegroundMinor
            text: qsTr("name")
        }

        EaComponents.TableViewLabel {
            flexibleWidth: true
            horizontalAlignment: Text.AlignLeft
            color: EaStyle.Colors.themeForegroundMinor
            text: qsTr("description")
        }

        EaComponents.TableViewLabel {
            width: EaStyle.Sizes.tableRowHeight
        }

    }
    // Header row


    // Table rows
    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            text: index + 1
            color: EaStyle.Colors.themeForegroundMinor
        }

        EaComponents.TableViewLabel {
            text: tableView.model[index].name
        }

        EaComponents.TableViewLabelControl {
            text: tableView.model[index].description
            ToolTip.text: tableView.model[index].description
        }

        EaComponents.TableViewButton {
            fontIcon: "upload"
            ToolTip.text: qsTr("Load this example")
            onClicked: {
                const fpath = Qt.resolvedUrl(tableView.model[index].path)
                Globals.Proxies.main.project.loadProjectFromFile(fpath)
            }
        }

    }
    // Table rows

}
