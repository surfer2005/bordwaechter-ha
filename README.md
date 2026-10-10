# Bordwächter — Home-Assistant-Integration (HACS)

Bindet das Bordwächter-Gerät in Home Assistant ein: Status, Kurs-Ampel, Alarm/SIFA und die
Schiffsposition — lokal gelesen, von extern (für die Technik) einsehbar. Das Sicherheits-/Alarm-Herz
bleibt auf dem Gerät; HA ist reine Anzeige.

## Installation (HACS)

1. HACS → ⋮ → **Benutzerdefinierte Repositorys** → dieses Repo als Typ *Integration* hinzufügen.
2. „Bordwächter" installieren, Home Assistant neu starten.
3. **Einstellungen → Geräte & Dienste → Integration hinzufügen → Bordwächter**.
4. **Host/IP** des Geräts, **Port** (8090) und das **UI-Passwort** eintragen → fertig.

## Entitäten

- **Sensoren:** Phase, Empfehlung, Kurszustand, Soll-Ankunft, Abfahrt, Reststrecke, Ist-/Soll-Tempo,
  Kursabweichung (m), Restzeit, Nächster Halt.
- **Binärsensoren:** Alarm, SIFA aktiv, Kamera-Hinweis, Position ok.
- **Device-Tracker:** Schiffsposition (auf der HA-Karte) — so kommen die **GPS-Koordinaten über die
  Integration** nach HA, ganz ohne eigenes MQTT-Setup.

## Hinweise

- Liest `GET /api/status` des Geräts (Basic-Auth mit dem UI-Passwort), Abruf alle 10 s.
- Fällt das Gerät/HA aus, warnt das Gerät trotzdem — HA ist nur Spiegel.
- Für den Release: dieses Verzeichnis (`custom_components/` + `hacs.json`) in ein eigenes
  GitHub-Repo `bordwaechter-ha` legen (HACS installiert aus GitHub).
