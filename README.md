# tebex-cog
=========================

Dieses Cog erlaubt es Discord-Usern, über den Befehl !claim ihre gekaufte Rolle 
automatisch zu erhalten – basierend auf ihrem Kauf über Tebex (mit Discord-Login).

Installation:
-------------
1. Entpacke den Ordner "tebexclaim" in dein Redbot-Cogs-Verzeichnis.
2. Starte deinen Bot neu oder lade das Cog mit:

   [p]load tebexclaim

Konfiguration:
--------------
1. Setze deinen Tebex Public API Token:
   [p]settoken DEIN_TOKEN

2. Mappe ein Produkt auf eine Rolle:
   [p]mapproduct Produktname Rollenname

   Beispiel:
   [p]mapproduct VIP VIP-Rolle

3. Jetzt kann ein User mit:
   [p]claim
   seine Rolle automatisch erhalten (wenn der Kauf gefunden wird).

Voraussetzung:
--------------
- Käufer müssen sich beim Kauf über Discord anmelden (Discord Login bei Tebex).
- Rollen müssen bereits auf deinem Discord-Server existieren.
