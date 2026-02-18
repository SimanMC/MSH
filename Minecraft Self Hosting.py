#!/usr/bin/env python3
"""
Minecraft Server Setup — GUI
Requires: Python 3.8+  (tkinter is built-in)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import socket
import urllib.request
import subprocess
import threading
import json
import os
import shutil
import time
from pathlib import Path

# Palette
BG       = "#1a1c1e"
PANEL    = "#23262b"
CARD     = "#2c3038"
GREEN    = "#5dbe6e"
GREEN_DK = "#3d9950"
TEXT     = "#e8eaed"
MUTED    = "#7e848f"
BORDER   = "#353940"
RED      = "#e05c5c"
RED_DK   = "#b03c3c"
ORANGE   = "#e8a44a"
BLUE     = "#5b9bd5"
FONT     = ("Segoe UI", 10)

# PaperMC — starts at 1.8 (first Paper release)
# Note: 1.8–1.15 use legacy Paperclip URLs from GitHub releases
PAPER_VERSIONS = {
    # ── 1.21.x ──────────────────────────────────────────────────────
    "1.21.4": "https://api.papermc.io/v2/projects/paper/versions/1.21.4/builds/174/downloads/paper-1.21.4-174.jar",
    "1.21.3": "https://api.papermc.io/v2/projects/paper/versions/1.21.3/builds/58/downloads/paper-1.21.3-58.jar",
    "1.21.1": "https://api.papermc.io/v2/projects/paper/versions/1.21.1/builds/132/downloads/paper-1.21.1-132.jar",
    "1.21":   "https://api.papermc.io/v2/projects/paper/versions/1.21/builds/130/downloads/paper-1.21-130.jar",
    # ── 1.20.x ──────────────────────────────────────────────────────
    "1.20.6": "https://api.papermc.io/v2/projects/paper/versions/1.20.6/builds/151/downloads/paper-1.20.6-151.jar",
    "1.20.4": "https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/497/downloads/paper-1.20.4-497.jar",
    "1.20.2": "https://api.papermc.io/v2/projects/paper/versions/1.20.2/builds/318/downloads/paper-1.20.2-318.jar",
    "1.20.1": "https://api.papermc.io/v2/projects/paper/versions/1.20.1/builds/196/downloads/paper-1.20.1-196.jar",
    # ── 1.19.x ──────────────────────────────────────────────────────
    "1.19.4": "https://api.papermc.io/v2/projects/paper/versions/1.19.4/builds/550/downloads/paper-1.19.4-550.jar",
    "1.19.3": "https://api.papermc.io/v2/projects/paper/versions/1.19.3/builds/448/downloads/paper-1.19.3-448.jar",
    "1.19.2": "https://api.papermc.io/v2/projects/paper/versions/1.19.2/builds/307/downloads/paper-1.19.2-307.jar",
    "1.19":   "https://api.papermc.io/v2/projects/paper/versions/1.19/builds/81/downloads/paper-1.19-81.jar",
    # ── 1.18.x ──────────────────────────────────────────────────────
    "1.18.2": "https://api.papermc.io/v2/projects/paper/versions/1.18.2/builds/388/downloads/paper-1.18.2-388.jar",
    "1.18.1": "https://api.papermc.io/v2/projects/paper/versions/1.18.1/builds/216/downloads/paper-1.18.1-216.jar",
    # ── 1.17.x ──────────────────────────────────────────────────────
    "1.17.1": "https://api.papermc.io/v2/projects/paper/versions/1.17.1/builds/411/downloads/paper-1.17.1-411.jar",
    # ── 1.16.x ──────────────────────────────────────────────────────
    "1.16.5": "https://api.papermc.io/v2/projects/paper/versions/1.16.5/builds/794/downloads/paper-1.16.5-794.jar",
    "1.16.4": "https://api.papermc.io/v2/projects/paper/versions/1.16.4/builds/416/downloads/paper-1.16.4-416.jar",
    "1.16.3": "https://api.papermc.io/v2/projects/paper/versions/1.16.3/builds/253/downloads/paper-1.16.3-253.jar",
    "1.16.2": "https://api.papermc.io/v2/projects/paper/versions/1.16.2/builds/189/downloads/paper-1.16.2-189.jar",
    "1.16.1": "https://api.papermc.io/v2/projects/paper/versions/1.16.1/builds/138/downloads/paper-1.16.1-138.jar",
    # ── 1.15.x ──────────────────────────────────────────────────────
    "1.15.2": "https://api.papermc.io/v2/projects/paper/versions/1.15.2/builds/391/downloads/paper-1.15.2-391.jar",
    "1.15.1": "https://api.papermc.io/v2/projects/paper/versions/1.15.1/builds/47/downloads/paper-1.15.1-47.jar",
    # ── 1.14.x ──────────────────────────────────────────────────────
    "1.14.4": "https://api.papermc.io/v2/projects/paper/versions/1.14.4/builds/243/downloads/paper-1.14.4-243.jar",
    # ── 1.13.x ──────────────────────────────────────────────────────
    "1.13.2": "https://api.papermc.io/v2/projects/paper/versions/1.13.2/builds/657/downloads/paper-1.13.2-657.jar",
    # ── 1.12.x ──────────────────────────────────────────────────────
    "1.12.2": "https://api.papermc.io/v2/projects/paper/versions/1.12.2/builds/1620/downloads/paper-1.12.2-1620.jar",
    "1.12.1": "https://api.papermc.io/v2/projects/paper/versions/1.12.1/builds/1169/downloads/paper-1.12.1-1169.jar",
    # ── 1.11.x ──────────────────────────────────────────────────────
    "1.11.2": "https://api.papermc.io/v2/projects/paper/versions/1.11.2/builds/1106/downloads/paper-1.11.2-1106.jar",
    # ── 1.10.x ──────────────────────────────────────────────────────
    "1.10.2": "https://api.papermc.io/v2/projects/paper/versions/1.10.2/builds/918/downloads/paper-1.10.2-918.jar",
    # ── 1.9.x ───────────────────────────────────────────────────────
    "1.9.4":  "https://api.papermc.io/v2/projects/paper/versions/1.9.4/builds/775/downloads/paper-1.9.4-775.jar",
    # ── 1.8.x ───────────────────────────────────────────────────────
    "1.8.8":  "https://api.papermc.io/v2/projects/paper/versions/1.8.8/builds/445/downloads/paper-1.8.8-445.jar",
}

# Forge — installer-based, runs --installServer
FORGE_VERSIONS = {
    # ── 1.21.x ──────────────────────────────────────────────────────
    "1.21.4": ("1.21.4-54.1.0",  "https://maven.minecraftforge.net/net/minecraftforge/forge/1.21.4-54.1.0/forge-1.21.4-54.1.0-installer.jar"),
    "1.21.1": ("1.21.1-52.0.33", "https://maven.minecraftforge.net/net/minecraftforge/forge/1.21.1-52.0.33/forge-1.21.1-52.0.33-installer.jar"),
    "1.21":   ("1.21-51.0.33",   "https://maven.minecraftforge.net/net/minecraftforge/forge/1.21-51.0.33/forge-1.21-51.0.33-installer.jar"),
    # ── 1.20.x ──────────────────────────────────────────────────────
    "1.20.6": ("1.20.6-50.1.0",  "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.6-50.1.0/forge-1.20.6-50.1.0-installer.jar"),
    "1.20.4": ("1.20.4-49.1.0",  "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.4-49.1.0/forge-1.20.4-49.1.0-installer.jar"),
    "1.20.2": ("1.20.2-48.1.0",  "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.2-48.1.0/forge-1.20.2-48.1.0-installer.jar"),
    "1.20.1": ("1.20.1-47.3.0",  "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.3.0/forge-1.20.1-47.3.0-installer.jar"),
    # ── 1.19.x ──────────────────────────────────────────────────────
    "1.19.4": ("1.19.4-45.3.0",  "https://maven.minecraftforge.net/net/minecraftforge/forge/1.19.4-45.3.0/forge-1.19.4-45.3.0-installer.jar"),
    "1.19.2": ("1.19.2-43.3.14", "https://maven.minecraftforge.net/net/minecraftforge/forge/1.19.2-43.3.14/forge-1.19.2-43.3.14-installer.jar"),
    # ── 1.18.x ──────────────────────────────────────────────────────
    "1.18.2": ("1.18.2-40.3.0",  "https://maven.minecraftforge.net/net/minecraftforge/forge/1.18.2-40.3.0/forge-1.18.2-40.3.0-installer.jar"),
    "1.18.1": ("1.18.1-39.1.2",  "https://maven.minecraftforge.net/net/minecraftforge/forge/1.18.1-39.1.2/forge-1.18.1-39.1.2-installer.jar"),
    # ── 1.17.x ──────────────────────────────────────────────────────
    "1.17.1": ("1.17.1-37.1.1",  "https://maven.minecraftforge.net/net/minecraftforge/forge/1.17.1-37.1.1/forge-1.17.1-37.1.1-installer.jar"),
    # ── 1.16.x ──────────────────────────────────────────────────────
    "1.16.5": ("1.16.5-36.2.42", "https://maven.minecraftforge.net/net/minecraftforge/forge/1.16.5-36.2.42/forge-1.16.5-36.2.42-installer.jar"),
    "1.16.4": ("1.16.4-35.1.37", "https://maven.minecraftforge.net/net/minecraftforge/forge/1.16.4-35.1.37/forge-1.16.4-35.1.37-installer.jar"),
    "1.16.3": ("1.16.3-34.1.42", "https://maven.minecraftforge.net/net/minecraftforge/forge/1.16.3-34.1.42/forge-1.16.3-34.1.42-installer.jar"),
    "1.16.2": ("1.16.2-33.0.61", "https://maven.minecraftforge.net/net/minecraftforge/forge/1.16.2-33.0.61/forge-1.16.2-33.0.61-installer.jar"),
    "1.16.1": ("1.16.1-32.0.108","https://maven.minecraftforge.net/net/minecraftforge/forge/1.16.1-32.0.108/forge-1.16.1-32.0.108-installer.jar"),
    # ── 1.15.x ──────────────────────────────────────────────────────
    "1.15.2": ("1.15.2-31.2.57", "https://maven.minecraftforge.net/net/minecraftforge/forge/1.15.2-31.2.57/forge-1.15.2-31.2.57-installer.jar"),
    "1.15.1": ("1.15.1-30.0.51", "https://maven.minecraftforge.net/net/minecraftforge/forge/1.15.1-30.0.51/forge-1.15.1-30.0.51-installer.jar"),
    # ── 1.14.x ──────────────────────────────────────────────────────
    "1.14.4": ("1.14.4-28.2.26", "https://maven.minecraftforge.net/net/minecraftforge/forge/1.14.4-28.2.26/forge-1.14.4-28.2.26-installer.jar"),
    # ── 1.12.x ──────────────────────────────────────────────────────
    "1.12.2": ("1.12.2-14.23.5.2860","https://maven.minecraftforge.net/net/minecraftforge/forge/1.12.2-14.23.5.2860/forge-1.12.2-14.23.5.2860-installer.jar"),
    "1.12.1": ("1.12.1-14.22.1.2485","https://maven.minecraftforge.net/net/minecraftforge/forge/1.12.1-14.22.1.2485/forge-1.12.1-14.22.1.2485-installer.jar"),
    "1.12":   ("1.12-14.21.1.2443",  "https://maven.minecraftforge.net/net/minecraftforge/forge/1.12-14.21.1.2443/forge-1.12-14.21.1.2443-installer.jar"),
    # ── 1.11.x ──────────────────────────────────────────────────────
    "1.11.2": ("1.11.2-13.20.1.2588","https://maven.minecraftforge.net/net/minecraftforge/forge/1.11.2-13.20.1.2588/forge-1.11.2-13.20.1.2588-installer.jar"),
    # ── 1.10.x ──────────────────────────────────────────────────────
    "1.10.2": ("1.10.2-12.18.3.2511","https://maven.minecraftforge.net/net/minecraftforge/forge/1.10.2-12.18.3.2511/forge-1.10.2-12.18.3.2511-installer.jar"),
    # ── 1.9.x ───────────────────────────────────────────────────────
    "1.9.4":  ("1.9.4-12.17.0.2317", "https://maven.minecraftforge.net/net/minecraftforge/forge/1.9.4-12.17.0.2317/forge-1.9.4-12.17.0.2317-installer.jar"),
    # ── 1.8.x ───────────────────────────────────────────────────────
    "1.8.9":  ("1.8.9-11.15.1.2318-1.8.9","https://maven.minecraftforge.net/net/minecraftforge/forge/1.8.9-11.15.1.2318-1.8.9/forge-1.8.9-11.15.1.2318-1.8.9-installer.jar"),
}


LANGS = {
    "🇬🇧 English": {
        "title": "Setup & Manager", "server_info": "SERVER INFO",
        "local_lbl": "🏠  For local multiplayer", "local_sub": "Same Wi-Fi / home network",
        "public_lbl": "🌍  For public (internet)", "public_sub": "Requires port forward on router",
        "copy": "copy", "server_type": "SERVER TYPE",
        "paper_desc": "Plugins · High performance · No mods",
        "forge_desc": "Mods .jar · More content · Requires installer",
        "basic": "BASIC", "folder": "Folder", "message": "Message", "port": "Port", "version": "Version",
        "world": "WORLD", "gamemode": "Gamemode", "difficulty": "Difficulty", "seed": "Seed",
        "players": "PLAYERS", "max_players": "Max players", "operators": "Operators", "ops_hint": " comma separated",
        "pvp": "PvP", "whitelist": "Whitelist", "hardcore": "Hardcore", "flight": "Allow flight", "online": "Online mode",
        "server": "SERVER", "ram": "RAM (GB)", "cmd_blocks": "Command blocks", "force_gm": "Force gamemode",
        "mods": "MODS", "mods_hint": "Add .jar mod files to install on the server.",
        "add_mod": "+ Add mod", "remove_mod": "x Remove", "output": "OUTPUT",
        "create_btn": "Create Server ->", "working": "Working...",
        "send": "Send", "cmd_placeholder": "Type a command...",
        "offline": "Offline", "starting": "Starting...", "online_status": "Online",
        "start": "▶  Start", "stop": "■  Stop",
        "version_lbl": "Version", "lang_lbl": "Language",
        "err_no_folder": "Folder not found. Create the server first.",
        "err_no_jar": "No JAR found in folder.",
        "err_java": "Java not found. Install Java 17+.",
        "err_not_running": "Server is not running.",
        "err_cmd": "Error sending command: ",
        "stop_confirm_title": "Server running",
        "stop_confirm_msg": "Server is still running. Stop and exit?",
        "overwrite_title": "Folder exists", "overwrite_msg": "already exists. Overwrite?",
        "done_title": "Done!", "done_msg": "Server created!\n\nLocal:   {local}\nPublic: {public}\n\nPress Start to launch.",
        "stopping": "Stopping server...", "stopped": "Server stopped.",
        "exited": "Server process exited.", "starting_log": "Starting server...",
        "java_not_found": "Java not found! Install Java 17+.",
        "folder_created": "Folder created: ", "java_ok": "Java: ",
        "dl_paper": "Downloading PaperMC {}...", "dl_done": "Download complete.",
        "eula_ok": "eula.txt accepted", "props_ok": "server.properties created",
        "scripts_ok": "Start scripts created", "ops_ok": "Operators: ",
        "dl_forge": "Downloading Forge {} installer...", "installer_dl": "Installer downloaded.",
        "installing_forge": "Installing Forge (may take a while)...", "forge_ok": "Forge installed.",
        "forge_fail": "Forge installation failed.",
        "copying_mods": "Copying {} mod(s)...", "mods_folder": "mods/ folder created.",
        "ready_log": "-- Server ready! --", "start_hint": "Press Start to launch.",
        "na_plugins": "N/A (plugins)",
    },
    "🇵🇹 Português": {
        "title": "Configuração & Gestor", "server_info": "INFO DO SERVIDOR",
        "local_lbl": "🏠  Para multijogador local", "local_sub": "Same Wi-Fi / home network",
        "public_lbl": "🌍  Para público (internet)", "public_sub": "Requires port forwarding on router",
        "copy": "copy", "server_type": "TIPO DE SERVIDOR",
        "paper_desc": "Plugins · High performance · No mods",
        "forge_desc": "Mods .jar · Mais conteúdo · Requer instalador",
        "basic": "BÁSICO", "folder": "Folder", "message": "Message", "port": "Port", "version": "Versão",
        "world": "MUNDO", "gamemode": "Gamemode", "difficulty": "Difficulty", "seed": "Seed",
        "players": "JOGADORES", "max_players": "Max players", "operators": "Operators", "ops_hint": " separados por vírgula",
        "pvp": "PvP", "whitelist": "Whitelist", "hardcore": "Hardcore", "flight": "Allow flight", "online": "Online mode",
        "server": "SERVIDOR", "ram": "RAM (GB)", "cmd_blocks": "Command blocks", "force_gm": "Force gamemode",
        "mods": "MODS", "mods_hint": "Adiciona ficheiros .jar de mods para instalar no servidor.",
        "add_mod": "+ Add mod", "remove_mod": "x Remove", "output": "OUTPUT",
        "create_btn": "Create Server ->", "working": "Working...",
        "send": "Send", "cmd_placeholder": "Escreve um comando...",
        "offline": "Offline", "starting": "Starting...", "online_status": "Online",
        "start": "▶  Start", "stop": "■  Stop",
        "version_lbl": "Versão", "lang_lbl": "Idioma",
        "err_no_folder": "Pasta não encontrada. Cria o servidor primeiro.",
        "err_no_jar": "No JAR found in folder.",
        "err_java": "Java não encontrado. Instala Java 17+.",
        "err_not_running": "Servidor não está a correr.",
        "err_cmd": "Error sending command: ",
        "stop_confirm_title": "Server running",
        "stop_confirm_msg": "O servidor ainda está a correr. Parar e sair?",
        "overwrite_title": "Folder exists", "overwrite_msg": "já existe. Substituir?",
        "done_title": "Done!", "done_msg": "Server created!\n\nLocal:   {local}\nPúblico: {public}\n\nPress Start to launch.",
        "stopping": "Stopping server...", "stopped": "Server stopped.",
        "exited": "Server stopped.", "starting_log": "Starting server...",
        "java_not_found": "Java não encontrado! Instala Java 17+.",
        "folder_created": "Folder created: ", "java_ok": "Java: ",
        "dl_paper": "Downloading PaperMC {}...", "dl_done": "Download concluído.",
        "eula_ok": "eula.txt accepted", "props_ok": "server.properties created",
        "scripts_ok": "Start scripts created", "ops_ok": "Operators: ",
        "dl_forge": "Downloading Forge {} installer...", "installer_dl": "Installer downloaded.",
        "installing_forge": "Installing Forge (may take a while)...", "forge_ok": "Forge installed.",
        "forge_fail": "Instalação do Forge falhou.",
        "copying_mods": "Copying {} mod(s)...", "mods_folder": "Folder 'mods/' created.",
        "ready_log": "-- Server ready! --", "start_hint": "Press Start to launch.",
        "na_plugins": "N/A (plugins)",
    },
    "🇪🇸 Español": {
        "title": "Configuración & Gestor", "server_info": "INFO DEL SERVIDOR",
        "local_lbl": "🏠  Para multijugador local", "local_sub": "Misma red Wi-Fi / casa",
        "public_lbl": "🌍  Para público (internet)", "public_sub": "Requiere reenvío de puertos",
        "copy": "copy", "server_type": "TIPO DE SERVIDOR",
        "paper_desc": "Plugins · Alto rendimiento · Sin mods",
        "forge_desc": "Mods .jar · Más contenido · Requiere instalador",
        "basic": "BÁSICO", "folder": "Carpeta", "message": "Mensaje", "port": "Puerto", "version": "Versión",
        "world": "MUNDO", "gamemode": "Modo de juego", "difficulty": "Dificultad", "seed": "Semilla",
        "players": "JUGADORES", "max_players": "Máx. jugadores", "operators": "Operators", "ops_hint": " separados por coma",
        "pvp": "PvP", "whitelist": "Lista blanca", "hardcore": "Hardcore", "flight": "Permitir vuelo", "online": "Modo online",
        "server": "SERVIDOR", "ram": "RAM (GB)", "cmd_blocks": "Bloques de comandos", "force_gm": "Forzar modo de juego",
        "mods": "MODS", "mods_hint": "Añade archivos .jar de mods para instalar en el servidor.",
        "add_mod": "+ Añadir mod", "remove_mod": "x Eliminar", "output": "SALIDA",
        "create_btn": "Crear Servidor ->", "working": "Trabajando...",
        "send": "Send", "cmd_placeholder": "Escribe un comando...",
        "offline": "Desconectado", "starting": "Iniciando...", "online_status": "En línea",
        "start": "▶  Iniciar", "stop": "■  Detener",
        "version_lbl": "Versión", "lang_lbl": "Idioma",
        "err_no_folder": "Carpeta no encontrada. Crea el servidor primero.",
        "err_no_jar": "No se encontró JAR en la carpeta.",
        "err_java": "Java no encontrado. Instala Java 17+.",
        "err_not_running": "El servidor no está en ejecución.",
        "err_cmd": "Error al enviar comando: ",
        "stop_confirm_title": "Servidor activo",
        "stop_confirm_msg": "El servidor sigue en ejecución. ¿Detener y salir?",
        "overwrite_title": "Carpeta existe", "overwrite_msg": "ya existe. ¿Sobreescribir?",
        "done_title": "¡Listo!", "done_msg": "¡Servidor creado!\n\nLocal:   {local}\nPúblico: {public}\n\nPulsa Iniciar para arrancar.",
        "stopping": "Deteniendo servidor...", "stopped": "Servidor detenido.",
        "exited": "Proceso del servidor terminado.", "starting_log": "Iniciando servidor...",
        "java_not_found": "¡Java no encontrado! Instala Java 17+.",
        "folder_created": "Carpeta creada: ", "java_ok": "Java: ",
        "dl_paper": "Descargando PaperMC {}...", "dl_done": "Descarga completa.",
        "eula_ok": "eula.txt aceptado", "props_ok": "server.properties creado",
        "scripts_ok": "Scripts de inicio creados", "ops_ok": "Operators: ",
        "dl_forge": "Descargando instalador Forge {}...", "installer_dl": "Instalador descargado.",
        "installing_forge": "Instalando Forge (puede tardar)...", "forge_ok": "Forge installed.",
        "forge_fail": "La instalación de Forge falló.",
        "copying_mods": "Copiando {} mod(s)...", "mods_folder": "Carpeta 'mods/' creada.",
        "ready_log": "-- ¡Servidor listo! --", "start_hint": "Pulsa Iniciar para arrancar.",
        "na_plugins": "N/A (plugins)",
    },
    "🇩🇪 Deutsch": {
        "title": "Einrichtung & Verwaltung", "server_info": "SERVER-INFO",
        "local_lbl": "🏠  Für lokales Multiplayer", "local_sub": "Gleiches WLAN / Heimnetz",
        "public_lbl": "🌍  Für öffentlich (Internet)", "public_sub": "Portweiterleitung am Router nötig",
        "copy": "kopieren", "server_type": "SERVERTYP",
        "paper_desc": "Plugins · Hohe Performance · Keine Mods",
        "forge_desc": "Mods .jar · Mehr Inhalt · Installer nötig",
        "basic": "GRUNDLEGEND", "folder": "Ordner", "message": "Nachricht", "port": "Port", "version": "Version",
        "world": "WELT", "gamemode": "Spielmodus", "difficulty": "Schwierigkeit", "seed": "Welt-Seed",
        "players": "SPIELER", "max_players": "Max. Spieler", "operators": "Operatoren", "ops_hint": " kommagetrennt",
        "pvp": "PvP", "whitelist": "Whitelist", "hardcore": "Hardcore", "flight": "Fliegen erlauben", "online": "Online-Modus",
        "server": "SERVER", "ram": "RAM (GB)", "cmd_blocks": "Befehlsblöcke", "force_gm": "Spielmodus erzwingen",
        "mods": "MODS", "mods_hint": "Füge .jar Mod-Dateien zum Installieren hinzu.",
        "add_mod": "+ Mod hinzufügen", "remove_mod": "x Entfernen", "output": "AUSGABE",
        "create_btn": "Server erstellen ->", "working": "Lädt...",
        "send": "Senden", "cmd_placeholder": "Befehl eingeben...",
        "offline": "Offline", "starting": "Startet...", "online_status": "Online",
        "start": "▶  Starten", "stop": "■  Stoppen",
        "version_lbl": "Version", "lang_lbl": "Sprache",
        "err_no_folder": "Ordner nicht gefunden. Erstelle zuerst den Server.",
        "err_no_jar": "Kein JAR im Ordner gefunden.",
        "err_java": "Java nicht gefunden. Installiere Java 17+.",
        "err_not_running": "Server läuft nicht.",
        "err_cmd": "Fehler beim Senden: ",
        "stop_confirm_title": "Server aktiv",
        "stop_confirm_msg": "Server läuft noch. Stoppen und beenden?",
        "overwrite_title": "Ordner existiert", "overwrite_msg": "existiert bereits. Überschreiben?",
        "done_title": "Fertig!", "done_msg": "Server erstellt!\n\nLokal:    {local}\nÖffentl.: {public}\n\nDrücke Starten zum Starten.",
        "stopping": "Server wird gestoppt...", "stopped": "Server gestoppt.",
        "exited": "Serverprozess beendet.", "starting_log": "Server wird gestartet...",
        "java_not_found": "Java nicht gefunden! Installiere Java 17+.",
        "folder_created": "Ordner erstellt: ", "java_ok": "Java: ",
        "dl_paper": "PaperMC {} wird heruntergeladen...", "dl_done": "Download abgeschlossen.",
        "eula_ok": "eula.txt akzeptiert", "props_ok": "server.properties erstellt",
        "scripts_ok": "Startskripte erstellt", "ops_ok": "Operatoren: ",
        "dl_forge": "Forge {} Installer wird heruntergeladen...", "installer_dl": "Installer heruntergeladen.",
        "installing_forge": "Forge wird installiert (kann dauern)...", "forge_ok": "Forge installiert.",
        "forge_fail": "Forge-Installation fehlgeschlagen.",
        "copying_mods": "{} Mod(s) werden kopiert...", "mods_folder": "Ordner 'mods/' erstellt.",
        "ready_log": "-- Server bereit! --", "start_hint": "Drücke Starten zum Starten.",
        "na_plugins": "N/A (Plugins)",
    },
    "🇫🇷 Français": {
        "title": "Configuration & Gestion", "server_info": "INFOS DU SERVEUR",
        "local_lbl": "🏠  Pour multijoueur local", "local_sub": "Même réseau Wi-Fi / maison",
        "public_lbl": "🌍  Pour public (internet)", "public_sub": "Redirection de port requise",
        "copy": "copier", "server_type": "TYPE DE SERVEUR",
        "paper_desc": "Plugins · Haute performance · Sans mods",
        "forge_desc": "Mods .jar · Plus de contenu · Installateur requis",
        "basic": "BASIQUE", "folder": "Dossier", "message": "Message", "port": "Port", "version": "Version",
        "world": "MONDE", "gamemode": "Mode de jeu", "difficulty": "Difficulté", "seed": "Graine",
        "players": "JOUEURS", "max_players": "Max joueurs", "operators": "Opérateurs", "ops_hint": " séparés par virgule",
        "pvp": "PvP", "whitelist": "Liste blanche", "hardcore": "Hardcore", "flight": "Vol autorisé", "online": "Mode en ligne",
        "server": "SERVEUR", "ram": "RAM (Go)", "cmd_blocks": "Blocs de commandes", "force_gm": "Forcer le mode de jeu",
        "mods": "MODS", "mods_hint": "Ajoute des fichiers .jar de mods à installer sur le serveur.",
        "add_mod": "+ Ajouter mod", "remove_mod": "x Supprimer", "output": "SORTIE",
        "create_btn": "Créer le serveur ->", "working": "En cours...",
        "send": "Envoyer", "cmd_placeholder": "Entrez une commande...",
        "offline": "Hors ligne", "starting": "Démarrage...", "online_status": "En ligne",
        "start": "▶  Démarrer", "stop": "■  Arrêter",
        "version_lbl": "Version", "lang_lbl": "Langue",
        "err_no_folder": "Dossier introuvable. Créez d'abord le serveur.",
        "err_no_jar": "Aucun JAR trouvé dans le dossier.",
        "err_java": "Java introuvable. Installez Java 17+.",
        "err_not_running": "Le serveur ne tourne pas.",
        "err_cmd": "Erreur lors de l'envoi: ",
        "stop_confirm_title": "Serveur actif",
        "stop_confirm_msg": "Le serveur tourne encore. Arrêter et quitter?",
        "overwrite_title": "Dossier existant", "overwrite_msg": "existe déjà. Écraser?",
        "done_title": "Terminé!", "done_msg": "Serveur créé!\n\nLocal:   {local}\nPublic: {public}\n\nCliquez Démarrer pour lancer.",
        "stopping": "Arrêt du serveur...", "stopped": "Serveur arrêté.",
        "exited": "Processus serveur terminé.", "starting_log": "Démarrage du serveur...",
        "java_not_found": "Java introuvable! Installez Java 17+.",
        "folder_created": "Dossier créé: ", "java_ok": "Java: ",
        "dl_paper": "Téléchargement PaperMC {}...", "dl_done": "Téléchargement terminé.",
        "eula_ok": "eula.txt accepté", "props_ok": "server.properties créé",
        "scripts_ok": "Scripts de démarrage créés", "ops_ok": "Opérateurs: ",
        "dl_forge": "Téléchargement installateur Forge {}...", "installer_dl": "Installateur téléchargé.",
        "installing_forge": "Installation Forge (peut prendre du temps)...", "forge_ok": "Forge installé.",
        "forge_fail": "Échec de l'installation Forge.",
        "copying_mods": "Copie de {} mod(s)...", "mods_folder": "Dossier 'mods/' créé.",
        "ready_log": "-- Serveur prêt! --", "start_hint": "Cliquez Démarrer pour lancer.",
        "na_plugins": "N/A (plugins)",
    },
}

def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "127.0.0.1"


def get_public_ip():
    try:
        with urllib.request.urlopen("https://api.ipify.org", timeout=5) as r:
            return r.read().decode()
    except Exception:
        return "unavailable"


def ping_server(host, port):
    try:
        s = socket.create_connection((host, int(port)), timeout=2)
        s.close()
        return True
    except Exception:
        return False


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minecraft Server")
        self.geometry("740x1060")
        self.minsize(680, 900)
        self.configure(bg=BG)

        self._server_proc   = None
        self._server_folder = None
        self._server_port   = "25565"
        self._status_job    = None
        self._mods_list     = []
        self._server_type   = tk.StringVar(value="paper")
        self._lang_key      = "🇬🇧 English"
        self._T             = LANGS[self._lang_key]
        self._ui_refs       = {}

        # server info vars (populated after create)
        self._info_local   = tk.StringVar(value="—")
        self._info_public  = tk.StringVar(value="—")
        self._info_version = tk.StringVar(value="—")
        self._info_type    = tk.StringVar(value="—")
        self._info_gm      = tk.StringVar(value="—")
        self._info_diff    = tk.StringVar(value="—")
        self._info_maxp    = tk.StringVar(value="—")
        self._info_mods    = tk.StringVar(value="—")
        self._info_folder  = tk.StringVar(value="—")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox",
                         fieldbackground=CARD, background=CARD,
                         foreground=TEXT, bordercolor=BORDER,
                         arrowcolor=MUTED, selectbackground=CARD,
                         selectforeground=TEXT)
        style.map("TCombobox",
                  fieldbackground=[("readonly", CARD)],
                  foreground=[("readonly", TEXT)])
        style.configure("TProgressbar",
                         troughcolor=CARD, background=GREEN,
                         bordercolor=BORDER, lightcolor=GREEN, darkcolor=GREEN)
        style.configure("TCheckbutton",
                         background=PANEL, foreground=TEXT, font=FONT,
                         focuscolor=PANEL, indicatorcolor=CARD,
                         indicatorbackground=CARD)
        style.map("TCheckbutton",
                  background=[("active", PANEL)],
                  indicatorcolor=[("selected", GREEN), ("!selected", CARD)])

        self.local_ip  = get_local_ip()
        self.public_ip = "loading..."
        self._build()
        threading.Thread(target=self._load_public_ip, daemon=True).start()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build(self):

        # ── Header ────────────────────────────────────────────────────
        hdr = tk.Frame(self, bg=PANEL, pady=18)
        hdr.pack(fill="x")

        # Language selector (top-right)
        lang_frame = tk.Frame(hdr, bg=PANEL)
        lang_frame.pack(side="right", padx=16, anchor="n")
        self._ui_refs["lang_lbl"] = tk.Label(lang_frame, text=self._T["lang_lbl"],
                 font=("Segoe UI", 8), fg=MUTED, bg=PANEL)
        self._ui_refs["lang_lbl"].pack(anchor="e")
        lang_var = tk.StringVar(value=self._lang_key)
        lang_combo = ttk.Combobox(lang_frame, textvariable=lang_var,
                                   values=list(LANGS.keys()),
                                   state="readonly", font=("Segoe UI", 9), width=14)
        lang_combo.pack()

        def on_lang_change(e=None):
            self._lang_key = lang_var.get()
            self._T = LANGS[self._lang_key]
            self._apply_lang()

        lang_combo.bind("<<ComboboxSelected>>", on_lang_change)

        # Centered title
        center = tk.Frame(hdr, bg=PANEL)
        center.pack(expand=True)
        tk.Label(center, text="⛏  Minecraft Server",
                 font=("Segoe UI", 17, "bold"), fg=GREEN, bg=PANEL).pack()
        self._ui_refs["subtitle"] = tk.Label(center, text=self._T["title"],
                 font=("Segoe UI", 9), fg=MUTED, bg=PANEL)
        self._ui_refs["subtitle"].pack(pady=(2, 0))

        # ── Status bar ────────────────────────────────────────────────
        status_bar = tk.Frame(self, bg=CARD, pady=10, padx=20)
        status_bar.pack(fill="x")

        dot_frame = tk.Frame(status_bar, bg=CARD)
        dot_frame.pack(side="left")
        self._dot = tk.Label(dot_frame, text="●", font=("Segoe UI", 16), fg=MUTED, bg=CARD)
        self._dot.pack(side="left")
        self._status_label = tk.Label(dot_frame, text=self._T["offline"],
                                       font=("Segoe UI", 10, "bold"), fg=MUTED, bg=CARD)
        self._status_label.pack(side="left", padx=(6, 0))

        btn_group = tk.Frame(status_bar, bg=CARD)
        btn_group.pack(side="right")

        self.btn_start = tk.Button(
            btn_group, text=self._T["start"],
            font=("Segoe UI", 10, "bold"),
            bg=CARD, fg=MUTED,
            activebackground=GREEN_DK, activeforeground="#0c1a10",
            relief="flat", padx=16, pady=7, cursor="hand2",
            state="disabled", command=self._start_server)
        self.btn_start.pack(side="left", padx=(0, 8))

        self.btn_stop = tk.Button(
            btn_group, text=self._T["stop"],
            font=("Segoe UI", 10, "bold"),
            bg=CARD, fg=MUTED,
            activebackground=RED_DK, activeforeground=TEXT,
            relief="flat", padx=16, pady=7, cursor="hand2",
            state="disabled", command=self._stop_server)
        self.btn_stop.pack(side="left")

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # ── Scrollable body ───────────────────────────────────────────
        canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        sb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        body = tk.Frame(canvas, bg=BG)
        win_id = canvas.create_window((0, 0), window=body, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))
        body.bind("<Configure>",   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind_all("<MouseWheel>",
                         lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        # ── Helpers ───────────────────────────────────────────────────
        _section_labels = {}
        def section(title, key=None):
            wrapper = tk.Frame(body, bg=BG)
            wrapper.pack(fill="x", padx=20, pady=(14, 0))
            lbl = tk.Label(wrapper, text=title.upper(),
                     font=("Segoe UI", 8, "bold"), fg=MUTED, bg=BG)
            lbl.pack(anchor="w", pady=(0, 6))
            if key:
                _section_labels[key] = lbl
                self._ui_refs[key] = lbl
            card = tk.Frame(wrapper, bg=PANEL, padx=18, pady=14)
            card.pack(fill="x")
            return card

        def field(parent, label, widget_fn, key=None, **kw):
            row = tk.Frame(parent, bg=PANEL)
            row.pack(fill="x", pady=5)
            lbl = tk.Label(row, text=label, width=16, anchor="w",
                     font=FONT, fg=TEXT, bg=PANEL)
            lbl.pack(side="left")
            if key:
                self._ui_refs[key] = lbl
            w = widget_fn(row, **kw)
            w.pack(side="left", fill="x", expand=True)
            return w

        def make_entry(parent, default="", **kw):
            e = tk.Entry(parent, bg=CARD, fg=TEXT, insertbackground=TEXT,
                          relief="flat", font=FONT, bd=0,
                          highlightthickness=1, highlightbackground=BORDER,
                          highlightcolor=GREEN, **kw)
            e.insert(0, default)
            return e

        def make_combo(parent, values, default=0):
            v = tk.StringVar(value=values[default])
            c = ttk.Combobox(parent, textvariable=v, values=values,
                              state="readonly", font=FONT)
            c._var = v
            return c

        _chk_widgets = []
        def make_checks(parent, items):
            row = tk.Frame(parent, bg=PANEL)
            row.pack(fill="x", pady=4)
            vars_ = []
            for label, default in items:
                v = tk.BooleanVar(value=default)
                w = ttk.Checkbutton(row, text=label, variable=v)
                w.pack(side="left", padx=(0, 14))
                vars_.append(v)
                _chk_widgets.append((w, label))
            return vars_

        # ══ Server Info Card (always visible, updates after create) ═══
        info_wrapper = tk.Frame(body, bg=BG)
        info_wrapper.pack(fill="x", padx=20, pady=(16, 0))
        self._ui_refs["info_sec"] = tk.Label(info_wrapper, text=self._T["server_info"],
                 font=("Segoe UI", 8, "bold"), fg=MUTED, bg=BG).pack(anchor="w", pady=(0, 6))

        info_card = tk.Frame(info_wrapper, bg=PANEL, padx=18, pady=16)
        info_card.pack(fill="x")

        # Connection block
        conn_frame = tk.Frame(info_card, bg=PANEL)
        conn_frame.pack(fill="x", pady=(0, 12))

        # Local multiplayer
        local_blk = tk.Frame(conn_frame, bg=CARD, padx=14, pady=12)
        local_blk.pack(side="left", expand=True, fill="both", padx=(0, 8))
        self._ui_refs["local_lbl"] = tk.Label(local_blk, text=self._T["local_lbl"],
                 font=("Segoe UI", 8, "bold"), fg=MUTED, bg=CARD).pack(anchor="w")
        self._lbl_local = tk.Label(local_blk, textvariable=self._info_local,
                                    font=("Consolas", 13, "bold"), fg=GREEN, bg=CARD)
        self._lbl_local.pack(anchor="w", pady=(4, 0))
        self._ui_refs["local_sub"] = tk.Label(local_blk, text=self._T["local_sub"],
                 font=("Segoe UI", 8), fg=MUTED, bg=CARD).pack(anchor="w")

        # Copy button local
        self._ui_refs["copy_local"] = tk.Button(local_blk, text=self._T["copy"], font=("Segoe UI", 8),
                  bg=BORDER, fg=MUTED, relief="flat", padx=6, pady=2, cursor="hand2",
                  command=lambda: self._copy(self._info_local.get()))
        self._ui_refs["copy_local"].pack(anchor="w", pady=(6, 0))

        # Public
        pub_blk = tk.Frame(conn_frame, bg=CARD, padx=14, pady=12)
        pub_blk.pack(side="left", expand=True, fill="both")
        self._ui_refs["public_lbl"] = tk.Label(pub_blk, text=self._T["public_lbl"],
                 font=("Segoe UI", 8, "bold"), fg=MUTED, bg=CARD).pack(anchor="w")
        self._lbl_public = tk.Label(pub_blk, textvariable=self._info_public,
                                     font=("Consolas", 13, "bold"), fg=ORANGE, bg=CARD)
        self._lbl_public.pack(anchor="w", pady=(4, 0))
        self._ui_refs["public_sub"] = tk.Label(pub_blk, text=self._T["public_sub"],
                 font=("Segoe UI", 8), fg=MUTED, bg=CARD).pack(anchor="w")

        self._ui_refs["copy_public"] = tk.Button(pub_blk, text=self._T["copy"], font=("Segoe UI", 8),
                  bg=BORDER, fg=MUTED, relief="flat", padx=6, pady=2, cursor="hand2",
                  command=lambda: self._copy(self._info_public.get()))
        self._ui_refs["copy_public"].pack(anchor="w", pady=(6, 0))

        # Divider
        tk.Frame(info_card, bg=BORDER, height=1).pack(fill="x", pady=(0, 12))

        # Details grid
        details = tk.Frame(info_card, bg=PANEL)
        details.pack(fill="x")

        def info_item(parent, label, var, col):
            f = tk.Frame(parent, bg=PANEL)
            f.grid(row=0, column=col, sticky="w", padx=(0, 30))
            tk.Label(f, text=label, font=("Segoe UI", 8), fg=MUTED, bg=PANEL).pack(anchor="w")
            tk.Label(f, textvariable=var, font=("Segoe UI", 10, "bold"), fg=TEXT, bg=PANEL).pack(anchor="w")

        info_item(details, "Versão",    self._info_version, 0)
        info_item(details, "Tipo",      self._info_type,    1)
        info_item(details, "Gamemode",  self._info_gm,      2)
        info_item(details, "Difficulty", self._info_diff,    3)
        info_item(details, "Players", self._info_maxp,    4)
        info_item(details, "Mods",      self._info_mods,    5)

        # Folder path
        folder_row = tk.Frame(info_card, bg=PANEL)
        folder_row.pack(fill="x", pady=(10, 0))
        tk.Label(folder_row, text="📁", font=("Segoe UI", 9), fg=MUTED, bg=PANEL).pack(side="left")
        tk.Label(folder_row, textvariable=self._info_folder,
                 font=("Consolas", 8), fg=MUTED, bg=PANEL).pack(side="left", padx=(6, 0))

        # ══ Server Type ════════════════════════════════════════════════
        s0 = section(self._T["server_type"], key="server_type")

        type_row = tk.Frame(s0, bg=PANEL)
        type_row.pack(fill="x", pady=4)

        def make_type_btn(parent, label, value, desc):
            col = tk.Frame(parent, bg=PANEL)
            col.pack(side="left", expand=True, fill="x", padx=(0, 8))

            def update():
                self._server_type.set(value)
                _refresh_type()

            btn = tk.Button(col, text=label,
                             font=("Segoe UI", 11, "bold"),
                             relief="flat", padx=12, pady=10,
                             cursor="hand2", command=update)
            btn.pack(fill="x")
            tk.Label(col, text=desc, font=("Segoe UI", 8),
                     fg=MUTED, bg=PANEL, wraplength=200, justify="center").pack(pady=(4, 0))
            return btn

        self._btn_paper = make_type_btn(type_row, "📄  PaperMC", "paper", self._T["paper_desc"])
        self._btn_forge = make_type_btn(type_row, "🔨  Forge", "forge", self._T["forge_desc"])

        def _refresh_type():
            t = self._server_type.get()
            if t == "paper":
                self._btn_paper.configure(bg=GREEN, fg="#0c1a10")
                self._btn_forge.configure(bg=CARD, fg=MUTED)
                self._mods_frame.pack_forget()
            else:
                self._btn_forge.configure(bg=ORANGE, fg="#1a1200")
                self._btn_paper.configure(bg=CARD, fg=MUTED)
                self._mods_frame.pack(fill="x", padx=20, pady=(14, 0))
            _update_version_list()

        # ══ Basic ══════════════════════════════════════════════════════
        s1 = section(self._T["basic"], key="basic_sec")
        self.e_folder  = field(s1, self._T["folder"],   make_entry, key="f_folder", default="my-server")
        self.e_motd    = field(s1, self._T["message"], make_entry, key="f_motd", default="A Minecraft Server")
        self.e_port    = field(s1, self._T["port"],    make_entry, key="f_port", default="25565")

        # Dynamic version row
        ver_row = tk.Frame(s1, bg=PANEL)
        ver_row.pack(fill="x", pady=5)
        self._ui_refs["f_ver"] = tk.Label(ver_row, text=self._T["version_lbl"], width=16, anchor="w",
                 font=FONT, fg=TEXT, bg=PANEL)
        self._ui_refs["f_ver"].pack(side="left")
        self._version_var = tk.StringVar()
        self._version_combo = ttk.Combobox(ver_row, textvariable=self._version_var,
                                            state="readonly", font=FONT)
        self._version_combo.pack(side="left", fill="x", expand=True)
        self._version_combo._var = self._version_var

        def _update_version_list():
            if self._server_type.get() == "paper":
                vals = list(PAPER_VERSIONS.keys())
            else:
                vals = list(FORGE_VERSIONS.keys())
            self._version_combo["values"] = vals
            self._version_var.set(vals[0])

        # ══ World ══════════════════════════════════════════════════════
        s2 = section(self._T["world"], key="world_sec")
        self.e_gamemode   = field(s2, self._T["gamemode"],    make_combo, key="f_gm",
                                   values=["survival","creative","adventure","spectator"])
        self.e_difficulty = field(s2, self._T["difficulty"], make_combo, key="f_diff",
                                   values=["peaceful","easy","normal","hard"], default=2)
        self.e_seed       = field(s2, self._T["seed"],         make_entry, key="f_seed", default="")

        # ══ Players ════════════════════════════════════════════════════
        s3 = section(self._T["players"], key="players_sec")
        self.e_maxp = field(s3, self._T["max_players"], make_entry, key="f_maxp", default="20")
        pvp, wl, hc, flight, online = make_checks(s3, [
            (self._T["pvp"],          True),
            (self._T["whitelist"],    False),
            (self._T["hardcore"],     False),
            (self._T["flight"], False),
            (self._T["online"],  True),
        ])
        self.chk_pvp = pvp; self.chk_wl = wl; self.chk_hc = hc
        self.chk_flight = flight; self.chk_online = online

        ops_row = tk.Frame(s3, bg=PANEL)
        ops_row.pack(fill="x", pady=(8, 0))
        self._ui_refs["f_ops"] = tk.Label(ops_row, text=self._T["operators"], width=16, anchor="w",
                 font=FONT, fg=TEXT, bg=PANEL).pack(side="left")
        self.e_ops = tk.Entry(ops_row, bg=CARD, fg=TEXT, insertbackground=TEXT,
                               relief="flat", font=FONT, bd=0,
                               highlightthickness=1, highlightbackground=BORDER,
                               highlightcolor=GREEN)
        self.e_ops.pack(side="left", fill="x", expand=True)
        self._ui_refs["ops_hint_lbl"] = tk.Label(ops_row, text=self._T["ops_hint"],
                 font=("Segoe UI", 8), fg=MUTED, bg=PANEL).pack(side="left")

        # ══ Server ═════════════════════════════════════════════════════
        s4 = section(self._T["server"], key="server_sec")
        self.e_ram = field(s4, self._T["ram"], make_combo, key="f_ram",
                            values=["1","2","4","6","8","12","16"], default=1)
        cmds, forcegm = make_checks(s4, [
            (self._T["cmd_blocks"], False),
            (self._T["force_gm"], False),
        ])
        self.chk_cmds = cmds; self.chk_forcegm = forcegm

        # ══ Mods (Forge only) ══════════════════════════════════════════
        mods_wrapper = tk.Frame(body, bg=BG)
        self._mods_frame = mods_wrapper

        self._ui_refs["mods_sec"] = tk.Label(mods_wrapper, text=self._T["mods"].upper(),
                 font=("Segoe UI", 8, "bold"), fg=MUTED, bg=BG).pack(anchor="w", pady=(0, 6))

        mods_card = tk.Frame(mods_wrapper, bg=PANEL, padx=18, pady=14)
        mods_card.pack(fill="x")

        self._ui_refs["mods_hint"] = tk.Label(mods_card, text=self._T["mods_hint"],
                 font=("Segoe UI", 9), fg=MUTED, bg=PANEL)
        self._ui_refs["mods_hint"].pack(anchor="w", pady=(0, 8))

        list_frame = tk.Frame(mods_card, bg=CARD,
                               highlightthickness=1, highlightbackground=BORDER)
        list_frame.pack(fill="x", pady=(0, 8))
        self._mods_listbox = tk.Listbox(
            list_frame, bg=CARD, fg=TEXT, font=("Consolas", 9),
            relief="flat", bd=0, selectbackground=BORDER,
            selectforeground=TEXT, height=5, activestyle="none")
        self._mods_listbox.pack(side="left", fill="both", expand=True, padx=4, pady=4)
        mods_sb2 = tk.Scrollbar(list_frame, orient="vertical",
                                 command=self._mods_listbox.yview)
        mods_sb2.pack(side="right", fill="y")
        self._mods_listbox.configure(yscrollcommand=mods_sb2.set)

        mod_btns = tk.Frame(mods_card, bg=PANEL)
        mod_btns.pack(fill="x")
        self._ui_refs["add_mod"] = tk.Button(mod_btns, text=self._T["add_mod"],
                  font=("Segoe UI", 9, "bold"),
                  bg=BLUE, fg=TEXT, activebackground="#3a78b0",
                  relief="flat", padx=14, pady=6, cursor="hand2",
                  command=self._add_mods).pack(side="left", padx=(0, 8))
        self._ui_refs["remove_mod_btn"] = tk.Button(mod_btns, text=self._T["remove_mod"],
                  font=("Segoe UI", 9),
                  bg=CARD, fg=MUTED, activebackground=RED_DK,
                  relief="flat", padx=14, pady=6, cursor="hand2",
                  command=self._remove_mod).pack(side="left")
        self._mod_count_var = tk.StringVar(value="0 mods")
        tk.Label(mod_btns, textvariable=self._mod_count_var,
                 font=("Segoe UI", 8), fg=MUTED, bg=PANEL).pack(side="right")

        # ══ Output ═════════════════════════════════════════════════════
        s5 = section(self._T["output"], key="output_sec")
        self.progress_var = tk.DoubleVar(value=0)
        ttk.Progressbar(s5, variable=self.progress_var,
                         maximum=100, style="TProgressbar").pack(fill="x", pady=(0, 8))
        self.log = scrolledtext.ScrolledText(
            s5, height=8, bg=CARD, fg=TEXT, font=("Consolas", 9),
            relief="flat", bd=0, insertbackground=TEXT,
            highlightthickness=1, highlightbackground=BORDER, state="disabled")
        self.log.pack(fill="x")

        # Command input bar
        cmd_bar = tk.Frame(s5, bg=CARD,
                            highlightthickness=1, highlightbackground=BORDER)
        cmd_bar.pack(fill="x", pady=(8, 0))

        tk.Label(cmd_bar, text=">", font=("Consolas", 11, "bold"),
                 fg=GREEN, bg=CARD, padx=8).pack(side="left")

        self._cmd_var = tk.StringVar()
        self._cmd_entry = tk.Entry(cmd_bar, textvariable=self._cmd_var,
                                    bg=CARD, fg=TEXT, insertbackground=GREEN,
                                    relief="flat", font=("Consolas", 10), bd=0)
        self._cmd_entry.pack(side="left", fill="x", expand=True, pady=8)
        self._cmd_entry.bind("<Return>", lambda e: self._send_command())
        self._cmd_entry.bind("<Up>",     lambda e: self._cmd_history_up())
        self._cmd_entry.bind("<Down>",   lambda e: self._cmd_history_down())

        self._ui_refs["send_btn"] = tk.Button(cmd_bar, text=self._T["send"],
                  font=("Segoe UI", 9, "bold"),
                  bg=GREEN, fg="#0c1a10", activebackground=GREEN_DK,
                  relief="flat", padx=12, pady=6, cursor="hand2",
                  command=self._send_command).pack(side="right", padx=6, pady=4)

        self._cmd_history = []
        self._cmd_hist_idx = -1

        # ══ Create button ══════════════════════════════════════════════
        btn_frame = tk.Frame(body, bg=BG, pady=18)
        btn_frame.pack(fill="x", padx=20)
        self.btn_create = tk.Button(
            btn_frame, text=self._T["create_btn"],
            font=("Segoe UI", 11, "bold"),
            bg=GREEN, fg="#0c1a10",
            activebackground=GREEN_DK, activeforeground="#0c1a10",
            relief="flat", padx=28, pady=12, cursor="hand2",
            command=self._start_create)
        self.btn_create.pack(side="right")

        tk.Frame(body, bg=BG, height=10).pack()

        # Store checkbox widgets for lang updates
        self._chk_widgets = _chk_widgets

        # Init type
        _refresh_type()
        self._update_version_list = _update_version_list

    def _copy(self, text):
        if text and text != "—":
            self.clipboard_clear()
            self.clipboard_append(text)

    def _ip_text(self):
        return f"Local: {self.local_ip}    Public: {self.public_ip}"

    def _load_public_ip(self):
        self.public_ip = get_public_ip()

    def _log(self, msg, tag="info"):
        self.log.configure(state="normal")
        self.log.tag_config("ok",   foreground=GREEN)
        self.log.tag_config("err",  foreground=RED)
        self.log.tag_config("info", foreground=MUTED)
        self.log.tag_config("srv",  foreground=TEXT)
        self.log.insert("end", msg + "\n", tag)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _progress(self, pct):
        self.progress_var.set(pct)
        self.update_idletasks()

    def _add_mods(self):
        files = filedialog.askopenfilenames(
            title="Select mods (.jar)",
            filetypes=[("Mod JAR", "*.jar"), ("All files", "*.*")])
        for f in files:
            p = Path(f)
            if p not in self._mods_list:
                self._mods_list.append(p)
                self._mods_listbox.insert("end", f"  {p.name}")
        n = len(self._mods_list)
        self._mod_count_var.set(f"{n} mod{'s' if n != 1 else ''}")

    def _remove_mod(self):
        sel = self._mods_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self._mods_listbox.delete(idx)
        self._mods_list.pop(idx)
        n = len(self._mods_list)
        self._mod_count_var.set(f"{n} mod{'s' if n != 1 else ''}")

    def _apply_lang(self):
        T = self._T
        # Section headers
        for key in ["server_info","server_type","basic_sec","world_sec",
                    "players_sec","server_sec","output_sec","mods_sec"]:
            if key in self._ui_refs:
                txt = {
                    "server_info":  T["server_info"],
                    "server_type":  T["server_type"],
                    "basic_sec":    T["basic"].upper(),
                    "world_sec":    T["world"].upper(),
                    "players_sec":  T["players"].upper(),
                    "server_sec":   T["server"].upper(),
                    "output_sec":   T["output"].upper(),
                    "mods_sec":     T["mods"].upper(),
                }.get(key, "")
                self._ui_refs[key].configure(text=txt)
        # Subtitle
        if "subtitle"      in self._ui_refs: self._ui_refs["subtitle"].configure(text=T["title"])
        if "lang_lbl"      in self._ui_refs: self._ui_refs["lang_lbl"].configure(text=T["lang_lbl"])
        # Connection labels
        if "local_lbl"     in self._ui_refs: self._ui_refs["local_lbl"].configure(text=T["local_lbl"])
        if "local_sub"     in self._ui_refs: self._ui_refs["local_sub"].configure(text=T["local_sub"])
        if "public_lbl"    in self._ui_refs: self._ui_refs["public_lbl"].configure(text=T["public_lbl"])
        if "public_sub"    in self._ui_refs: self._ui_refs["public_sub"].configure(text=T["public_sub"])
        if "copy_local"    in self._ui_refs: self._ui_refs["copy_local"].configure(text=T["copy"])
        if "copy_public"   in self._ui_refs: self._ui_refs["copy_public"].configure(text=T["copy"])
        # Field labels
        field_map = {
            "f_folder": "folder", "f_motd": "message", "f_port": "port",
            "f_ver":    "version_lbl",
            "f_gm":     "gamemode",  "f_diff": "difficulty", "f_seed": "seed",
            "f_maxp":   "max_players", "f_ops": "operators", "f_ram": "ram",
        }
        for ref_key, t_key in field_map.items():
            if ref_key in self._ui_refs:
                self._ui_refs[ref_key].configure(text=T[t_key])
        if "ops_hint_lbl" in self._ui_refs: self._ui_refs["ops_hint_lbl"].configure(text=T["ops_hint"])
        if "mods_hint"    in self._ui_refs: self._ui_refs["mods_hint"].configure(text=T["mods_hint"])
        # Buttons
        if "add_mod"      in self._ui_refs: self._ui_refs["add_mod"].configure(text=T["add_mod"])
        if "remove_mod_btn" in self._ui_refs: self._ui_refs["remove_mod_btn"].configure(text=T["remove_mod"])
        if "send_btn"     in self._ui_refs: self._ui_refs["send_btn"].configure(text=T["send"])
        # Main buttons
        self.btn_create.configure(text=T["create_btn"])
        self.btn_start.configure(text=T["start"])
        self.btn_stop.configure(text=T["stop"])
        # Status label (only if offline/online)
        cur = self._status_label.cget("text")
        for old_k, new_k in [("offline","offline"),("starting","starting"),("online_status","online_status")]:
            # check any lang
            for lang in LANGS.values():
                if cur == lang[old_k]:
                    self._status_label.configure(text=T[new_k])
                    break
        # Checkbuttons
        chk_keys = ["pvp","whitelist","hardcore","flight","online","cmd_blocks","force_gm"]
        for i, (widget, _) in enumerate(self._chk_widgets):
            if i < len(chk_keys):
                widget.configure(text=T[chk_keys[i]])
        # Type buttons
        self._btn_paper.configure()  # text set via make_type_btn
        # Re-trigger to update paper/forge desc (desc labels need patching)

    def _send_command(self):
        cmd = self._cmd_var.get().strip()
        if not cmd:
            return
        if self._server_proc is None or self._server_proc.poll() is not None:
            self._log("Server is not running.", "err")
            return
        try:
            self._server_proc.stdin.write(cmd + "\n")
            self._server_proc.stdin.flush()
            self._log(f"> {cmd}", "ok")
            # save history
            if not self._cmd_history or self._cmd_history[-1] != cmd:
                self._cmd_history.append(cmd)
            self._cmd_hist_idx = -1
            self._cmd_var.set("")
        except Exception as ex:
            self._log(f"Error sending command: {ex}", "err")

    def _cmd_history_up(self):
        if not self._cmd_history:
            return
        if self._cmd_hist_idx == -1:
            self._cmd_hist_idx = len(self._cmd_history) - 1
        elif self._cmd_hist_idx > 0:
            self._cmd_hist_idx -= 1
        self._cmd_var.set(self._cmd_history[self._cmd_hist_idx])
        self._cmd_entry.icursor("end")

    def _cmd_history_down(self):
        if self._cmd_hist_idx == -1:
            return
        if self._cmd_hist_idx < len(self._cmd_history) - 1:
            self._cmd_hist_idx += 1
            self._cmd_var.set(self._cmd_history[self._cmd_hist_idx])
        else:
            self._cmd_hist_idx = -1
            self._cmd_var.set("")
        self._cmd_entry.icursor("end")

    def _set_status(self, state):
        if state == "online":
            self._dot.configure(fg=GREEN)
            self._status_label.configure(text="Online", fg=GREEN)
            self.btn_stop.configure(state="normal", bg=RED, fg=TEXT)
            self.btn_start.configure(state="disabled", bg=CARD, fg=MUTED)
        elif state == "starting":
            self._dot.configure(fg=ORANGE)
            self._status_label.configure(text="Starting...", fg=ORANGE)
            self.btn_start.configure(state="disabled", bg=CARD, fg=MUTED)
            self.btn_stop.configure(state="normal", bg=RED, fg=TEXT)
        else:
            self._dot.configure(fg=MUTED)
            self._status_label.configure(text="Offline", fg=MUTED)
            self.btn_stop.configure(state="disabled", bg=CARD, fg=MUTED)
            if self._server_folder and self._server_folder.exists():
                self.btn_start.configure(state="normal", bg=GREEN, fg="#0c1a10")
            else:
                self.btn_start.configure(state="disabled", bg=CARD, fg=MUTED)

    def _poll_status(self):
        if self._server_proc is None:
            self._set_status("offline")
            return
        if self._server_proc.poll() is not None:
            self._server_proc = None
            self._set_status("offline")
            self._log("Server stopped.", "info")
            return
        alive = ping_server("127.0.0.1", self._server_port)
        self._set_status("online" if alive else "starting")
        self._status_job = self.after(3000, self._poll_status)

    def _start_server(self):
        if not self._server_folder or not self._server_folder.exists():
            messagebox.showerror("Erro", "Folder not found. Create the server first.")
            return
        run_sh  = self._server_folder / "run.sh"
        run_bat = self._server_folder / "run.bat"
        if run_sh.exists() or run_bat.exists():
            cmd = ["cmd", "/c", "run.bat"] if os.name == "nt" else ["bash", "run.sh"]
        else:
            jars = list(self._server_folder.glob("paper-*.jar"))
            if not jars:
                messagebox.showerror("Erro", "No JAR found.")
                return
            ram = self.e_ram._var.get()
            cmd = ["java", f"-Xmx{ram}G", f"-Xms{ram}G", "-jar", jars[0].name, "--nogui"]

        self._set_status("starting")
        self._log("Starting server...", "info")
        try:
            self._server_proc = subprocess.Popen(
                cmd, cwd=str(self._server_folder),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        except FileNotFoundError:
            self._set_status("offline")
            messagebox.showerror("Erro", "Java not found. Install Java 17+.")
            return
        threading.Thread(target=self._stream_output, daemon=True).start()
        self._status_job = self.after(3000, self._poll_status)

    def _stream_output(self):
        for line in self._server_proc.stdout:
            line = line.rstrip()
            if line:
                self._log(line, "srv")
        self._server_proc = None
        self.after(0, lambda: self._set_status("offline"))
        self._log("Server stopped.", "info")

    def _stop_server(self):
        if self._server_proc is None:
            return
        self._log("Stopping server...", "info")
        try:
            self._server_proc.stdin.write("stop\n")
            self._server_proc.stdin.flush()
        except Exception:
            pass
        try:
            self._server_proc.terminate()
        except Exception:
            pass
        if self._status_job:
            self.after_cancel(self._status_job)
            self._status_job = None
        self._set_status("offline")

    def _start_create(self):
        self.btn_create.configure(state="disabled", text="Working...")
        threading.Thread(target=self._run_create, daemon=True).start()

    def _run_create(self):
        try:
            self._create()
        except Exception as ex:
            self._log(f"Error: {ex}", "err")
            messagebox.showerror("Erro", str(ex))
        finally:
            self.btn_create.configure(state="normal", text="Create Server ->")

    def _create(self):
        folder_name = self.e_folder.get().strip() or "my-server"
        motd        = self.e_motd.get().strip()   or "A Minecraft Server"
        version     = self._version_var.get()
        port        = self.e_port.get().strip()   or "25565"
        gm          = self.e_gamemode._var.get()
        diff        = self.e_difficulty._var.get()
        seed        = self.e_seed.get().strip()
        maxp        = self.e_maxp.get().strip()   or "20"
        ram         = self.e_ram._var.get()
        ops_raw     = self.e_ops.get().strip()
        stype       = self._server_type.get()

        bstr = lambda v: str(v).lower()
        pvp = bstr(self.chk_pvp.get()); wl = bstr(self.chk_wl.get())
        hc  = bstr(self.chk_hc.get());  flight = bstr(self.chk_flight.get())
        online  = bstr(self.chk_online.get())
        cmds    = bstr(self.chk_cmds.get())
        forcegm = bstr(self.chk_forcegm.get())

        folder = Path(folder_name)
        if folder.exists():
            if not messagebox.askyesno("Folder exists", f"'{folder_name}' already exists. Overwrite?"):
                return
            shutil.rmtree(folder)

        folder.mkdir(parents=True)
        self._log(f"Folder created: {folder.resolve()}", "ok")
        self._progress(8)

        try:
            res = subprocess.run(["java", "-version"], capture_output=True, text=True)
            self._log("Java: " + res.stderr.split("\n")[0], "info")
        except FileNotFoundError:
            raise RuntimeError("Java not found! Install Java 17+.")
        self._progress(15)

        if stype == "paper":
            url      = PAPER_VERSIONS[version]
            jar_name = f"paper-{version}.jar"
            self._log(f"Downloading PaperMC {version}...", "info")

            def hook_paper(count, block, total):
                if total > 0:
                    self._progress(15 + min(int(count * block * 65 / total), 65))

            urllib.request.urlretrieve(url, folder / jar_name, reporthook=hook_paper)
            self._log("Download complete.", "ok")
            self._progress(82)
            self._write_eula_and_props(folder, gm, diff, motd, port, maxp,
                                        seed, pvp, wl, hc, flight, online, cmds, forcegm)
            cmd_str = f"java -Xmx{ram}G -Xms{ram}G -jar {jar_name} --nogui"
            self._write_start_scripts(folder, cmd_str)
            type_label = "PaperMC"
            mods_label = "N/A (plugins)"
        else:
            forge_ver, installer_url = FORGE_VERSIONS[version]
            installer_name = f"forge-{forge_ver}-installer.jar"
            self._log(f"Downloading Forge {forge_ver} installer...", "info")

            def hook_forge(count, block, total):
                if total > 0:
                    self._progress(15 + min(int(count * block * 50 / total), 50))

            urllib.request.urlretrieve(installer_url, folder / installer_name, reporthook=hook_forge)
            self._log("Installer downloaded.", "ok")
            self._progress(68)
            self._log("Installing Forge (may take a while)...", "info")
            result = subprocess.run(
                ["java", "-jar", installer_name, "--installServer"],
                cwd=str(folder), capture_output=True, text=True)
            if result.returncode != 0:
                self._log(result.stderr[-600:], "err")
                raise RuntimeError("Forge installation failed.")
            self._log("Forge installed.", "ok")
            self._progress(82)
            self._write_eula_and_props(folder, gm, diff, motd, port, maxp,
                                        seed, pvp, wl, hc, flight, online, cmds, forcegm)
            mods_dir = folder / "mods"
            mods_dir.mkdir(exist_ok=True)
            type_label = f"Forge {forge_ver}"
            mods_label = f"{len(self._mods_list)} mod(s)"
            if self._mods_list:
                self._log(f"Copying {len(self._mods_list)} mod(s)...", "info")
                for mod_path in self._mods_list:
                    shutil.copy2(mod_path, mods_dir / mod_path.name)
                    self._log(f"  OK {mod_path.name}", "ok")

        if ops_raw:
            ops = [o.strip() for o in ops_raw.split(",") if o.strip()]
            ops_data = [{"uuid":"","name":op,"level":4,"bypassesPlayerLimit":False} for op in ops]
            (folder / "ops.json").write_text(json.dumps(ops_data, indent=2))
            self._log(f"Operators: {', '.join(ops)}", "ok")

        self._progress(100)
        self._server_folder = folder
        self._server_port   = port

        # Wait for public IP if still loading
        if self.public_ip == "loading...":
            self._log("Getting public IP...", "info")
            for _ in range(10):
                time.sleep(0.5)
                if self.public_ip != "loading...":
                    break

        local_addr  = f"{self.local_ip}:{port}"
        public_addr = f"{self.public_ip}:{port}"

        # Update info card
        self._info_local.set(local_addr)
        self._info_public.set(public_addr)
        self._info_version.set(version)
        self._info_type.set(type_label)
        self._info_gm.set(gm)
        self._info_diff.set(diff)
        self._info_maxp.set(f"{maxp} max")
        self._info_mods.set(mods_label)
        self._info_folder.set(str(folder.resolve()))

        self.after(0, lambda: self._set_status("offline"))
        self._log(f"\n-- Server ready! --", "ok")
        self._log(f"Press Start to launch.", "info")

        messagebox.showinfo("Done!",
            f"Server created!\n\n"
            f"Local:   {local_addr}\n"
            f"Public: {public_addr}\n\n"
            f"Press Start to launch.")

    def _write_eula_and_props(self, folder, gm, diff, motd, port, maxp,
                               seed, pvp, wl, hc, flight, online, cmds, forcegm):
        (folder / "eula.txt").write_text("eula=true\n")
        self._log("eula.txt accepted", "ok")
        props = (
            f"gamemode={gm}\ndifficulty={diff}\nmotd={motd}\n"
            f"server-port={port}\nmax-players={maxp}\nlevel-seed={seed}\n"
            f"pvp={pvp}\nwhite-list={wl}\nhardcore={hc}\nallow-flight={flight}\n"
            f"online-mode={online}\nenable-command-block={cmds}\nforce-gamemode={forcegm}\n"
            f"level-name=world\ngenerate-structures=true\nspawn-npcs=true\n"
            f"spawn-animals=true\nspawn-monsters=true\nview-distance=10\n"
        )
        (folder / "server.properties").write_text(props)
        self._log("server.properties created", "ok")

    def _write_start_scripts(self, folder, cmd):
        (folder / "start.sh").write_text(f'#!/bin/bash\ncd "$(dirname "$0")"\n{cmd}\n')
        os.chmod(folder / "start.sh", 0o755)
        (folder / "start.bat").write_text(f'@echo off\ncd /d "%~dp0"\n{cmd}\npause\n')
        self._log("Start scripts created", "ok")

    def _on_close(self):
        if self._server_proc and self._server_proc.poll() is None:
            if messagebox.askyesno("Server running",
                                    "The server is still running. Stop and exit?"):
                self._stop_server()
                time.sleep(1)
            else:
                return
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
