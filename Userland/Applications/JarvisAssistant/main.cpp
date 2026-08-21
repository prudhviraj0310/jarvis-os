/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "JarvisAssistantWidget.h"
#include "ArcReactorWidget.h"
#include <LibCore/System.h>
#include <LibGUI/Application.h>
#include <LibGUI/Icon.h>
#include <LibGUI/Window.h>
#include <LibMain/Main.h>

ErrorOr<int> serenity_main(Main::Arguments arguments)
{
    TRY(Core::System::pledge("stdio recvfd sendfd rpath unix"));
    auto app = TRY(GUI::Application::create(arguments));

    TRY(Core::System::pledge("stdio recvfd sendfd rpath unix"));
    TRY(Core::System::unveil("/res", "r"));
    TRY(Core::System::unveil("/tmp", "rwc"));
    TRY(Core::System::unveil("/etc/jarvis", "r"));
    TRY(Core::System::unveil(nullptr, nullptr));

    auto app_icon = GUI::Icon::default_icon("app-terminal"sv);

    auto window = GUI::Window::construct();
    window->set_title("⚡ JARVIS Holographic Tactical Command HUD");
    window->resize(980, 680);
    window->center_on_screen();

    auto widget = TRY(JarvisAssistant::JarvisAssistantWidget::try_create());
    TRY(widget->initialize());
    window->set_main_widget(widget.ptr());
    window->set_icon(app_icon.bitmap_for_size(16));

    window->show();

    return app->exec();
}
