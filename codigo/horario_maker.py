import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import textwrap
import pandas as pd

# Importar las sesiones
df = pd.read_csv("sessions.csv")
# Seleccionamos las de la semana a evaluar, que son las que ordenaremos
this_week_sessions = df.loc[df["setmana"] == "2026-W47"]
this_week_sessions_matins = df.loc[df["torn_requerit"] == "mati"]

print(this_week_sessions)

# =========================================================
# PENALTY SETTINGS
# =========================================================
# Hard penalties are deliberately much larger than soft penalties. This supports
# a feasibility-first approach: the genetic algorithm should prioritise avoiding
# invalid timetables before improving preferences.

HARD_PENALTY = 10 ** 6
SOFT_SMALL = 10
SOFT_MEDIUM = 50
SOFT_LARGE = 200


# =========================================================
# EVENT GENERATION
# =========================================================
# Events are the individual timetable items that the genetic algorithm assigns
# to time slots. Each event stores its type, module, teacher and group identity.
# Duration of each event type in hours.

DAYS = ["MON", "TUE", "WED", "THU", "FRI"]
HOURS = list(range(830, 1430))  # available hourly slots: 08:30 to 14:30

# Total number of grid slots in the timetable.
nG = len(DAYS) * len(HOURS)

def valid_slots(duration):
    """ Returns all valid start slots for an event with the given duration.
    This prevents multi-hour events, such as lectures, from starting so late
    that they run beyond the end of the working day. """

    slots = []

    for slot in range(nG):
        hour_index = slot % len(HOURS)

        if hour_index <= len(HOURS) - duration:
            slots.append(slot)

    return slots

# Precompute valid start slots for each event type.
valid_start_slots = {}

for jj, duration in this_week_sessions():
    valid_start_slots[jj] = valid_slots(this_week_sessions[durada_min(jj)])
