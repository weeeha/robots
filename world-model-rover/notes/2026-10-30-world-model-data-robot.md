# World-model data robot: brainstorm notes (2026-10-27 to 10-30)

Status: brainstorm only. No design approved, nothing built.
Source: the "Mars rover teaching demo" session (2026-10-27 to 10-30). Close cousin of
[city-sensor-robot](../../city-sensor-robot/), which is the simulated, sensor-heavy version.

## The idea, how it changed
1. Started as: use a free, open world model to teach a simulated Mars rover, as a portfolio demo.
2. Nick's pivot: a real robot that drives on the street and collects data. That data (camera video paired with the drive commands) is the kind a world model trains on.
3. Nick: robots live in their own PUBLIC repo, kept apart from world-models-lab-spec.

## Working picture (Claude's guess, Nick hasn't confirmed it)
- Small rover-style robot, maybe styled like a Mars rover. Camera, plus a log of every steering and speed command saved alongside the video.
- Nick drives it at first, and those rides are the training data. Then a world model trained on his street predicts what the camera sees next, and later drives a little on its own.
- Portfolio payoff: show the robot's prediction next to the real footage.
- Hardware he already owns that could be used: Bambu P1S for the body, a Raspberry Pi as the brain, the RTX 3090 in ArtPC for training.

## Constraints that come from the repo being public
- Street video has faces and license plates. Blur them automatically before anything is published. Raw footage never goes in the repo.
- No dataset files in the repo. NASA's AI4Mars has no license on its listing and is about 17.8 GB, so ship a download script (from Zenodo) and a few sample frames, credit NASA/JPL.
- No keys. Any `.env` is gitignored from the first commit.
- MIT license on Nick's code, with DreamerV3 or any other borrowed code clearly marked.

## Free building blocks found
- DreamerV3: open code, small world model, trains on a laptop or a single GPU.
- AI4Mars: about 35K labeled terrain images from Curiosity, Opportunity and Spirit. https://data.nasa.gov/dataset/ai4mars-a-dataset-for-terrain-aware-autonomous-driving-on-mars and https://zenodo.org/records/15995036
- Open-weight world/action models: SenseTime Kairos 3.0 (4B, Apache-2.0); Runway Praxis-1 (announced, public release "in the coming months"). Cosmos and V-JEPA 2 license status not re-checked.

## Open question still with Nick
- First ride: where does it drive, and is he walking next to it with a controller, or is it supposed to go on its own?
