serenity_component(
    JarvisService
    REQUIRED
    TARGETS JarvisService
)

compile_ipc(JarvisServer.ipc JarvisServerEndpoint.h)
compile_ipc(JarvisClient.ipc JarvisClientEndpoint.h)

set(SOURCES
    CapabilityDispatcher.cpp
    ConnectionFromClient.cpp
    PolicyGate.cpp
    main.cpp
)

set(GENERATED_SOURCES
    JarvisServerEndpoint.h
    JarvisClientEndpoint.h
)

serenity_bin(JarvisService)
target_link_libraries(JarvisService PRIVATE LibCore LibIPC LibMain)
