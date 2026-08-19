serenity_component(
    JarvisAssistant
    RECOMMENDED
    TARGETS JarvisAssistant
)

compile_gml(JarvisAssistantWindow.gml JarvisAssistantGML.cpp)

set(SOURCES
    main.cpp
    JarvisAssistantWidget.cpp
    ArcReactorWidget.cpp
    JarvisAssistantGML.cpp
)

serenity_app(JarvisAssistant ICON app-terminal)
target_link_libraries(JarvisAssistant PRIVATE LibCore LibGfx LibGUI LibJarvis LibMain)
