import nxbt
from time import sleep

# --- Movement Macro Definition ---
# This is the sequence you want to test.
# Sequence: +, Y, Down x22, A, A, Wait 5s, Left 2s, Up 1s, A, A

wa_5_day_up = "16"
wa_19_night_down = "22"

FAST_TRAVEL=f"""w
0.2s
PLUS 0.1s
0.2s
Y 0.1s
0.2s
LOOP {wa_5_day_up}
    DPAD_UP 0.092s
    0.2s

A 0.1s
0.7s
A 0.1s
5.0s
"""

DAY_NIGHT_CYCLE = """
0.2s
PLUS 0.1s
0.2s
Y 0.1s
0.2s
LOOP 22
    DPAD_DOWN 0.092s
    0.2s

A 0.1s
0.7s
A 0.1s

5.0s

L_STICK@-100+000 1.5s
0.2s
L_STICK@+000+100 1.0s
0.2s


A 0.1s
0.6s
A 0.1s
0.6s
A 0.1s
0.6s
A 0.1s
0.6s
A 0.1s
0.6s
A 0.1s
0.6s
A 0.1s

15.0s

L_STICK@+000-100 0.5s
A 0.1s
0.6s
A 0.1s
0.6s
A 0.1s
0.6s
A 0.1s
0.6s
A 0.1s
0.6s
A 0.1s
0.6s
A 0.1s

20.0s
"""


def main():
    """
    Connects to the Switch and runs the movement macro once for testing.
    """
    # Initialize NXBT
    nx = nxbt.Nxbt()

    # Create a single Pro Controller
    print("Creating controller...")
    controller_index = -1
    try:
        controller_index = nx.create_controller(nxbt.PRO_CONTROLLER)
        
        # Wait for the Switch to connect
        print("Ready to connect. Please go to the 'Change Grip/Order' menu on your Switch.")
        nx.wait_for_connection(controller_index)
        print("Connected!")
        
        input("Press Enter to start the movement macro test...")

        # --- Run the Movement Macro Once ---
        print("--- Running Movement Macro Test ---")
        # Using block=True makes the script wait here until the macro is finished.
        # This is simpler for a single-run test script.
        # nx.macro(controller_index, DAY_NIGHT_CYCLE, block=True)
        while True:
            for travel in range(100):
                nx.macro(controller_index, FAST_TRAVEL, block=True)
                print(f"Encounter {travel + 1}/100")
            print("It's getting late, passing time for day/night cycle...")
            sleep(2)
            nx.macro(controller_index, DAY_NIGHT_CYCLE, block=True)
    except KeyboardInterrupt:
        print("\nScript stopped by user.")
    
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

    finally:
        # Cleanly disconnect the controller
        print("Disconnecting controller...")
        if controller_index != -1:
            nx.remove_controller(controller_index)
        print("Disconnected.")


if __name__ == "__main__":
    main()
