#!/usr/bin/python3
import time, random, os, sys, asyncio

from ably import AblyRealtime, AblyVCDiffDecoder
from ably.realtime.realtime_channel import ChannelOptions
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ABLY_API_KEY")
CHANNEL_NAME = os.getenv("CHANNEL_NAME")
RACE_LAP_CHANNEL_NAME = os.getenv("RACE_LAP_ABLY_CHANNEL")
RACE_FLAG_CHANNEL_NAME = os.getenv("RACE_FLAG_ABLY_CHANNEL")

TOTAL_LAPS = os.getenv("NUMBER_OF_LAPS", 2)

# Lock file configuration
LOCK_FILE = "/tmp/race_simulation.lock"


# -----------------------------
# ANSI Colors
# -----------------------------
RESET = "\033[0m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
ORANGE = "\033[33m"
BLUE = "\033[94m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"

# -----------------------------
# Configuration
# -----------------------------
TIME_STEP = 0.2  # 200ms per telemetry row
BASE_ACCELERATION = 30
BASE_BRAKING = 32
MAX_SPEED = 380

YELLOW_STEPS = 2
VSC_STEPS = 2
SAFETY_CAR_STEPS = 2
SAFETY_CAR_SPEED = 140
VSC_SPEED = 190
YELLOW_REDUCTION = 0.65
DRS_SPEED = 180

PIT_LANE_SPEED = 80
PIT_STOP_TIME = 2.0
PIT_SECTION = "Club"
PIT_TIME_LOSS = 22.0  # seconds

START_FUEL = 110.0
FUEL_BURN_PER_LAP = 20.0  # Increased fuel burn

LOCKUP_CHANCE = 0.6
LOCKUP_EXTRA_WEAR = (2.0, 7.0)  # % extra tyre wear if lockup occurs

TOTAL_DRIVERS = 20

# Typical lap times (seconds) for Silverstone GP (example)
TYPICAL_LAP_TIME = 95.0  # seconds for a clean lap
LAP_VARIATION = 3.0      # ± seconds random variation per lap

OVERTAKE_MODIFIERS = {
    "straight": 1.5,   # more likely to overtake
    "corner": 0.5,     # less likely to overtake
}

tyres = {
    "FL": 0.0,
    "FR": 0.0,
    "RL": 0.0,
    "RR": 0.0,
}


# Fan cheering messages
CHEERS = [
    "🏁 Fans cheer loudly! 🏎️💨",
    "👏 Crowd goes wild! 🏎️🔥",
    "🎉 Massive roar from the stands!",
    "📣 Supporters are on their feet!",
]

# -----------------------------
# Gears
# -----------------------------
GEARS = {
    1: (0, 90),
    2: (80, 130),
    3: (120, 170),
    4: (160, 210),
    5: (200, 250),
    6: (240, 290),
    7: (280, 320),
    8: (310, 350),
}

# -----------------------------
# Track Layout
# -----------------------------
TRACK_LAYOUT = [
    ("Hamilton Straight", 330, 6, True),
    ("Abbey Corner", 280, 3, False),
    ("Farm Curve", 300, 3, False),
    ("Village Corner", 110, 4, False),
    ("The Loop", 90, 4, False),
    ("Aintree", 180, 3, False),
    ("Wellington Straight", 320, 6, True),
    ("Brooklands", 130, 4, False),
    ("Luffield", 180, 5, False),
    ("Woodcote", 260, 3, False),
    ("Copse", 290, 4, False),
    ("Maggotts", 220, 3, False),
    ("Becketts", 200, 3, False),
    ("Chapel", 240, 3, False),
    ("Hangar Straight", 330, 7, True),
    ("Stowe", 160, 4, False),
    ("Vale", 120, 4, False),
    ("Club", 280, 6, False),
]

OTHER_DRIVERS = ["Red Bull", "Ferrari", "Mercedes", "Aston Martin", "Alpine", "Williams", "Audi", "Racing Bulls", "Haas", "Kick Sauber"]

# -----------------------------
# Helpers
# -----------------------------

# -----------------------------
# Lock File Management
# -----------------------------
def create_lock_file():
    """Create a lock file with the current process ID."""
    if os.path.exists(LOCK_FILE):
        # Check if the process in the lock file is still running
        try:
            with open(LOCK_FILE, 'r') as f:
                old_pid = int(f.read().strip())

            # Check if process is still running
            try:
                os.kill(old_pid, 0)  # Doesn't actually kill, just checks if process exists
                print(f"{RED}Error: Another race simulation is already running (PID: {old_pid}){RESET}")
                print(f"{YELLOW}If you're sure no other simulation is running, delete: {LOCK_FILE}{RESET}")
                return False
            except ProcessLookupError:
                # Process doesn't exist, safe to remove stale lock file
                print(f"{YELLOW}Removing stale lock file from PID {old_pid}{RESET}")
                os.remove(LOCK_FILE)
        except (ValueError, FileNotFoundError):
            # Invalid or empty lock file
            os.remove(LOCK_FILE)

    # Create new lock file with current PID
    with open(LOCK_FILE, 'w') as f:
        f.write(str(os.getpid()))
    print(f"{GREEN}Lock file created: {LOCK_FILE} (PID: {os.getpid()}){RESET}")
    return True


def remove_lock_file():
    """Remove the lock file."""
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
            print(f"{GREEN}Lock file removed: {LOCK_FILE}{RESET}")
    except Exception as e:
        print(f"{RED}Warning: Could not remove lock file: {e}{RESET}")



def adjust_speed(speed, target, accel, brake):
    if speed < target:
        speed += accel * TIME_STEP
    elif speed > target:
        speed -= brake * TIME_STEP
    return max(0, min(MAX_SPEED, speed))

def average_tyre_wear(tyres):
    return sum(tyres.values()) / 4

def worst_tyre_wear(tyres):
    return max(tyres.values())


def get_gear(speed):
    for g, (lo, hi) in GEARS.items():
        if lo <= speed <= hi:
            return g
    return 8


def overtake(speed, drs, section):
    if not drs:  # no DRS → cannot overtake
        return False
    base_chance = 0.05
    modifier = OVERTAKE_MODIFIERS.get(section_type(section), 1.0)
    return random.random() < base_chance * modifier


def color_flag(flag):
    return {
        "GREEN": f"{GREEN}GREEN{RESET}",
        "YELLOW": f"{YELLOW}YELLOW{RESET}",
        "SAFETY CAR": f"{ORANGE}SAFETY CAR{RESET}",
        "VSC": f"{BLUE}VSC{RESET}",
    }.get(flag, flag)

def color_drs(drs):
    if drs:
        return f"{GREEN}OPEN{RESET}"
    return "OFF "

def be_overtaken(speed, drs, section):
    """
    Returns True if your driver is overtaken.
    Only possible when your DRS is closed.
    """
    if drs:  # DRS open → cannot be overtaken
        return False
    # Randomly assume other drivers have DRS open 50% of the time
    other_drs = random.random() < 0.5
    if not other_drs:
        return False
    # Base chance modified by section type
    base_chance = 0.03
    modifier = OVERTAKE_MODIFIERS.get(section_type(section), 1.0)
    return random.random() < base_chance * modifier

# Helper function to classify section
def section_type(section_name):
    # Simplified: consider sections with "Straight" or "Hangar" as straights
    if "Straight" in section_name or "Hangar" in section_name or "Hamilton" in section_name or "Wellington" in section_name:
        return "straight"
    else:
        return "corner"

def handle_cheers(next_cheer_time, time_step=TIME_STEP):
    """
    Check if it's time for a fan cheer, print it, and return the updated next_cheer_time.
    Also sleep for the given time_step to maintain telemetry timing.
    """
    current_time = time.time()
    if current_time >= next_cheer_time:
        print(f"{MAGENTA}{random.choice(CHEERS)}{RESET}")
        next_cheer_time = current_time + 30
    time.sleep(time_step)
    return next_cheer_time
# -----------------------------
# Simulation
# -----------------------------
async def run_race():
    print("McLaren F1 – Silverstone Circuit Simulation")
    print("Telemetry: Lap | Section | Speed | Gear | DRS | Flag | PIT | Tyre Wear | Fuel (kg)\n")

    ## Ably
    ably = AblyRealtime(API_KEY, vcdiff_decoder=AblyVCDiffDecoder())
    channel = ably.channels.get(CHANNEL_NAME)

    lap_channel = ably.channels.get(RACE_LAP_CHANNEL_NAME)
    flag_channel = ably.channels.get(RACE_FLAG_CHANNEL_NAME)

    #@todo implement delta processing to reduce the amount of noise being pushed to the client app
    drs_channel = ably.channels.get("drs-status", ChannelOptions(params={
    'delta': 'vcdiff'
    }))

    speed = 0.0
    fuel = START_FUEL
    pit_done = False
    tyre_wear = 0.0  # 0% = fresh
    lap_times = []
    best_lap = None
    retired = False

    start_time = time.time()
    next_cheer_time = start_time + 30  # first cheer at 30s

    safety_car_active = False
    safety_car_steps_remaining = 0
    vsc_active = False
    vsc_steps_remaining = 0
    yellow_active = False
    yellow_steps_remaining = 0
    yellow_section = None

    position = random.randint(2, TOTAL_DRIVERS)  # start somewhere in the pack

    for lap in range(1, int(TOTAL_LAPS) + 1):
        await channel.publish("race_status", {"total_laps": TOTAL_LAPS, "racing":True})

        if retired==True:
            break


        # Generate a random tyre degradation per row for this lap
        TYRE_DEGRADATION_PER_STEP = random.uniform(0.03, 0.07)

        # Lap-to-lap variability
        lap_variation_factor = random.uniform(-LAP_VARIATION, LAP_VARIATION)
        lap_target_time = TYPICAL_LAP_TIME + lap_variation_factor
        # Total base duration of all sections (sum of section durations)
        total_base_duration = sum(duration for _, _, duration, _ in TRACK_LAYOUT)
         # Scale factor to adjust speed for lap variability
        lap_speed_factor = total_base_duration / lap_target_time


        fuel_per_section = FUEL_BURN_PER_LAP / len(TRACK_LAYOUT)
        fuel_factor = 1.0 + ((START_FUEL - fuel) * 0.002)
        accel = BASE_ACCELERATION * fuel_factor
        brake = BASE_BRAKING * fuel_factor
        lap_sim_time = 0.0

        prev_flag = None
        pit_this_lap = False
        pit_message=''
        approaching_pit_published = False


        print(f"{CYAN}========== LAP {lap} =========={RESET}")
        print(f"Fuel remaining: {fuel:.1f} kg | Tyre Wear: {tyre_wear:.1f}% | Tyre Degrade per step: {TYRE_DEGRADATION_PER_STEP:.3f}%")

        for section, base_speed, duration, drs_zone in TRACK_LAYOUT:
            flag = "GREEN"
            sector_time = 0.0  # start counting this sector
            base_sector_time = duration
            sector_time_modifier = 1.0


            section_variation = random.uniform(0.95, 1.05)  # 5% faster or slower
            target = (base_speed + random.uniform(-5,5)) * section_variation
            in_pit = pit_this_lap and section == PIT_SECTION

            # Determine if this sector is just before the pit entry
            pit_sector_index = [i for i, (s, _, _, _) in enumerate(TRACK_LAYOUT) if s == PIT_SECTION][0]
            current_sector_index = TRACK_LAYOUT.index((section, base_speed, duration, drs_zone))

            if pit_this_lap and current_sector_index == pit_sector_index - 1 and not approaching_pit_published:
                pit_message = pit_message  + " (on approach)"
                await channel.publish("boxbox_status", {"boxbox": True, "in_pit": False, "approaching_pit": True, "reason":pit_message})
                approaching_pit_published = True  # ensure only once




            # Retire car if out of fuel
            if fuel <= 0:
                retired = True
                speed = 0
                pit_text = "----"
                print(f"{RED}--- CAR RETIRED DUE TO FUEL DEPLETION ---{RESET}")
                await channel.publish(
                    "telemetry",
                    {
                        "lap": lap,
                        "section": section,
                        "speed_kmh": 0,
                        "gear": 0,
                        "drs": False,
                        "fuel_kg": 0,
                        "tyre_wear_pct": max(tyres.values()),  # or your choice
                        "in_pit": False,
                        "position": position,
                        "flag": flag,
                        "overtake": False,
                        "retired": True,
                    }
                )
                break  # exit steps for this section

        # Safety Logic Start #
            # --- Do not trigger SC/VSC/yellow on first sector of first lap ---
            first_sector_first_lap = lap == 1 and TRACK_LAYOUT.index((section, base_speed, duration, drs_zone)) == 0

            if not first_sector_first_lap:
                # Random incident → deploy Safety Car (section-based)  # 3% chance per section
                if (not safety_car_active and random.random() < 0.03 ):
                    safety_car_active = True
                    safety_car_steps_remaining = SAFETY_CAR_STEPS
                    print(f"{ORANGE}--- INCIDENT in {section}! SAFETY CAR DEPLOYED ---{RESET}")

                # Trigger sector yellow (only if no SC or VSC active)
                if (not safety_car_active and not vsc_active and not yellow_active and random.random() < 0.25 ):
                    yellow_active = True
                    yellow_steps_remaining = YELLOW_STEPS
                    yellow_section = section
                    print(f"{YELLOW}--- SECTOR YELLOW in {section} ---{RESET}")
                    # Escalate yellow to VSC
                    if yellow_active and not vsc_active and not safety_car_active:
                        if random.random() < 0.35:  # 35% escalation chance
                            vsc_active = True
                            vsc_steps_remaining = VSC_STEPS
                            yellow_active = False
                            yellow_section = None
                            print(f"{BLUE}--- YELLOW ESCALATED TO VSC ---{RESET}")

                if ( not safety_car_active and not vsc_active and not yellow_active and random.random() < 0.03 ):
                    vsc_active = True
                    vsc_steps_remaining = VSC_STEPS
                    print(f"{BLUE}--- VSC DEPLOYED (RACE CONTROL) ---{RESET}")


            if safety_car_steps_remaining > 0:
                flag = "SAFETY CAR"
                safety_car_steps_remaining -= 1

                if safety_car_steps_remaining == 0 and safety_car_active:
                    safety_car_active = False

            elif vsc_steps_remaining > 0:
                flag = "VSC"
                vsc_steps_remaining -= 1

                if vsc_steps_remaining == 0 and vsc_active:
                    vsc_active = False

            elif yellow_active and section == yellow_section and yellow_steps_remaining > 0:
                flag = "YELLOW"
                yellow_steps_remaining -= 1

                if yellow_steps_remaining == 0 and yellow_active:
                    yellow_active = False
                    yellow_section = None

            else:
                flag = "GREEN"

            # --- publish flag only on change ---
            if flag != prev_flag:
                await flag_channel.publish("flag_status", {"flag": flag})
                prev_flag = flag

        # Safety Logic End #



            # Random lockup event generates tyre wear
            lockup_wear = 0
            if random.random() < LOCKUP_CHANCE:
                lockup_wear = random.uniform(*LOCKUP_EXTRA_WEAR)
                print(f"{RED}--- Lockup! Extra tyre wear +{lockup_wear:.2f}% ---{RESET}")


            # Flag effects to sector times
            if flag == "YELLOW":
                sector_time_modifier *= 1.15
            elif flag == "VSC":
                sector_time_modifier *= 1.30
            elif flag == "SAFETY CAR":
                sector_time_modifier *= 1.60

            # Tyre wear effect
            sector_time_modifier *= max(0.7, 1.0 + worst_tyre_wear(tyres) / 200.0)

            # Optional: sector type
            if section_type(section) == "corner":
                sector_time_modifier *= 1.05

        # Pit Logic Start #
            if in_pit:
                    pit_message = f"{CYAN}--- IN PIT ---{RESET}"
                    pit_this_lap = False

                    pit_total_time = random.uniform(18.0, 23.0)  # seconds for this lap's pit
                    sector_time_modifier += pit_total_time / base_sector_time  # scale to sector

                    await channel.publish("boxbox_status", {"boxbox": False, "in_pit": True,  "approaching_pit" : False })

                    target = PIT_LANE_SPEED
                    speed  = PIT_LANE_SPEED
                    time.sleep(PIT_STOP_TIME)
                    # pit_done = True
                    for tyre in tyres:
                        tyres[tyre] = 0.0
                    if fuel < 70:
                        fuel = START_FUEL

                    print(f"{RED}--- PIT STOP ({PIT_STOP_TIME}s) - Tyres refreshed ---{RESET}")
                    await channel.publish("boxbox_status", {"boxbox": False, "in_pit": False, "approaching_pit" : False, "total_pit_time": pit_total_time})
            else:
                actual_sector_time = base_sector_time * sector_time_modifier

                # Force pit for tyres or fuel if not already pitting
                if not pit_this_lap:
                    if worst_tyre_wear(tyres) >= 45:
                        pit_this_lap = True
                        pit_message = "Tyres"
                        in_pit = section == "Club"
                        print(f"{RED}--- Tyres critically worn ({tyre_wear:.1f}%) - forced pit ---{RESET}")
                        safety_factor = max(0.6, 1.0 - (tyre_wear - 60) / 20)
                        target *= safety_factor
                        await channel.publish("boxbox_status", {"boxbox": True, "in_pit":False, "reason":"Tyres"})

                    if fuel <= 70.0:
                        pit_this_lap = True
                        pit_message = "Fuel"
                        in_pit = section == "Club"
                        print(f"{RED}--- Fuel low ({fuel:.1f} kg) - forced pit ---{RESET}")
                        await channel.publish("boxbox_status", {"boxbox": True, "in_pit":False, "reason":"Fuel"})

                    # Undercut strategy: only pit if safety car is out AND we're close to pit entry
                    # Check if we're within 2 sections of the pit lane (Club)
                    sections_to_pit = (pit_sector_index - current_sector_index) % len(TRACK_LAYOUT)
                    close_to_pit = sections_to_pit <= 2
                    if safety_car_active and close_to_pit and not pit_this_lap and random.random() < 0.8:
                        pit_this_lap = True
                        pit_message = "Undercut"
                        print(f"{RED}--- Safety Car Undercut Strategy (SC active, {sections_to_pit} sections to pit) ---{RESET}")
                        await channel.publish("boxbox_status", {"boxbox": True, "in_pit":False, "reason":"Undercut"})


        # Pit Logic End #


            #a step witll be 200ms so we can publish telemetry data in realtime
            steps = int(duration / TIME_STEP)

            for _ in range(steps):
                if retired:
                    break

                ot_text = None

                if safety_car_steps_remaining > 0:
                    safety_car_steps_remaining -= 1

                # --- Target speed ---
                section_variation = random.uniform(-5, 5)
                target = (base_speed + section_variation) * lap_speed_factor

                # Apply tyre wear effect
                worst_wear = worst_tyre_wear(tyres)
                tyre_factor = max(0.7, 1.0 - worst_wear / 100.0)
                target *= tyre_factor

                if flag == "SAFETY CAR":
                    target = SAFETY_CAR_SPEED
                elif flag == "VSC":
                    target = VSC_SPEED
                elif flag == "YELLOW":
                    target *=  YELLOW_REDUCTION

                # Pit lane speed enforcement
                if in_pit:
                    speed = PIT_LANE_SPEED
                else:
                    speed = adjust_speed(speed, target, accel, brake)
                    speed += random.uniform(-1.0, 1.0)

                drs = drs_zone and speed > 150 and flag == "GREEN" and not in_pit
                await drs_channel.publish( "drs_status", {"drs_enabled": drs})
                if drs:
                    target += 12

                # Gear selection
                gear = 2 if in_pit else get_gear(speed)

                # On-track overtakes
                if not in_pit:
                    if position > 1 and overtake(speed, drs, section):
                        position -= 1
                        ot_text = f"💨 OVERTAKE! Now in position {position}"
                        await channel.publish("overtake_status", {"status": "over take", "position": position})

                    elif position < TOTAL_DRIVERS and be_overtaken(speed, drs, section):
                        position += 1
                        ot_text = f"⬇️ OVERTAKEN! Now in position {position}"
                        await channel.publish("overtake_status", {"status": "passed", "position": position})

                # --- Pit overtakes ---
                else:
                    if position < TOTAL_DRIVERS and random.random() < 0.15:  # 15% chance per step
                        position += 1
                        ot_text = f"⬇️ OVERTAKEN IN PIT! Now in position {position}"
                        await channel.publish("overtake_status", {"status": "passed in pits", "position": position})


                # --- Update timers ---
                time_per_step = actual_sector_time / steps
                sector_time += time_per_step
                lap_sim_time += time_per_step

                # Fuel consumption
                fuel -= fuel_per_section / steps
                fuel = max(0, fuel)



                # Tyre degradation per row
                if not in_pit:
                    tyre_wear += TYRE_DEGRADATION_PER_STEP + (lockup_wear / steps)
                    tyre_wear = min(100, tyre_wear)
                    for tyre in tyres:
                        # Base degradation
                        wear = TYRE_DEGRADATION_PER_STEP

                        # Front tyres suffer more in corners
                        if tyre in ("FL", "FR") and section_type(section) == "corner":
                            wear *= 1.3

                        # Lockups mostly hurt front tyres
                        if lockup_wear > 0 and tyre in ("FL", "FR"):
                            wear += lockup_wear / steps

                        tyres[tyre] = min(100, tyres[tyre] + wear)


                # --- publish telemetry data ---
                await channel.publish(
                    "telemetry",
                    {
                        "timestamp": time.time(),
                        "lap": lap,
                        "section": section,
                        "speed_kmh": round(speed, 1),
                        "gear": gear,
                        "drs": drs,
                        "fuel_kg": round(fuel, 2),
                        "in_pit": in_pit,
                        "position": position,
                        "flag":flag,
                        "overtake": ot_text is not None,
                        "tyres": tyres,
                        "tyre_wear_avg": round(average_tyre_wear(tyres), 2),
                        "tyre_wear_worst": round(worst_tyre_wear(tyres), 2),
                        "retired": False
                    }
                )


                print(
                    f"Lap {lap} | Pos {position} | {section:<18} | ",
                    f"Speed: {speed:6.1f} km/h | "
                    f"Gear: {gear} | "
                    f"DRS: {color_drs(drs)} | "
                    f"Flag: {color_flag(flag)} | "
                    f"Tyres: FL {tyres['FL']:.1f}% | FR {tyres['FR']:.1f}% | "
                    f"RL {tyres['RL']:.1f}% | RR {tyres['RR']:.1f}% | "
                    f"Pit This Lap: {YELLOW if pit_this_lap else ''}{pit_this_lap}{RESET if pit_this_lap else ''} | "
                    f"Pit Msg: {YELLOW if pit_message else ''}{pit_message}{RESET if pit_this_lap else ''} | "
                    f"Fuel: {fuel:6.1f} kg",
                    end=""
                )
                print(f" | {ot_text}" if ot_text else "")


                # Fans cheering every 30s
                next_cheer_time = handle_cheers(next_cheer_time)

            # --- publish sector time after finishing section ---
            await channel.publish(
                "sector_time",
                {
                    "lap": lap,
                    "sector": section,
                    "sector_time_sec": round(sector_time, 3),
                    "lap_time_sec": round(lap_sim_time, 3),
                    "position": position,
                }
            )


        lap_times.append(lap_sim_time)
        best_lap = lap_sim_time if best_lap is None or lap_sim_time < best_lap else best_lap

        print(
            f"{GREEN}Lap {lap} time: {lap_sim_time:.2f}s | Best: {best_lap:.2f}s  "
        )

        # --- publish lap time after finishing lap ---
        await lap_channel.publish(
            "lap_time",
            {
                "lap": lap,
                "lap_time_sec": round(lap_sim_time, 3),
                "best_lap_sec": round(best_lap, 3),
                "position": position,
            }
        )


    await channel.publish("telemetry", "finished")
    await ably.close()
    print(f"{GREEN}Race simulation complete — {TOTAL_LAPS} laps completed 🏁{RESET}")


# =============================
# Entry point
# =============================
if __name__ == "__main__":

       # Check and create lock file before starting
    if not create_lock_file():
        sys.exit(1)

    try:
        asyncio.run(run_race())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Race interrupted by user{RESET}")
        remove_lock_file()
        sys.exit(0)
    except Exception as e:
        print(f"{RED}Error during race: {e}{RESET}")
        remove_lock_file()
        sys.exit(1)
