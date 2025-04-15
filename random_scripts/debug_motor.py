from dynamixel_sdk import *

# === CONFIG ===
PORT_NAME = 'COM6'
BAUDRATE = 1000000
PROTOCOL_VERSION = 1.0

DXL_ID = 12

# === ADDRESS MAP ===
ADDR_TORQUE_ENABLE = 24
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0
ADDR_GOAL_POSITION = 30
ADDR_PRESENT_POSITION = 36
ADDR_MOVING_SPEED = 32

# === SETUP ===
portHandler = PortHandler(PORT_NAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

# === OPEN PORT ===
if not portHandler.openPort():
    print("❌ Failed to open port")
    quit()
print("✅ Port opened")

if not portHandler.setBaudRate(BAUDRATE):
    print("❌ Failed to set baudrate")
    portHandler.closePort()
    quit()
print("✅ Baudrate set")

# === PING MOTOR ===
print(f"\n🔍 Pinging motor with ID {DXL_ID}...")
model_number, dxl_comm_result, dxl_error = packetHandler.ping(portHandler, DXL_ID)
if dxl_comm_result != COMM_SUCCESS:
    print(f"❌ Ping failed: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"⚠️ Ping error: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print(f"✅ Motor responded! Model: {model_number}")

# === READ PRESENT POSITION ===
position, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
if dxl_comm_result != COMM_SUCCESS:
    print(f"❌ Read position failed: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"⚠️ Position read error: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print(f"📍 Current position: {position}")


packetHandler.write2ByteTxRx(portHandler, DXL_ID, 6, 0)       # CW limit
packetHandler.write2ByteTxRx(portHandler, DXL_ID, 8, 1023)    # CCW limit

# === ENABLE TORQUE ===
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print(f"❌ Torque enable failed: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"⚠️ Torque error: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print("✅ Torque enabled")

# === SET SPEED (OPTIONAL) ===
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_MOVING_SPEED, 500)
if dxl_comm_result != COMM_SUCCESS:
    print(f"❌ Speed set failed: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"⚠️ Speed error: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print("✅ Speed set to 500")

# === MOVE MOTOR ===
goal_position = 100
print(f"➡️ Moving to {goal_position}...")
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, goal_position)
if dxl_comm_result != COMM_SUCCESS:
    print(f"❌ Move command failed: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"⚠️ Move command error: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print("✅ Move command sent")


# === CLOSE PORT ===
packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
portHandler.closePort()
print("🔌 Port closed")
