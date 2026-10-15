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

Die Integration gibt **alles** weiter, was das Gerät über `/api/status` liefert — Fahrt, Umwelt und
den Zustand des Raspberry selbst. So sieht man aus der Ferne (gleiches Netz / über HA) den ganzen
Betrieb eines Schiffs.

- **Fahrt / Pünktlichkeit:** Phase, Empfehlung, Kurszustand, Alarm-Zustand, Soll-Ankunft, Abfahrt,
  Reststrecke, Ist-/Soll-/Differenz-/Höchst-Tempo, Kurs über Grund, Kursabweichung + Kursgrenze,
  Restzeit, Wartezeit, Verspätung, Alter von Position und KAI-Daten, Hinweis, Nächster Halt.
- **Wetter:** Lufttemperatur, Wind, Windrichtung, Niederschlag (gleiche Quelle wie KAI).
- **Pegel:** Pegelstand, Pegeländerung (cm/h), Pegeltrend (steigend/stabil/fallend), Station.
- **Pi-Zustand (Diagnose):** CPU-Temperatur, CPU-Auslastung, Systemlast, Speicher belegt,
  RAM gesamt, Platte belegt, Laufzeit.
- **Binärsensoren:** Alarm, SIFA aktiv, Kamera-Hinweis, Position ok, Hupe, Warnlampe,
  Bordbuch vorhanden, Nächstes Bordbuch fällig, Kamera/Livestream konfiguriert.
- **Device-Tracker:** Schiffsposition (auf der HA-Karte) — so kommen die **GPS-Koordinaten über die
  Integration** nach HA, ganz ohne eigenes MQTT-Setup.

> Wetter/Pegel/Pi-Zustand brauchen Bordwächter-Gerät **≥ v0.1.47**.

## Hinweise

- Liest `GET /api/status` des Geräts (Basic-Auth mit dem UI-Passwort), Abruf alle 10 s.
- Fällt das Gerät/HA aus, warnt das Gerät trotzdem — HA ist nur Spiegel.
- Für den Release: dieses Verzeichnis (`custom_components/` + `hacs.json`) in ein eigenes
  GitHub-Repo `bordwaechter-ha` legen (HACS installiert aus GitHub).
