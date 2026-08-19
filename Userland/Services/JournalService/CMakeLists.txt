serenity_component(
    JournalService
    REQUIRED
    TARGETS JournalService
)

compile_ipc(JournalServer.ipc JournalServerEndpoint.h)
compile_ipc(JournalClient.ipc JournalClientEndpoint.h)

set(SOURCES
    ConnectionFromClient.cpp
    JournalManager.cpp
    main.cpp
)

set(GENERATED_SOURCES
    JournalServerEndpoint.h
    JournalClientEndpoint.h
)

serenity_bin(JournalService)
target_link_libraries(JournalService PRIVATE LibCore LibCrypto LibIPC LibMain)
