from dynamixel_sdk import *

PORT_NAME = 'COM6'
BAUDRATE = 1000000
PROTOCOL_VERSION = 1.0

portHandler = PortHandler(PORT_NAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

portHandler.openPort()
portHandler.setBaudRate(BAUDRATE)

print("🔎 Scanning for Dynamixel IDs...")

for dxl_id in range(0, 254):
    dxl_model_number, dxl_comm_result, dxl_error = packetHandler.ping(portHandler, dxl_id)
    if dxl_comm_result == COMM_SUCCESS:
        print(f"✅ Found device at ID: {dxl_id} (Model: {dxl_model_number})")

portHandler.closePort()
