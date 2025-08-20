from neopixel_control import NeoPixelControl

def run_test():
    print("--- Running NeoPixelControl Simulation Test ---")

    # Initialize in simulation mode
    npc = NeoPixelControl(simulation=True)

    # Test 1: Set a single pixel
    print("\n--- Test 1: Set a single pixel ---")
    npc.set_pixel(0, 0, (255, 0, 0))
    # In a real test, we would assert the state of the pixel.
    # For now, we rely on the print statements from the simulation.

    # Test 2: Fill the matrix
    print("\n--- Test 2: Fill the matrix ---")
    npc.fill((0, 255, 0))

    # Test 3: Clear the matrix
    print("\n--- Test 3: Clear the matrix ---")
    npc.clear()

    # Test 4: Run an animation
    print("\n--- Test 4: Run an animation ---")
    npc.run_animation("rainbow")
    npc.animate()

    # Test 5: Load a pattern
    print("\n--- Test 5: Load a pattern ---")
    pattern = [[(255, 255, 255) for _ in range(16)] for _ in range(16)]
    npc.load_pattern(pattern)

    # Test 6: Get a pattern
    print("\n--- Test 6: Get a pattern ---")
    retrieved_pattern = npc.get_pattern()
    if retrieved_pattern == pattern:
        print("Pattern retrieved successfully.")
    else:
        print("Error: Retrieved pattern does not match the loaded pattern.")

    print("\n--- NeoPixelControl Simulation Test Complete ---")

if __name__ == "__main__":
    run_test()
