/*
 * Copyright (c) 2026, JARVIS OS Engineering Team
 * SPDX-License-Identifier: MIT
 *
 * Material 3 Executive Command Center for DankMaterialShell
 */

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "../widgets"

Rectangle {
    id: root
    width: 960
    height: 640
    radius: 24
    color: "rgba(10, 14, 26, 0.94)"
    border.color: "rgba(0, 243, 255, 0.4)"
    border.width: 1

    property string currentSection: "briefing"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 16

        // Top Header
        RowLayout {
            Layout.fillWidth: true
            Text {
                text: "⚡ JARVIS OS — EXECUTIVE COMMAND CENTER"
                color: "#00f3ff"
                font.bold: true
                font.pixelSize: 16
            }

            Item { Layout.fillWidth: true }

            JarvisAttendancePill {
                score: "87.5%"
            }
        }

        // Main Content Area
        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 16

            // Left Navigation
            ColumnLayout {
                Layout.preferredWidth: 200
                spacing: 8

                Button {
                    Layout.fillWidth: true
                    text: "🌐 Web Browser"
                }

                Button {
                    Layout.fillWidth: true
                    text: "🌅 Morning Briefing"
                    highlighted: root.currentSection === "briefing"
                    onClicked: root.currentSection = "briefing"
                }

                Button {
                    Layout.fillWidth: true
                    text: "💬 WhatsApp (2)"
                    onClicked: root.currentSection = "whatsapp"
                }

                Button {
                    Layout.fillWidth: true
                    text: "📬 Inbox (3)"
                    onClicked: root.currentSection = "email"
                }

                Button {
                    Layout.fillWidth: true
                    text: "📅 Calendar"
                    onClicked: root.currentSection = "calendar"
                }

                Button {
                    Layout.fillWidth: true
                    text: "🌍 News"
                    onClicked: root.currentSection = "news"
                }

                Item { Layout.fillHeight: true }

                JarvisArcReactor {
                    Layout.alignment: Qt.AlignHCenter
                }
            }

            // Right Intelligence Viewport
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                radius: 16
                color: "rgba(16, 24, 44, 0.7)"
                border.color: "rgba(0, 243, 255, 0.2)"

                ScrollView {
                    anchors.fill: parent
                    anchors.margins: 16

                    Text {
                        width: parent.width
                        color: "#e0f7fa"
                        wrapMode: Text.WordWrap
                        font.pixelSize: 13
                        text: (root.currentSection === "briefing") ?
                            "🌅 EXECUTIVE MORNING INTELLIGENCE BRIEFING\n\n" +
                            "JARVIS: \"Good morning, Prudhvi Raj. All systems and DankMaterialShell Wayland desktop are running at 120 FPS.\"\n\n" +
                            "• [10:30 AM] Operating Systems Capstone Review & Demo (Lab 402)\n" +
                            "• [WhatsApp] Rahul Sharma: \"Bro can you send me the project tomorrow?\" [ACT-WA-001]\n" +
                            "• [Email] Prof. Krishnamurthy: Final Capstone Deliverables (Deadline: Tomorrow 5 PM)\n" +
                            "• [Attendance] 87.5% (Safe Zone: +3 Buffer. Exam clearance guaranteed.)\n\n" +
                            "Click 'Handle It' or speak instructions."
                            :
                            "💬 WHATSAPP & COMMUNICATIONS\n\n" +
                            "• Rahul Sharma (07:45 AM): \"Bro can you send me the project tomorrow?\"\n" +
                            "• Priya V. (08:10 AM): \"Are we meeting in the library at 2 PM?\""
                    }
                }
            }
        }
    }
}
