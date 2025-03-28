import asyncio
from mavsdk import System

async def run():
    # Step 1: Create a drone object
    drone = System()
    
    # Step 2: Connect to the drone (default PX4 SITL address)
    await drone.connect(system_address="udp://:14540")

    # Step 3: Wait until the drone is connected
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("✅ Drone connected!")
            break    

    # Step 4: Wait until the drone has a global position estimate
    print("Waiting for a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("✅ Global position estimate OK")
            break

    # Step 5: Arm the drone
    print("Arming drone...")
    await drone.action.arm()

    # Step 6: Take off
    print("Taking off...")
    await drone.action.takeoff()

    # Step 7: Wait while it's climbing
    await asyncio.sleep(10)

    # Step 8: Land the drone
    print("Landing...")
    await drone.action.land()

    # Step 9: Wait until landed
    await asyncio.sleep(10)

# Start the asyncio event loop
if __name__ == "__main__":
    asyncio.run(run())
