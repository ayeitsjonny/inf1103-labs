import time

elapsed_seconds = 0        # tracks how long the simulation has been running
light_index = 0            # 0 = Green, 1 = Yellow, 2 = Red (cycles through)
seconds_per_light = 2      # how long each light stays on

while elapsed_seconds < 10:
    # Selection control flow: decide what to print based on the current light
    if light_index == 0:
        light = "Green"
        print(f"Light: {light} -> Go")
    elif light_index == 1:
        light = "Yellow"
        print(f"Light: {light} -> Slow Down")
    elif light_index == 2:
        light = "Red"
        print(f"Light: {light} -> Stop")

    time.sleep(seconds_per_light)
    elapsed_seconds = elapsed_seconds + seconds_per_light

    # Cycle back to Green after Red
    light_index = light_index + 1
    if light_index > 2:
        light_index = 0

print("Simulation ended (10 seconds elapsed).")