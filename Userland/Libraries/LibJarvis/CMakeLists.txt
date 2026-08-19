serenity_component(
    LibJarvis
    TARGETS LibJarvis
)

set(SOURCES
    ConnectionToServer.cpp
)

serenity_lib(LibJarvis jarvis)
target_link_libraries(LibJarvis PUBLIC LibCore LibIPC)
target_include_directories(LibJarvis PUBLIC ${CMAKE_BINARY_DIR}/Userland/Services)
add_dependencies(LibJarvis generate_JarvisServerEndpoint.h generate_JarvisClientEndpoint.h)
