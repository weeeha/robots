# City Sensor Robot: design

Status: draft for Nick's review, 2026-10-26
Working name: **UNIT-01** (placeholder, Nick's to rename)

## TL;DR

A concept and art project: a city robot on a delivery-bot-class chassis with an extra battery and as many sensors as it can carry. It drives through city streets collecting environment data for later video and world-model work. We don't build it physically. We design it as if it could be built, with real parts from RobotShop Canada, then imitate it: renders of the robot, a simulated drive with a plausible multi-sensor dataset, and a web console that replays the drive with every sensor feed side by side.

Four deliverables, built in this order: **1 spec sheet → 4 console → 3 simulated drive → 2 renders.**

## Intent

- Nick's own concept/art project, not a client job and not a product.
- The data is part of the artwork: an ordinary street seen as heat, Wi-Fi density, UV, sound, point clouds.
- Believability matters. Every part is a real product with a real price, and every number (weight, power, runtime, data rate) should hold up to someone who builds robots. A sci-fi render with invented sensors is a failure even if it looks good.
- The dataset is shaped like a real world-model dataset (synchronized streams on one clock, poses, metadata), so it reads as research-grade.

## Goals

1. A spec sheet for the robot: parts list with RobotShop Canada links and CAD prices, plus weight, power budget, runtime, data rates and storage per hour.
2. Renders of the robot in Blender: a hero shot, a close-up of the sensor mast, and one shot in a street setting.
3. One simulated drive: a route through real city streets and a synthetic dataset covering every sensor along it.
4. A web console that replays that drive: a map with the robot moving along it and all sensor feeds beside it. Screen-recording it produces the video.

## Non-goals

- No physical build, wiring diagrams, firmware or ROS code that runs on hardware.
- No real data capture. Nothing is collected from real people or networks.
- No training a world model on the output. The dataset only has to look ready for one.

## Anti-goals (would make it a failure even if it works)

- Made-up sensors or impossible numbers (a 2 kg robot running 12 h, 8K thermal).
- Personal data in the art: real faces, real licence plates, real Wi-Fi network names or MAC addresses. Wi-Fi shows up as counts, channels and signal strength, with hashed IDs only.
- A generic "AI robot dashboard" look. The console should feel like an instrument, in line with Nick's unslop rule.

## The robot

### Chassis

| Part | Source | Price (CAD) | Why |
|---|---|---|---|
| AgileX Scout 2.0, 4WD all-terrain AGV, 930 × 699 × 349 mm, 24 V, CAN bus, ROS | [RobotShop CA, AgileX](https://ca.robotshop.com/collections/agilex) | ~20,830 | Delivery-bot footprint, a common choice for outdoor research data collection, and room for a sensor mast. |

Nick asked for a "delivery bot chassis". RobotShop sells no 6-wheel delivery-bot chassis (Starship-style), so the Scout 2.0 is the closest real equivalent. **My call.**
Cheaper alternative: [Rover Robotics 4WD Pro](https://ca.robotshop.com/products/rover-robotics-4wd-pro-mobile-robotics-platform) (~13,497, IP67, 180 lb payload).

### Power ("add more battery")

| Part | Source | Price (CAD) |
|---|---|---|
| Stock Scout 2.0 pack, 24 V 30 Ah (~720 Wh) | included | 0 |
| Extra 24 V 50 Ah LiFePO4 pack (~1,280 Wh, ~12 kg) with BMS, in a sealed box on the top deck under the mast (too big for the Scout's internal bay) | **off-store** (RobotShop has no 24 V LiFePO4 pack) | ~900 est. |
| 24 V → 12 V / 5 V DC-DC converters for the sensor bus | RobotShop CA | ~80 est. |

Power budget (average while driving at walking pace): drive ~150 W, compute ~40 W, sensors ~40 W, so **~230 W total**.
Runtime: stock pack alone ~3 h. Stock plus extra pack (~2,000 Wh) gives **~8 h, a full day**.

### Compute (the "model on board")

| Part | Source | Price (CAD) |
|---|---|---|
| NVIDIA Jetson AGX Orin 64 GB dev kit (275 TOPS, 15–60 W) | [RobotShop CA](https://ca.robotshop.com/products/yahboom-nvidia-jetson-agx-orin-developer-kit-64gb-275-tops-official-developer-kit) | ~8,205 |
| 4 TB NVMe SSD for logging | off-store | ~350 est. |

The onboard model: **my call.** It runs a curiosity loop. It picks the next street by how different it looks from what it has already logged, and it tags moments worth keeping (heat anomalies, loud events, dense Wi-Fi). The console shows those decisions as a "why I turned here" log.
Cheaper alternative: [Jetson Orin NX 16 GB](https://ca.robotshop.com/products/yahboom-jetson-orin-nx-developer-kit-16gb-ram-super-version-with-nvidia-core-module-ai-large-model-developer-kit) (~1,667).

### Sensors (Nick's list)

| Sensor | Part | Source | Price (CAD) |
|---|---|---|---|
| Lidar | Unitree 4D LiDAR L2, 360° × 96° FOV, 30 m | [RobotShop](https://www.robotshop.com/products/unitree-4d-lidar-l2) | ~478 |
| Thermal | Waveshare long-wave IR thermal camera, 80 × 62 px, wide angle | [RobotShop CA](https://ca.robotshop.com/products/waveshare-long-wave-ir-thermal-imaging-camera-module-raspberry-pi-ir-camera-8062-pixels-type-c-port-wide-angle) | ~150 est. |
| Infrared (near-IR) | Arducam NoIR 8 MP IMX219 with motorized IR-cut filter, plus an 850 nm IR illuminator | RobotShop CA | ~57 + ~30 |
| UV | Waveshare LTR390-UV (UV index, I²C) | [RobotShop CA](https://ca.robotshop.com/products/digital-ltr390-uv-ultraviolet-sensor-c-direct-uv-index-value-output-i2c) | ~14 |
| Sound | ReSpeaker XMOS XVF3800 circular 4-mic array with direction of arrival | [RobotShop CA](https://ca.robotshop.com/products/respeaker-xmos-xvf3800-w-case-ai-powered-4-mic-array-for-clear-voice-in-noise) | ~90 est. |
| Wi-Fi | ESP32-S3 dev board in passive scan mode (counts, channels, RSSI; 2.4 GHz only, so the dataset has no 5 GHz band) | [RobotShop CA](https://ca.robotshop.com/products/waveshare-esp32-s3-microcontroller-24ghz-wi-fi-development-board-240mhz-dual-core-processor-esp32-s3-wroom-1-module-no-headers) | ~20 est. |
| 360 camera | Insta360 X4 (8K 360), powered from the 5 V bus, 512 GB microSD swapped mid-day, clock synced by a GNSS-timestamped LED flash at the start of each clip | **off-store** | ~700 est. |
| High-detail camera | Arducam 64 MP USB 3.0 motorized-focus module with enclosure | [RobotShop CA](https://ca.robotshop.com/products/arducam-64mp-motorized-focus-usb-30-camera-module-w-encolsure) | ~379 |

Support sensors (needed to make the data usable, **my call**):

| Part | Source | Price (CAD) |
|---|---|---|
| Emlid Reach M2 multi-band RTK GNSS (position + IMU, ~5–10 Hz fixes) with multi-band antenna, RTK corrections over NTRIP via the robot's LTE link | [RobotShop CA](https://ca.robotshop.com/products/emlid-reach-m2-multi-band-uav-rtk-gnss-module) | ~899 + ~150 antenna |
| Mast, weatherproof enclosures, mounts, cabling | mixed | ~800 est. |

Layout (**my call**): a single mast about 1.4 m off the ground. Lidar and 360 camera on top. Below them, a forward-facing head with the 64 MP, thermal and NoIR cameras side by side. Mic array and UV sensor on the top deck of the head. GNSS antenna on the rear of the chassis. Compute, batteries and the ESP32 sit inside the chassis.

### Totals (rough)

- **Full build: ~CA$34,100.** About CA$31,000 of that is RobotShop, the rest is off-store.
- Budget build (Rover 4WD Pro + Orin NX): ~CA$20,300.
- Mass: ~80 kg (Scout ~62 kg + battery ~12 kg + mast and sensors ~6 kg).

Prices come from search snippets of RobotShop pages. Some may be stale, and the store's bot check blocked live verification. The spec sheet lists them as "listed price, verify at checkout".

### Data rates (for the spec sheet and the simulated dataset)

| Stream | Rate | ~GB/hour |
|---|---|---|
| Lidar point cloud (~64k pts/s, 10 Hz frames) | 10 Hz | ~4 |
| 360 video, 5.7K H.265 (on the camera's own SD) | 30 fps | ~50 |
| 64 MP stills | 1 per 2 s | ~25 |
| Thermal 80 × 62, 16-bit radiometric | 9 Hz | ~0.3 |
| NoIR 8 MP video, H.265 | 15 fps | ~4 |
| Audio, 4 ch 48 kHz | continuous | ~2 |
| UV, Wi-Fi, GNSS/IMU | 1–100 Hz | <0.1 |
| **Total** | | **~85 GB/h, ~700 GB per 8 h day** (~400 GB to the SSD, the rest on the 360's SD cards) |

The 4 TB SSD holds about ten days of driving. The 360 camera needs a card swap about every 10 hours of recording.

## Simulated drive

- **City and route: open, Nick's call.** The route should be real streets so the map and the street shot can be specific. About 3–5 km, roughly 1 hour at walking pace.
- Dataset layout (**my call**), shaped like a real world-model dataset:
  ```
  unit01_<city>_<date>/
    metadata.json        robot spec, sensor calibration, extrinsics
    poses.parquet        fused GNSS + IMU estimate, 100 Hz
    lidar/               .pcd per frame (downsampled for the web)
    thermal/             16-bit PNG per frame
    nir/ cam360/ hires/  frames or short clips
    audio/               4-channel WAV chunks + SPL timeline
    uv.csv  wifi.csv     scalar timelines
    events.jsonl         the onboard model's decisions and tags
  ```
- How the synthetic data is made (**builder's call, with constraints**): every stream must line up in time and place. The thermal map has to agree with the camera frames (warm vents, cold shadows), and Wi-Fi density should rise near storefronts. Imagery can be generated or rendered, but no real faces, licence plates or network names.
- Scale: the console needs a web-weight subset (~200–500 MB). The "full" dataset can exist as a manifest with plausible file sizes; it doesn't have to be filled to 60 GB.

## Console

- A single web page that plays back the drive.
- Map with the robot's track and current position. A scrubbable timeline with the onboard model's event markers.
- Panels for lidar (3D point cloud), thermal, NIR, 360 (draggable view), high-detail still, audio level and direction, UV index, Wi-Fi count/channel chart.
- A "why I turned here" log from the onboard model.
- Visual direction: instrument-like, dense, monochrome base with one signal colour per sensor. Run unslop before and after.
- Hosting: a private Artifact or a Vercel preview, whichever Nick prefers. Default is a Vercel preview, unlisted.

## Renders

- Model the robot in Blender to the spec's dimensions: Scout 2.0 body, mast, sensor head.
- Three shots: hero 3/4, mast close-up, robot on a street from the simulated route.
- Style: product-photo clean for the first two, documentary for the street shot.

## Calls made after the builder check (mine, Nick can overturn)

- **Route vs. onboard model:** the route is chosen up front. The "why I turned here" log is authored narration, but every line cites values that really exist in the synthetic streams at that timestamp. Nothing is computed with embeddings.
- **Spec sheet format:** an HTML page, the first section of the console site. A PDF export of it is optional.
- **Video:** a 16:9 1080p screen recording of the console, with the 1-hour drive time-compressed to about 2–3 minutes and synthetic street audio from the mic stream. Venue-specific cuts come later.

## Left to the builder

- Console tech stack, map provider and how the 3D lidar is rendered.
- Method for generating synthetic imagery and point clouds, within the constraints above.
- Blender modelling approach and level of detail.

## Open (Nick's)

- City and route.
- Robot name.
