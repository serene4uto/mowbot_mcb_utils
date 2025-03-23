import ctypes
import enum
from typing import Optional

# Constants
MCBRunDataMsgSize = 26
STATUS_FIELD_SIZE = 2


# -------------------- Data Structures --------------------

class MCBRunDataMStatusFields(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('current_overload', ctypes.c_uint8, 1),
        ('load_abnormal', ctypes.c_uint8, 1),
        ('temperature_protection', ctypes.c_uint8, 1),
        ('voltage_too_high', ctypes.c_uint8, 1),
        ('voltage_too_low', ctypes.c_uint8, 1),
        ('blocking_protection', ctypes.c_uint8, 1),
        ('hall_signal_abnormal', ctypes.c_uint8, 1),
        ('abnormal', ctypes.c_uint8, 1),
        ('reserved', ctypes.c_uint8, 8),
    ]

    def as_dict(self):
        return {
            field[0]: getattr(self, field[0])
            for field in self._fields_[:-1]  # Exclude 'reserved'
        }


class MCBRunDataFields(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('fix1', ctypes.c_uint8),
        ('fix2', ctypes.c_uint8),
        ('m1data', ctypes.c_uint8 * 4),
        ('m2data', ctypes.c_uint8 * 4),
        ('m1current', ctypes.c_uint8 * 2),
        ('m2current', ctypes.c_uint8 * 2),
        ('m1temp', ctypes.c_uint8 * 2),
        ('m2temp', ctypes.c_uint8 * 2),
        ('supply_vol', ctypes.c_uint8 * 2),
        ('m1status', ctypes.c_uint8 * 2),
        ('m2status', ctypes.c_uint8 * 2),
        ('unknown1', ctypes.c_uint8),
        ('unknown2', ctypes.c_uint8),
    ]


class MCBRunDataMsg(ctypes.Union):
    _fields_ = [
        ('fields', MCBRunDataFields),
        ('raw', ctypes.c_uint8 * MCBRunDataMsgSize),
    ]
    _anonymous_ = ('fields',)


class MCBDataReturnMode(enum.Enum):
    RUN = 0
    SET = 1


# -------------------- Helper Functions --------------------

def parse_scaled_uint16(data: ctypes.Array, scale: float = 0.1) -> float:
    return round(int.from_bytes(data, byteorder="big") * scale, 2)


def parse_int32(data: ctypes.Array) -> int:
    return int.from_bytes(data, byteorder="big", signed=True)


def mcb_run_data_status_parser(data: ctypes.Array) -> dict:
    status_bytes = int.from_bytes(data, byteorder="big").to_bytes(STATUS_FIELD_SIZE, byteorder="big")
    parsed_status = MCBRunDataMStatusFields.from_buffer_copy(status_bytes)
    return parsed_status.as_dict()


# -------------------- Main Parser --------------------

def mcb_data_parser(data: bytes, mode: MCBDataReturnMode) -> Optional[dict]:
    if mode == MCBDataReturnMode.RUN:
        if len(data) != MCBRunDataMsgSize:
            return None

        run_data = MCBRunDataMsg.from_buffer_copy(data)

        return {
            "m1rpm": parse_int32(run_data.m1data),
            "m2rpm": parse_int32(run_data.m2data),
            "m1current": parse_scaled_uint16(run_data.m1current),
            "m2current": parse_scaled_uint16(run_data.m2current),
            "m1temp": parse_scaled_uint16(run_data.m1temp),
            "m2temp": parse_scaled_uint16(run_data.m2temp),
            "supply_vol": parse_scaled_uint16(run_data.supply_vol),
            "m1status": mcb_run_data_status_parser(run_data.m1status),
            "m2status": mcb_run_data_status_parser(run_data.m2status),
        }

    elif mode == MCBDataReturnMode.SET:
        # Handle SET mode parsing if needed
        return None

    else:
        raise ValueError(f"Unsupported mode: {mode}")
