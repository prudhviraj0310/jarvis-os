/*
 * Copyright (c) 2026, JARVIS OS Engineering Team
 * SPDX-License-Identifier: MIT
 *
 * Material 3 Attendance Pill for DankMaterialShell Top Panel
 */

import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    width: 140
    height: 32
    radius: 16
    color: "#10182c"
    border.color: "#00e676"
    border.width: 1

    property string score: "87.5%"
    property string statusText: "SAFE ZONE"

    RowLayout {
        anchors.centerIn: parent
        spacing: 6

        Text {
            text: "📈"
            font.pixelSize: 14
        }

        Text {
            text: root.score
            color: "#00e676"
            font.bold: true
            font.pixelSize: 13
        }

        Text {
            text: "(+3 Buffer)"
            color: "#80deea"
            font.pixelSize: 10
        }
    }
}
