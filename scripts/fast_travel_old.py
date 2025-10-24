import nxbt
import time
import threading

# --- Timing Configuration ---
# You can adjust these values to fine-tune the macro's speed and reliability.
# How long to simulate holding a button down (in seconds).
PRESS_DURATION = 0.075 
# How long to wait after most button presses.
REST_DURATION = 0.25
# Specific, longer delay between two identical, rapid presses (like A, A).
DOUBLE_PRESS_DELAY = 0.5 

# Initialize NXBT
nx = nxbt.Nxbt()

# Global flag to control the macro loop
macro_running = False

def reliable_press(controller_index, button, press_duration, rest_duration):
    """
    Performs a more reliable button press by controlling the press, hold, 
    release, and rest periods.
    """
    # Create an input packet to press the specified button
    packet = nx.create_input_packet()
    packet[button] = True
    
    # Press and hold the button
    nx.set_controller_input(controller_index, packet)
    time.sleep(press_duration)
    
    # Release the button
    packet = nx.create_input_packet() # Creates a packet with all buttons released
    nx.set_controller_input(controller_index, packet)
    time.sleep(rest_duration)


def macro_loop(controller_index):
    """
    Contains the sequence of button presses to be executed on the Switch.
    This loop now uses the reliable_press function for consistency.
    """
    global macro_running
    print("Macro sequence started. Press Ctrl+C in this terminal to stop.")
    
    # A brief pause to ensure the connection is fully stable
    time.sleep(1)

    while macro_running:
        if not macro_running:
            break
        
        print("Executing macro loop...")

        # 1. Press Start (+)
        reliable_press(controller_index, "PLUS", PRESS_DURATION, REST_DURATION)

        # 2. Press Y
        reliable_press(controller_index, "Y", PRESS_DURATION, REST_DURATION)

        # 3. Go up 16 times
        for i in range(16):
            if not macro_running:
                break
            print(f"  - D-Pad Up: {i+1}/16")
            reliable_press(controller_index, "DPAD_UP", PRESS_DURATION, 0.1) # A shorter delay for D-Pad is often fine
        
        if not macro_running:
            break

        # 4. Press A, wait, then press A again
        print("  - Pressing A (first time)")
        reliable_press(controller_index, "A", PRESS_DURATION, REST_DURATION)
        
        # THIS IS THE FIX: Add a specific, longer pause before the second press
        # to allow the Switch UI to update.
        print(f"  - Pausing for {DOUBLE_PRESS_DELAY}s before second A press")
        time.sleep(DOUBLE_PRESS_DELAY)

        # Only press the second 'A' if the macro is still supposed to be running
        if macro_running:
            print("  - Pressing A (second time)")
            reliable_press(controller_index, "A", PRESS_DURATION, REST_DURATION)

        # 5. Wait for 5 seconds
        print("Waiting for 5 seconds...")
        for _ in range(5):
            if not macro_running:
                break
            time.sleep(1)

    print("Macro loop finished.")

def main():
    """
    Main function to handle Switch connection and user input to trigger the macro.
    """
    global macro_running
    controller_index = -1

    try:
        controller_index = nx.create_controller(nxbt.PRO_CONTROLLER)
        
        print("Ready to connect. Go to the 'Change Grip/Order' menu on your Switch.")
        nx.wait_for_connection(controller_index)
        print("Connected!")

        input("Press Enter to start the macro...")

        macro_running = True
        macro_thread = threading.Thread(target=macro_loop, args=(controller_index,))
        macro_thread.start()

        while macro_thread.is_alive():
            macro_thread.join(0.1)

    except KeyboardInterrupt:
        print("\nStopping macro...")
        macro_running = False
        if 'macro_thread' in locals() and macro_thread.is_alive():
            macro_thread.join()
        print("Macro stopped.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Disconnecting controller...")
        if controller_index != -1:
             nx.remove_controller(controller_index)
        print("Disconnected.")

if __name__ == "__main__":
    main()
