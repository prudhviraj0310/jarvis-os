@JarvisAssistant::JarvisAssistantWidget {
    fill_with_background_color: true
    layout: @GUI::VerticalBoxLayout {
        margins: [16]
        spacing: 12
    }

    @GUI::GroupBox {
        title: "⚡ JARVIS OS — HOLOGRAPHIC TACTICAL COMMAND MATRIX"
        preferred_height: 50
        layout: @GUI::HorizontalBoxLayout {
            margins: [8]
            spacing: 12
        }

        @GUI::Label {
            name: "status_label"
            text: "KERNEL: JARVIS OS 1.0 (Foundation) | CPU: ACTIVE | MEM: NOMINAL"
            text_alignment: "CenterLeft"
        }

        @GUI::Label {
            name: "shield_label"
            text: "ULTIMATE SHIELD: 100% | DEFCON: NOMINAL"
            text_alignment: "CenterRight"
        }
    }

    @GUI::Widget {
        layout: @GUI::HorizontalBoxLayout {
            spacing: 12
        }

        @GUI::GroupBox {
            title: "Tactical Protocols & Sentry"
            preferred_width: 240
            layout: @GUI::VerticalBoxLayout {
                margins: [8]
                spacing: 8
            }

            @GUI::Button {
                name: "btn_diag"
                text: "⚡ Full System Diagnostics"
            }

            @GUI::Button {
                name: "btn_shield"
                text: "🛡️ Ultimate Shield Perimeter"
            }

            @GUI::Button {
                name: "btn_lockdown"
                text: "🔒 DEFCON-1 Lockdown"
            }

            @GUI::Button {
                name: "btn_journal"
                text: "📜 SHA-256 Crypto Journal"
            }

            @GUI::Label {
                name: "ipc_label"
                text: "IPC: /tmp/portal/jarvis\nMode: Fullscreen HUD"
                text_alignment: "Center"
            }
        }

        @JarvisAssistant::ArcReactorWidget {
            name: "arc_reactor_widget"
        }

        @GUI::GroupBox {
            title: "Threat & Telemetry Vectors"
            preferred_width: 240
            layout: @GUI::VerticalBoxLayout {
                margins: [8]
                spacing: 6
            }

            @GUI::Label {
                text: "Syscall Security: ENFORCED"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "Journal State: CHAINED"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "VFS Integrity: VERIFIED"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "Core Frequency: 60 FPS"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "Voice Matrix: ENGAGED"
                text_alignment: "CenterLeft"
            }
        }
    }

    @GUI::GroupBox {
        title: "Neural Voice & Cognitive Command Console"
        preferred_height: "shrink"
        layout: @GUI::HorizontalBoxLayout {
            margins: [8]
            spacing: 8
        }

        @GUI::Button {
            name: "voice_button"
            text: "🎙️ Voice"
            fixed_width: 90
        }

        @GUI::TextBox {
            name: "capability_input"
            placeholder: "Speak or type voice command (status, shield, processes, lockdown, memory)..."
        }

        @GUI::Button {
            name: "execute_button"
            text: "Execute"
            fixed_width: 100
        }
    }

    @GUI::GroupBox {
        title: "Holographic Neural & Cryptographic Execution Journal Log"
        preferred_height: 180
        layout: @GUI::VerticalBoxLayout {
            margins: [8]
            spacing: 4
        }

        @GUI::TextEditor {
            name: "output_editor"
            mode: "DisplayOnly"
        }
    }
}
