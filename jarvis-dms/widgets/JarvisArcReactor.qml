/*
 * Copyright (c) 2026, JARVIS OS Engineering Team
 * SPDX-License-Identifier: MIT
 *
 * Material 3 Quickshell Arc Reactor Widget for DankMaterialShell
 */

import QtQuick
import QtQuick.Controls

Item {
    id: root
    width: 220
    height: 220

    property real rotationAngle: 0
    property color cyanGlow: "#00f3ff"
    property color coreGreen: "#00e676"
    property bool activeVoice: false

    Canvas {
        id: canvas
        anchors.fill: parent

        onPaint: {
            var ctx = getContext("2d");
            ctx.reset();
            var cx = width / 2;
            var cy = height / 2;

            // Outer Glowing Ring
            ctx.save();
            ctx.beginPath();
            ctx.arc(cx, cy, 80, 0, Math.PI * 2);
            ctx.strokeStyle = root.cyanGlow;
            ctx.lineWidth = 3;
            ctx.shadowColor = root.cyanGlow;
            ctx.shadowBlur = 15;
            ctx.stroke();

            // Segmented Arc Reactor Segments
            ctx.translate(cx, cy);
            ctx.rotate(root.rotationAngle * Math.PI / 180);
            var segments = 10;
            for (var i = 0; i < segments; i++) {
                ctx.beginPath();
                var startA = (i * 2 * Math.PI) / segments;
                var endA = startA + Math.PI / segments;
                ctx.arc(0, 0, 65, startA, endA);
                ctx.strokeStyle = (i % 2 === 0) ? "#00f3ff" : "#0066ff";
                ctx.lineWidth = 6;
                ctx.stroke();
            }

            // Inner Core
            ctx.rotate(-root.rotationAngle * 2 * Math.PI / 180);
            ctx.beginPath();
            for (var j = 0; j < 3; j++) {
                var a = (j * 2 * Math.PI) / 3;
                var x = Math.cos(a) * 35;
                var y = Math.sin(a) * 35;
                if (j === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
            }
            ctx.closePath();
            ctx.strokeStyle = root.coreGreen;
            ctx.lineWidth = 3;
            ctx.stroke();

            // Center Point
            ctx.beginPath();
            ctx.arc(0, 0, 14, 0, Math.PI * 2);
            ctx.fillStyle = "#ffffff";
            ctx.fill();

            ctx.restore();
        }
    }

    NumberAnimation {
        target: root
        property: "rotationAngle"
        from: 0
        to: 360
        duration: 8000
        loops: Animation.Infinite
        running: true
        onTriggered: canvas.requestPaint()
    }
}
