from dynamixel_sdk import *
import time

DEVICENAME = 'COM6'
BAUDRATE = 1000000
PROTOCOL_VERSION = 1.0

DXL_IDS = [2, 3]
ADDR_GOAL_POSITION = 30
ADDR_MOVING_SPEED = 32
ADDR_PRESENT_POSITION = 36

SPEED = 100 # (0–1023)
STEP_DELAY = 2.0
ANGLE_RANGE = 200

portHandler = PortHandler(DEVICENAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

if not portHandler.openPort():
    print("❌ Port konnte nicht geöffnet werden.")
    exit()

if not portHandler.setBaudRate(BAUDRATE):
    print("❌ Baudrate konnte nicht gesetzt werden.")
    exit()

for dxl_id in DXL_IDS:
    packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_MOVING_SPEED, SPEED)

start_positions = {}
for dxl_id in DXL_IDS:
    pos, _, _ = packetHandler.read2ByteTxRx(portHandler, dxl_id, ADDR_PRESENT_POSITION)
    start_positions[dxl_id] = pos

targets = [+ANGLE_RANGE, 0, -ANGLE_RANGE, 0]

for offset in targets:
    for dxl_id in DXL_IDS:
        goal_position = max(0, min(1023, start_positions[dxl_id] + offset))
        packetHandler.write2ByteTxRx(portHandler, dxl_id, ADDR_GOAL_POSITION, goal_position)
    print(f"➡️ Bewegung zu Offset: {offset} (Warte {STEP_DELAY} Sekunden)")
    time.sleep(STEP_DELAY)

portHandler.closePort()
print("✅ Test abgeschlossen.")
