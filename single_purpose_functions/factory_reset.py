from dynamixel_sdk import *

PORT_NAME = "COM6"
BAUDRATE = 1000000
PROTOCOL_VERSION = 1.0
DXL_ID = 11

portHandler = PortHandler(PORT_NAME)
packetHandler = PacketHandler(PROTOCOL_VERSION)

portHandler.openPort()
portHandler.setBaudRate(BAUDRATE)

print(f"⚠️ Sending factory reset to motor ID {DXL_ID}...")

# Factory reset
dxl_comm_result, dxl_error = packetHandler.factoryReset(portHandler, DXL_ID)

if dxl_comm_result != COMM_SUCCESS:
    print(f"❌ Failed: {packetHandler.getTxRxResult(dxl_comm_result)}")
elif dxl_error != 0:
    print(f"⚠️ Packet Error: {packetHandler.getRxPacketError(dxl_error)}")
else:
    print("✅ Factory reset complete!")

portHandler.closePort()
