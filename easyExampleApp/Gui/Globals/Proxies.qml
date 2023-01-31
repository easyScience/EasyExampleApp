// SPDX-FileCopyrightText: 2023 EasyExample contributors
// SPDX-License-Identifier: BSD-3-Clause
// © 2023 Contributors to the EasyExample project <https://github.com/EasyScience/EasyExampleApp>

pragma Singleton

import QtQuick 2.15


QtObject {

    readonly property var mainProxy: QtObject {
        readonly property var project: QtObject {
            property bool projectCreated: false
            property string currentProjectPath: '_path_'
            property var projectInfoAsJson: QtObject {
                property string name: '_name_'
                property string short_description: '_short_description_'
                property string modified: '_modified_'
            }
            property string statusModelAsXml:
`<root>
   <item>
     <label>Minimization</label>
     <value>lmfit</value>
   </item>
</root>`
            function createProject() { projectCreated = true }
        }
        readonly property var plotting1d: QtObject {
            property var libs: ['Plotly']
            property string currentLib: 'Plotly'
        }
    }

}
