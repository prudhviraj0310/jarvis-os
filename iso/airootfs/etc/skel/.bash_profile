# Auto-start Hyprland on login to tty1
if [ -z "${WAYLAND_DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
    export QT_QPA_PLATFORM="wayland;xcb"
    export GDK_BACKEND="wayland,x11"
    export MOZ_ENABLE_WAYLAND=1
    exec Hyprland
fi
