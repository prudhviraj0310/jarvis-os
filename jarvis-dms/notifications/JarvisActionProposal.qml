/*
 * Copyright (c) 2026, JARVIS OS Engineering Team
 * SPDX-License-Identifier: MIT
 *
 * Material 3 Action Proposal Confirmation Modal for DankMaterialShell
 * Connects directly to PolicyGate invariant: Model != Authority.
 */

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    id: root
    width: 480
    height: 240
    radius: 20
    color: "#0a0e1a"
    border.color: "#00f3ff"
    border.width: 2

    property string actionId: "ACT-WA-001"
    property string title: "JARVIS ACTION REQUEST"
    property string target: "Send WhatsApp message to Rahul Sharma"
    property string draftText: "\"Yes, I will send the files tomorrow before noon.\""

    signal approved(string id)
    signal rejected(string id)

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 18
        spacing: 12

        RowLayout {
            spacing: 8
            Text { text: "🛡️"; font.pixelSize: 18 }
            Text {
                text: root.title
                color: "#00f3ff"
                font.bold: true
                font.pixelSize: 14
            }
        }

        Text {
            text: root.target
            color: "#ffffff"
            font.bold: true
            font.pixelSize: 13
        }

        Rectangle {
            Layout.fillWidth: true
            height: 60
            radius: 10
            color: "#162038"
            border.color: "rgba(0, 243, 255, 0.3)"

            Text {
                anchors.centerIn: parent
                width: parent.width - 20
                text: root.draftText
                color: "#b9f6ca"
                wrapMode: Text.WordWrap
                font.italic: true
                font.pixelSize: 12
            }
        }

        Text {
            text: "⚡ Machine Sovereignty Guard: Action requires explicit human approval."
            color: "#80deea"
            font.pixelSize: 10
        }

        RowLayout {
            Layout.alignment: Qt.AlignRight
            spacing: 12

            Button {
                text: "REJECT"
                onClicked: root.rejected(root.actionId)
            }

            Button {
                text: "APPROVE"
                highlighted: true
                onClicked: root.approved(root.actionId)
            }
        }
    }
}
