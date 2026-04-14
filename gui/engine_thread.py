import os, time
import pygame
from config             import PROFILES_DIR
from detector           import wait_for_controller, get_events
from normalizer         import normalize
from mapper             import Mapper
from core.output_router import OutputRouter
from gui.state          import state, add_log

def start(profile_name, mode):
    import threading
    state["running"] = True
    threading.Thread(target=_run, args=(profile_name, mode), daemon=True).start()

def _run(profile_name, mode):
    add_log("Initialisation pygame...", "INFO")
    pygame.init()
    pygame.joystick.init()
    path = os.path.join(PROFILES_DIR, f"{profile_name}.json")
    state["mapper"] = Mapper(path)
    state["router"] = OutputRouter(mode=mode)
    add_log("Manette virtuelle creee", "INFO")

    while state["running"]:
        try:
            joy = wait_for_controller()
            state["connected"]       = True
            state["controller_name"] = joy.get_name()
            add_log(f"Connectee : {joy.get_name()}", "INFO")

            while state["running"] and state["connected"]:
                try:
                    t0 = time.perf_counter()
                    for ev in get_events():
                        result = normalize(ev)
                        if result is None: continue
                        if isinstance(result, str):
                            name = result
                            if ev.type == pygame.JOYBUTTONDOWN:
                                state["pressed"].add(name)
                                state["input_count"] += 1
                                add_log(f"{name} presse", "ACTION")
                            else:
                                state["pressed"].discard(name)
                            action = state["mapper"].get(name)
                            state["router"].execute(name, action or {}, ev.type)
                        elif isinstance(result, tuple):
                            name, value = result
                            if   name == "AXIS_LX":   state["axis_lx"] = value
                            elif name == "AXIS_LY":   state["axis_ly"] = value
                            elif name == "AXIS_RX":   state["axis_rx"] = value
                            elif name == "AXIS_RY":   state["axis_ry"] = value
                            elif name == "TRIGGER_L":
                                state["trigger_l"] = (value+1)/2
                                state["pressed"].add("L2") if value>0.1 else state["pressed"].discard("L2")
                            elif name == "TRIGGER_R":
                                state["trigger_r"] = (value+1)/2
                                state["pressed"].add("R2") if value>0.1 else state["pressed"].discard("R2")
                            action = state["mapper"].get_axis(name)
                            if action:
                                state["router"].execute_axis(name, action, value)
                    state["latency_ms"] = (time.perf_counter()-t0)*1000
                    pygame.time.wait(8)
                except Exception as e:
                    state["connected"] = False
                    add_log(f"Deconnexion : {e}", "WARN")
                    break
        except Exception as e:
            state["connected"] = False
            add_log(f"Erreur : {e}", "ERROR")
            time.sleep(2)

    state["connected"] = False
    state["controller_name"] = "—"
    for k in ["axis_lx","axis_ly","axis_rx","axis_ry","trigger_l","trigger_r"]:
        state[k] = 0.0
    state["pressed"].clear()
    if state["router"]: state["router"].reset()
