# PiDog "Buddy"

SunFounder PiDog running as a voice-active dog. Speech goes to an LLM on the ArtPC
(Ollama, `gpt-oss:20b` on the RTX 3090), and the reply comes back as a line of text plus
actions (sit, wag tail, bark...).

- `real_dog.py`: config and personality. Wake word "hey buddy", ultrasonic "too close"
  at 15 cm, likes front-to-rear petting, hates rear-to-front.
- Runs on the dog's Pi: `sudo python3 ~/scripts/real_dog.py`. Needs SunFounder's `pidog`
  library and `voice_active_dog`.

Copied 2026-10-30 from `~/.openclaw/workspace/pidog/real_dog.py` (written 2026-03-07).
The original stays where it is.
