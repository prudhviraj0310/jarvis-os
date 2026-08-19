/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include "ConnectionFromClient.h"
#include <LibCore/EventLoop.h>
#include <LibCore/System.h>
#include <LibIPC/MultiServer.h>
#include <LibMain/Main.h>

ErrorOr<int> serenity_main(Main::Arguments)
{
    TRY(Core::System::pledge("stdio recvfd sendfd accept rpath wpath cpath unix proc"));

    Core::EventLoop event_loop;
    auto server = TRY(IPC::MultiServer<JarvisService::ConnectionFromClient>::try_create());

    TRY(Core::System::unveil("/sys/kernel", "r"));
    TRY(Core::System::unveil("/proc", "r"));
    TRY(Core::System::unveil("/tmp", "rwc"));
    TRY(Core::System::unveil(nullptr, nullptr));

    return event_loop.exec();
}
