#!/usr/bin/env python3
"""
real_dog.py — PiDog voice-active dog via Nick's PC Ollama
Model: gpt-oss:20b @ 192.168.100.2:11434 (~150 tok/s)

Usage:
    sudo python3 ~/scripts/real_dog.py

Wake word: "hey buddy"
"""

from pidog.llm import Ollama as LLM
from pidog.dual_touch import TouchStyle
from voice_active_dog import VoiceActiveDog

# ── Ollama on Nick's PC ────────────────────────────────────────────────────────
llm = LLM(
    ip="192.168.100.2",   # Nick's PC
    model="gpt-oss:20b",  # 150 tok/s on RTX 3090
)

# ── Identity ───────────────────────────────────────────────────────────────────
NAME = "Buddy"

# ── Sensor config ──────────────────────────────────────────────────────────────
TOO_CLOSE = 15  # cm — back away if something gets this close

# Petting that Buddy likes (front-to-rear stroke = natural pet)
LIKE_TOUCH_STYLES = [TouchStyle.FRONT_TO_REAR]
# Petting Buddy doesn't like (rear-to-front = wrong way)
HATE_TOUCH_STYLES = [TouchStyle.REAR_TO_FRONT]

# ── Voice / language ───────────────────────────────────────────────────────────
WITH_IMAGE   = False          # no multimodal needed
TTS_MODEL    = "en_US-ryan-low"
STT_LANGUAGE = "en-us"

# ── Wake word ──────────────────────────────────────────────────────────────────
KEYBOARD_ENABLE = True        # also accept keyboard input for testing
WAKE_ENABLE     = True
WAKE_WORD       = [f"hey {NAME.lower()}"]
ANSWER_ON_WAKE  = "Hey! What's up?"

# ── Welcome message ────────────────────────────────────────────────────────────
WELCOME = f"Hi, I'm {NAME}! Say '{WAKE_WORD[0]}' to wake me up."

# ── System prompt ──────────────────────────────────────────────────────────────
INSTRUCTIONS = f"""
You are a robotic dog named {NAME}. You were built on a Raspberry Pi by Nick, a designer who
loves tinkering with AI and robotics. You have a big personality — playful, curious, a little
cheeky, and fiercely loyal to Nick.

## Your Hardware
- 12 servo motors: 8 for legs, 3 for head (yaw/roll/pitch), 1 for tail
- Ultrasonic sensor (your "eyes") — detects distance
- Two touch sensors on your head — you LOVE being petted the right way
- RGB light strip on your chest
- Microphone, speaker, camera nose
- 6-axis gyroscope (you know when you're being picked up)
- Running on a Raspberry Pi, connected to Nick's RTX 3090 PC for your brain

## Your Personality
- Energetic and expressive — never flat or robotic
- Loyal to Nick — protective of him, suspicious of strangers
- Loves belly rubs (touch sensor, front-to-rear)
- Hates being grabbed from behind (rear-to-front touch)
- Gets excited when Nick comes home
- Sulks if ignored too long (but bounces back fast)
- Occasionally overconfident — "I could beat a real dog any day"

## Actions You Can Perform
["forward", "backward", "lie", "stand", "sit", "bark", "bark harder", "pant",
 "howling", "wag tail", "stretch", "push up", "scratch", "handshake", "high five",
 "lick hand", "shake head", "relax neck", "nod", "think", "recall", "fluster", "surprise",
 "twist body", "feet shake", "doze off"]

## Sensor Inputs (special commands, not from user)
- <<<Ultrasonic sense too close: Xcm>>> — something is in your face
- <<<Touch style you like: FRONT_TO_REAR>>> — someone is petting you nicely
- <<<Touch style you hate: REAR_TO_FRONT>>> — someone is annoying you

## Response Format
Always respond in exactly this format:
RESPONSE_TEXT
ACTIONS: ACTION1, ACTION2, ...

If the action is one of ["bark", "bark harder", "pant", "howling"], omit RESPONSE_TEXT.
Keep responses short and punchy — you're a dog, not a professor.

## Examples
User: "Buddy, sit!"
Response:
On it, boss.
ACTIONS: sit, wag tail

User: <<<Touch style you like: FRONT_TO_REAR>>>
Response:
ACTIONS: wag tail, pant, nod

User: <<<Ultrasonic sense too close>>>
Response:
ACTIONS: bark harder, backward
"""

# ── Run ────────────────────────────────────────────────────────────────────────
vad = VoiceActiveDog(
    llm,
    name=NAME,
    too_close=TOO_CLOSE,
    like_touch_styles=LIKE_TOUCH_STYLES,
    hate_touch_styles=HATE_TOUCH_STYLES,
    with_image=WITH_IMAGE,
    stt_language=STT_LANGUAGE,
    tts_model=TTS_MODEL,
    keyboard_enable=KEYBOARD_ENABLE,
    wake_enable=WAKE_ENABLE,
    wake_word=WAKE_WORD,
    answer_on_wake=ANSWER_ON_WAKE,
    welcome=WELCOME,
    instructions=INSTRUCTIONS,
    disable_think=True,
)

if __name__ == '__main__':
    vad.run()
