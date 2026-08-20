@JarvisAssistant::JarvisAssistantWidget {
    fill_with_background_color: true
    layout: @GUI::VerticalBoxLayout {
        margins: [12]
        spacing: 8
    }

    @GUI::GroupBox {
        title: "⚡ JARVIS OS — HOLOGRAPHIC TACTICAL COMMAND MATRIX"
        preferred_height: 48
        layout: @GUI::HorizontalBoxLayout {
            margins: [8]
            spacing: 12
        }

        @GUI::Label {
            name: "status_label"
            text: "KERNEL: JARVIS OS 1.0 (64-bit) | CPU: ACTIVE | MEMORY: NOMINAL"
            text_alignment: "CenterLeft"
        }

        @GUI::Label {
            name: "shield_label"
            text: "ULTIMATE SHIELD: ACTIVE (100%) | DEFCON: NOMINAL"
            text_alignment: "CenterRight"
        }
    }

    @GUI::Widget {
        layout: @GUI::HorizontalBoxLayout {
            spacing: 10
        }

        @GUI::GroupBox {
            title: "Tactical Protocols"
            preferred_width: 220
            layout: @GUI::VerticalBoxLayout {
                margins: [8]
                spacing: 6
            }

            @GUI::Button {
                name: "btn_diag"
                text: "⚡ System Diagnostics"
            }

            @GUI::Button {
                name: "btn_shield"
                text: "🛡️ Ultimate Shield ON"
            }

            @GUI::Button {
                name: "btn_lockdown"
                text: "🔒 DEFCON-1 Lockdown"
            }

            @GUI::Button {
                name: "btn_journal"
                text: "📜 SHA-256 Crypto Log"
            }

            @GUI::Button {
                name: "btn_mem"
                text: "🔍 Kernel Memory Scan"
            }

            @GUI::Button {
                name: "btn_who"
                text: "🌐 JARVIS Identity"
            }
        }

        @GUI::Widget {
            layout: @GUI::VerticalBoxLayout {
                spacing: 6
            }

            @JarvisAssistant::ArcReactorWidget {
                name: "arc_reactor_widget"
                preferred_height: 230
            }

            @GUI::Widget {
                preferred_height: 30
                layout: @GUI::HorizontalBoxLayout {
                    spacing: 6
                }

                @GUI::Button {
                    name: "chip_status"
                    text: "📊 Status"
                }

                @GUI::Button {
                    name: "chip_shield"
                    text: "🛡️ Shield"
                }

                @GUI::Button {
                    name: "chip_diag"
                    text: "⚡ Diag"
                }

                @GUI::Button {
                    name: "chip_lockdown"
                    text: "🔒 Lockdown"
                }

                @GUI::Button {
                    name: "chip_identity"
                    text: "🤖 Identity"
                }
            }
        }

        @GUI::GroupBox {
            title: "Defense & Threat Vectors"
            preferred_width: 220
            layout: @GUI::VerticalBoxLayout {
                margins: [8]
                spacing: 4
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

            @GUI::Label {
                text: "IPC: /tmp/portal/jarvis"
                text_alignment: "CenterLeft"
            }
        }
    }

    @GUI::GroupBox {
        title: "Neural Voice & Cognitive Command Console"
        preferred_height: 48
        layout: @GUI::HorizontalBoxLayout {
            margins: [8]
            spacing: 8
        }

        @GUI::Button {
            name: "voice_button"
            text: "🎙️ Wake JARVIS"
            fixed_width: 130
        }

        @GUI::TextBox {
            name: "capability_input"
            placeholder: "Speak or type command (status, shield, lockdown, diagnostics, memory, who are you)..."
        }

        @GUI::Button {
            name: "execute_button"
            text: "Execute"
            fixed_width: 90
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
