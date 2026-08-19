/*
 * Copyright (c) 2026, JARVIS OS Kernel Team
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include <AK/String.h>
#include <LibCore/ArgsParser.h>
#include <LibCore/EventLoop.h>
#include <LibCore/System.h>
#include <LibJarvis/ConnectionToServer.h>
#include <LibMain/Main.h>

ErrorOr<int> serenity_main(Main::Arguments arguments)
{
    TRY(Core::System::pledge("stdio rpath unix"));

    Core::EventLoop event_loop;

    StringView command;
    StringView capability;
    StringView args_json;

    Core::ArgsParser args_parser;
    args_parser.add_positional_argument(command, "Command (health, run, policy)", "command");
    args_parser.add_positional_argument(capability, "Capability name", "capability", Core::ArgsParser::Required::No);
    args_parser.add_positional_argument(args_json, "Arguments JSON", "arguments", Core::ArgsParser::Required::No);
    args_parser.parse(arguments);

    auto connection = TRY(Jarvis::ConnectionToServer::try_create());

    if (command == "health"sv) {
        auto health = TRY(connection->get_system_health_sync());
        outln("{}", health);
        return 0;
    }

    if (command == "policy"sv) {
        if (capability.is_empty()) {
            warnln("Error: Capability name required for policy query");
            return 1;
        }
        auto cap_str = TRY(String::from_utf8(capability));
        auto result = TRY(connection->query_policy_sync(cap_str));
        outln("{}", result);
        return 0;
    }

    if (command == "run"sv) {
        if (capability.is_empty()) {
            warnln("Error: Capability name required to execute");
            return 1;
        }
        auto cap_str = TRY(String::from_utf8(capability));
        auto args_str = args_json.is_empty() ? "{}"_string : TRY(String::from_utf8(args_json));
        auto result = TRY(connection->request_capability_sync(cap_str, args_str, "req-cli-001"_string));
        outln("{}", result);
        return 0;
    }

    warnln("Unknown command: {}", command);
    warnln("Usage: jarvis <health|policy|run> [capability] [args_json]");
    return 1;
}
