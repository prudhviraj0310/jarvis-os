serenity_component(
    JarvisService
    REQUIRED
    TARGETS JarvisService
)

compile_ipc(JarvisServer.ipc JarvisServerEndpoint.h)
compile_ipc(JarvisClient.ipc JarvisClientEndpoint.h)

set(SOURCES
    Automation/AutomationEngine.cpp
    CapabilityDispatcher.cpp
    Connectors/CalendarConnector.cpp
    Connectors/ConnectorRegistry.cpp
    Connectors/EmailConnector.cpp
    Connectors/FilesConnector.cpp
    Connectors/NewsConnector.cpp
    Connectors/WhatsAppConnector.cpp
    ConnectionFromClient.cpp
    MIRA/MIRAEngine.cpp
    MIRA/MIRAGateway.cpp
    MIRA/MIRAMCPHost.cpp
    MIRA/MIRAMemoryWiki.cpp
    MIRA/MIRAModelRouter.cpp
    MIRA/MIRAProactiveCompanion.cpp
    Persona/PersonaModel.cpp
    PersonalContext/ContactGraph.cpp
    PersonalContext/ContextEngine.cpp
    PersonalContext/PersonalMemory.cpp
    PersonalContext/UserProfile.cpp
    PolicyGate.cpp
    main.cpp
)

set(GENERATED_SOURCES
    JarvisServerEndpoint.h
    JarvisClientEndpoint.h
)

serenity_bin(JarvisService)
target_link_libraries(JarvisService PRIVATE LibCore LibCrypto LibIPC LibMain)
