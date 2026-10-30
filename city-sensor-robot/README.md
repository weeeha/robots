# City sensor robot

A robot that drives city streets and records what it sees, so the recordings can feed video
and world-model work. Two versions of the same idea:

| | A. Sensor rover (simulated) | B. World-model rover (real) |
|---|---|---|
| What | Delivery-bot-class rover carrying lidar, thermal, NIR, UV, sound, Wi-Fi, 360 and 64 MP cameras | Small, maybe Mars-rover-styled robot with a camera that logs every steering and speed command next to the video |
| Built? | Designed with real RobotShop Canada parts (~CA$34k), then imitated: spec sheet, renders, a simulated drive, a replay console | Meant to be built from what Nick has: printed body on the P1S, a Raspberry Pi, training on the ArtPC 3090 |
| Output | A synthetic multi-sensor dataset and an art piece | Real street footage plus drive commands, a world model that predicts the next frame, then drives a little |
| Doc | [docs/2026-10-26-city-sensor-robot-design.md](docs/2026-10-26-city-sensor-robot-design.md) | [notes/2026-10-30-world-model-rover.md](notes/2026-10-30-world-model-rover.md) |
| State | Design drafted, 3 questions open | Brainstorm notes |

Rules for both, since this repo is public: no faces, licence plates or real network names in
anything published; no raw footage or dataset files committed; no keys (`.env` is ignored).

Open questions:
- A: who opens the raw data, where street images come from, which city.
- B: on the first ride, does Nick walk next to it with a controller, or does it drive itself?
