import itertools

# ---------------------------
# MOCHI (RABBIT FORM)
# ---------------------------

MOCHI_IDLE = [
r"""
   (\_/)
   ( •ᴗ• )
  / >🥕
""",

r"""
   (\_/)
   ( •‿• )
  / >🥕
""",

r"""
   (\_/)
   ( •_• )
  / >🥕
"""
]

MOCHI_HAPPY = [
r"""
   (\_/)
   ( ^‿^ )
  / >💖
""",

r"""
   (\_/)
   ( ^▽^ )
  / >✨
"""
]

MOCHI_SAD = [
r"""
   (\_/)
   ( •︵• )
  / >...
""",

r"""
   (\_/)
   ( T_T )
  / >...
"""
]

MOCHI_SLEEP = [
r"""
   (\_/)
   ( -.- )
  / >💤
"""
]

MOCHI_HUNGRY = [
r"""
   (\_/)
   ( X_X )
  / >🍂
""",

r"""
   (\_/)
   ( •﹏• )
  / >🍃
"""
]

# ---------------------------
# CYCLES
# ---------------------------
idle_cycle = itertools.cycle(MOCHI_IDLE)
happy_cycle = itertools.cycle(MOCHI_HAPPY)
sad_cycle = itertools.cycle(MOCHI_SAD)
sleep_cycle = itertools.cycle(MOCHI_SLEEP)
hungry_cycle = itertools.cycle(MOCHI_HUNGRY)


# ---------------------------
# PUBLIC API (IMPORTANT)
# ---------------------------
def get_frame(state):
    mood = state.get("mood", "calm")
    energy = state.get("energy", 5)
    hunger = state.get("hunger", 5)
    bond = state.get("bond", 5)

    # ---------------------------
    # SURVIVAL PRIORITY
    # ---------------------------
    if energy <= 2:
        return next(sleep_cycle)

    if hunger >= 8:
        return next(hungry_cycle)

    # ---------------------------
    # MOOD SYSTEM
    # ---------------------------
    if mood == "happy":
        return next(happy_cycle)

    if mood == "lonely":
        return next(sad_cycle)

    if mood == "tired":
        return next(sleep_cycle)

    # ---------------------------
    # BOND OVERRIDES
    # ---------------------------
    if bond >= 8:
        return r"""
   (\_/)
   ( ^‿^ )
  / >💖
"""

    if bond <= 2:
        return r"""
   (\_/)
   ( •︵• )
  / >...
"""

    # ---------------------------
    # DEFAULT
    # ---------------------------
    return next(idle_cycle)