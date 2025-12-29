import subprocess

# =========================
# DESKTOP (Win32) APPS
# =========================

DESKTOP_APPS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "vscode": r"C:\Users\Lenovo\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "code": r"C:\Users\Lenovo\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "notepad": "notepad.exe"
}

DESKTOP_CLOSE_MAP = {
    "chrome": "chrome.exe",
    "edge": "msedge.exe",
    "vscode": "Code.exe",
    "code": "Code.exe",
    "notepad": "notepad.exe"
}

# =========================
# UWP / MICROSOFT STORE APPS
# =========================

UWP_APPS = {
    "spotify": "SpotifyAB.SpotifyMusic_zpdnekdrzrea0!Spotify",
    "camera": "Microsoft.WindowsCamera_8wekyb3d8bbwe!App",
    "whatsapp": "5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",
    "calculator": "Microsoft.WindowsCalculator_8wekyb3d8bbwe!App"
}


# =========================
# OPEN APP
# =========================

def open_app(app_name: str) -> bool:
    app_name = app_name.lower().strip()

    # Desktop apps
    if app_name in DESKTOP_APPS:
        try:
            subprocess.Popen(DESKTOP_APPS[app_name])
            return True
        except Exception:
            return False

    # UWP apps
    if app_name in UWP_APPS:
        try:
            subprocess.Popen([
                "explorer.exe",
                f"shell:AppsFolder\\{UWP_APPS[app_name]}"
            ])
            return True
        except Exception:
            return False

    return False


# =========================
# CLOSE APP
# =========================

def close_app(app_name: str) -> str:
    """
    Returns:
    - 'closed'         → app closed successfully
    - 'not_supported'  → UWP apps (manual close required)
    - 'failed'         → close attempt failed
    - 'unknown'        → app not recognized
    """
    app_name = app_name.lower().strip()

    
    if app_name in DESKTOP_CLOSE_MAP:
        try:
            subprocess.call(
                ["taskkill", "/IM", DESKTOP_CLOSE_MAP[app_name], "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return "closed"
        except Exception:
            return "failed"

    
    if app_name in UWP_APPS:
        return "not_supported"

    return "unknown"
