# Robots

**Problem.** World models train on camera video paired with the commands that drove it, and none of the robots in these projects records that yet.

**Idea.** One robot in two versions. A is a delivery-bot-class sensor rover designed from real parts and simulated, and B is a small real rover that logs every steering and speed command next to its camera video.

**Built.** Mostly design documents: a drafted spec for version A, brainstorm notes for version B, a PiDog voice-dog script from March 2026, and a placeholder for a walking plant pot. Neither rover is built. 5 commits on 1 day, Oct 30, 2026.

**Decision.** Version A is designed from real RobotShop Canada parts (about CA$34k) and then simulated instead of built. Invented sensors or impossible numbers count as a failure there, so every part is a real product with a real price.

Nick's robot projects, real and imagined.

| Project | What it is | State |
|---|---|---|
| [city-sensor-robot](city-sensor-robot/) | A robot that drives city streets collecting data for video and world-model work, in two versions: A, a simulated sensor-heavy rover built from real RobotShop Canada parts, and B, a small real rover that logs camera video with its drive commands | A: design drafted. B: brainstorm notes |
| [pidog](pidog/) | SunFounder PiDog "Buddy", voice-controlled through Ollama on the ArtPC | Working script from March 2026 |
| [walking-plant-pot](walking-plant-pot/) | A plant pot that walks | Notes to be brought in |
