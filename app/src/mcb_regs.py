

MCB_DATA_MODE_REG = 0x1005  # 0: Operating Data, 1: Setting DataMCB
MCB_MOTOR1_MODE_REG = 0x0010  # 0: Open Loop, 1: Speed Closed Loop, 2: Position Closed Loop
MCB_MOTOR2_MODE_REG = 0x0011  # 0: Open Loop, 1: Speed Closed Loop, 2: Position Closed LoopMCB
MCB_MOTOR1_DIR_REG = 0x0012  # 0: Forward, 1: Reverse
MCB_MOTOR2_DIR_REG = 0x0013  # 0: Forward, 1: ReverseMCB
MCB_MOTOR1_POLE_PAIRS_REG = 0x0014  # 1-20
MCB_MOTOR2_POLE_PAIRS_REG = 0x0015  # 1-20MCB
MCB_MOTOR1_MAX_SPEED_REG = 0x0016  # 100–30,000
MCB_MOTOR2_MAX_SPEED_REG = 0x0017  # 100–30,000MCB
MCB_MOTOR1_MAX_CURRENT_REG = 0x0018  # 0–nominal current
MCB_MOTOR2_MAX_CURRENT_REG = 0x0019  # 0–nominal currentMCB
MCB_MOTOR1_ACCEL_DECEL_RATE_REG = 0x001A  # 1–30
MCB_MOTOR2_ACCEL_DECEL_RATE_REG = 0x001B  # 1–30MCB
MCB_MOTOR1_HOLD_CURRENT_REG = 0x001C  # 0–100 (0.1A)
MCB_MOTOR2_HOLD_CURRENT_REG = 0x001D  # 0–100 (0.1A)MCB
MCB_SERIAL_BAUD_RATE_REG = 0x001E  # 0:4800, ..., 7:115200
MCB_CAN_BAUD_RATE_REG = 0x001F     # 0:50K, ..., 9:1MMCB
MCB_ENABLE_PORT_REG = 0x0020  # 0: Disable, 1: EnableMCB
MCB_ENCODER1_LINE_COUNT_REG = 0x0021  # 100-5000
MCB_ENCODER2_LINE_COUNT_REG = 0x0022  # 100-5000MCB
MCB_MOTOR1_VOLTAGE_RANGE_REG = 0x0023  # Format: upper 2 digits high voltage, lower 2 digits low voltage, e.g., 7218
MCB_MOTOR2_VOLTAGE_RANGE_REG = 0x0024
MCB_PWM_PORT_CONFIG_REG = 0x0025  # 0: Mixed mode, 1: Independent modeMCB
MCB_RESERVED_REG = 0x0026
MCB_RESERVED2_REG = 0x0027
MCB_DRIVER_ID_REG = 0x0028  # 1-100
