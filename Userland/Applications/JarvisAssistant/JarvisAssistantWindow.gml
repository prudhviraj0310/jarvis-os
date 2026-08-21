@JarvisAssistant::JarvisAssistantWidget {
    fill_with_background_color: true
    layout: @GUI::VerticalBoxLayout {
        margins: [12]
        spacing: 8
    }

    @GUI::GroupBox {
        title: "⚡ JARVIS OS 1.0 — MIRA DEEP SELF-HOSTED PERSONAL AGENT OPERATING SYSTEM"
        preferred_height: 48
        layout: @GUI::HorizontalBoxLayout {
            margins: [8]
            spacing: 12
        }

        @GUI::Label {
            name: "status_label"
            text: "KERNEL: JARVIS OS 1.0 | MIRA AGENT CORE: ACTIVE | SOVEREIGN ARCHITECTURE"
            text_alignment: "CenterLeft"
        }

        @GUI::Label {
            name: "shield_label"
            text: "SHIELD: 100% | ATTENDANCE: 87.5% (Safe Zone)"
            text_alignment: "CenterRight"
        }
    }

    @GUI::Widget {
        layout: @GUI::HorizontalBoxLayout {
            spacing: 10
        }

        @GUI::GroupBox {
            title: "MIRA & Personal Nervous Center"
            preferred_width: 220
            layout: @GUI::VerticalBoxLayout {
                margins: [8]
                spacing: 4
            }

            @GUI::Button {
                name: "btn_browser"
                text: "🌐 Launch Web Browser"
            }

            @GUI::Button {
                name: "btn_mira"
                text: "🤖 MIRA Agent Engine"
            }

            @GUI::Button {
                name: "btn_briefing"
                text: "🌅 Morning Briefing"
            }

            @GUI::Button {
                name: "btn_whatsapp"
                text: "💬 WhatsApp Intelligence"
            }

            @GUI::Button {
                name: "btn_email"
                text: "📬 Inbox Intelligence"
            }

            @GUI::Button {
                name: "btn_calendar"
                text: "📅 Calendar & Deadlines"
            }

            @GUI::Button {
                name: "btn_news"
                text: "🌍 Clustered News"
            }

            @GUI::Button {
                name: "btn_memory"
                text: "🧠 Memory & Wiki Graph"
            }

            @GUI::Button {
                name: "btn_handle_it"
                text: "⚡ 'Handle It' (Propose)"
            }

            @GUI::Button {
                name: "btn_confirm_all"
                text: "✅ Confirm & Send All"
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
                    name: "chip_browser"
                    text: "🌐 Browser"
                }

                @GUI::Button {
                    name: "chip_mira"
                    text: "🤖 MIRA"
                }

                @GUI::Button {
                    name: "chip_briefing"
                    text: "🌅 Brief"
                }

                @GUI::Button {
                    name: "chip_whatsapp"
                    text: "💬 WhatsApp"
                }

                @GUI::Button {
                    name: "chip_email"
                    text: "📬 Email"
                }

                @GUI::Button {
                    name: "chip_calendar"
                    text: "📅 Agenda"
                }

                @GUI::Button {
                    name: "chip_handle_it"
                    text: "⚡ Handle It"
                }

                @GUI::Button {
                    name: "chip_confirm"
                    text: "✅ Confirm"
                }
            }
        }

        @GUI::GroupBox {
            title: "MIRA Multi-Channel Telemetry"
            preferred_width: 220
            layout: @GUI::VerticalBoxLayout {
                margins: [8]
                spacing: 4
            }

            @GUI::Label {
                text: "Web Browser: STANDBY"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "MIRA Gateway: 8 CHANNELS"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "Model Router: DUAL-TIER"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "Companion: ACTIVE CHECK-IN"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "Memory Wiki: 3 ARTICLES"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "MCP Host: 3 SANDBOXED TOOLS"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "Policy Guard: SOVEREIGN"
                text_alignment: "CenterLeft"
            }

            @GUI::Label {
                text: "Voice Matrix: 44.1 kHz DUPLEX"
                text_alignment: "CenterLeft"
            }
        }
    }

    @GUI::GroupBox {
        title: "Cognitive Command & Voice Interface (Type or Speak)"
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
            placeholder: "Speak or type (e.g., 'browser', 'mira', 'morning briefing', 'handle it', 'confirm', 'whatsapp', 'email')..."
        }

        @GUI::Button {
            name: "execute_button"
            text: "Execute"
            fixed_width: 90
        }
    }

    @GUI::GroupBox {
        title: "Executive Intelligence Briefing, Context Stream & Execution Journal"
        preferred_height: 200
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
