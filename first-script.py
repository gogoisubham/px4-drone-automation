import asyncio
from mavsdk import System

async def takeoff_land():
    drone = System()
    
    await drone.connect(system_address="udp://127.0.0.1:14540")

    print("Waiting for drone to connect..")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("✅ Drone connected!")
            break    

    print("Waiting for a global position estimate..")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("✅ Global position estimate OK")
            break

    print("Arming drone..")
    await drone.action.arm()

    print("Taking off..")
    await drone.action.takeoff()

    await asyncio.sleep(10)

    print("Landing..")
    await drone.action.land()

    await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(takeoff_land())
