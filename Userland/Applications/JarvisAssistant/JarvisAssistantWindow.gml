@JarvisAssistant::JarvisAssistantWidget {
    fill_with_background_color: true
    layout: @GUI::VerticalBoxLayout {
        margins: [12]
        spacing: 8
    }

    @GUI::GroupBox {
        title: "⚡ JARVIS OS — HOLOGRAPHIC TACTICAL COMMAND MATRIX & MORNING INTELLIGENCE"
        preferred_height: 48
        layout: @GUI::HorizontalBoxLayout {
            margins: [8]
            spacing: 12
        }

        @GUI::Label {
            name: "status_label"
            text: "KERNEL: JARVIS OS 1.0 | TIME: 08:00 AM | STATUS: ONLINE"
            text_alignment: "CenterLeft"
        }

        @GUI::Label {
            name: "shield_label"
            text: "ULTIMATE SHIELD: ACTIVE (100%) | READINESS: 96%"
            text_alignment: "CenterRight"
        }
    }

    @GUI::Widget {
        layout: @GUI::HorizontalBoxLayout {
            spacing: 10
        }

        @GUI::GroupBox {
            title: "Daily Intelligence & Protocols"
            preferred_width: 220
            layout: @GUI::VerticalBoxLayout {
                margins: [8]
                spacing: 5
            }

            @GUI::Button {
                name: "btn_briefing"
                text: "🌅 Morning Briefing"
            }

            @GUI::Button {
                name: "btn_whatsapp"
                text: "💬 WhatsApp (3 Unread)"
            }

            @GUI::Button {
                name: "btn_email"
                text: "📬 Priority Emails (4)"
            }

            @GUI::Button {
                name: "btn_score"
                text: "📊 Readiness Score (96%)"
            }

            @GUI::Button {
                name: "btn_news"
                text: "🌍 World & Tech News"
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
                name: "btn_diag"
                text: "⚡ System Diagnostics"
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
                    spacing: 4
                }

                @GUI::Button {
                    name: "chip_briefing"
                    text: "🌅 Briefing"
                }

                @GUI::Button {
                    name: "chip_whatsapp"
                    text: "💬 WhatsApp"
                }

                @GUI::Button {
                    name: "chip_email"
                    text: "📬 Emails"
                }

                @GUI::Button {
                    name: "chip_score"
                    text: "📈 96% Score"
                }

                @GUI::Button {
                    name: "chip_news"
                    text: "🌍 News"
                }

                @GUI::Button {
                    name: "chip_shield"
                    text: "🛡️ Shield"
                }
            }
        }

        @GUI::GroupBox {
            title: "Personal Telemetry & Defense"
            preferred_width: 220
            layout: @GUI::VerticalBoxLayout {
                margins: [8]
                spacing: 4
            }

            @GUI::Label {
                text: "Daily Readiness: 96% (Optimal)"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "Battery Power: 98% (Healthy)"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "WhatsApp Sync: CONNECTED"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "Email Feed: SYNCHRONIZED"
                text_alignment: "CenterLeft"
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
        title: "Neural Voice & Cognitive Intelligence Command Console"
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
            placeholder: "Speak or type (morning briefing, whatsapp, email, percentage, news, shield, lockdown)..."
        }

        @GUI::Button {
            name: "execute_button"
            text: "Execute"
            fixed_width: 90
        }
    }

    @GUI::GroupBox {
        title: "Holographic Intelligence Briefing & Execution Journal Log"
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
