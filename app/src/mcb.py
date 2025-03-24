import ctypes
import enum
from typing import Optional

from app.src.logger import logger

# Constants
MCB_MSG_H1 = 0x5A
MCB_MSG_H2 = 0xA5
MCB_MSG_TX_CMD = 0x83
MCB_MSG_RX_CMD = 0x82

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

MBBMC_MSG_RUN_DATA_LEN = ctypes.sizeof(MCBRunDataFields)


class MCBRunDataMsg(ctypes.Union):
    _fields_ = [
        ('fields', MCBRunDataFields),
        ('raw', ctypes.c_uint8 * MBBMC_MSG_RUN_DATA_LEN),
    ]
    _anonymous_ = ('fields',)
    

class MBBMCSetDataFields(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ('fix1', ctypes.c_uint8),
        ('fix2', ctypes.c_uint8),
        ('m1mode', ctypes.c_uint8 * 2),
        ('m2mode', ctypes.c_uint8 * 2),
        ('m1dir', ctypes.c_uint8 * 2),
        ('m2dir', ctypes.c_uint8 * 2),
        ('m1polepairs', ctypes.c_uint8 * 2),
        ('m2polepairs', ctypes.c_uint8 * 2),
        ('m1maxspeed', ctypes.c_uint8 * 2),
        ('m2maxspeed', ctypes.c_uint8 * 2),
        ('m1maxcurrent', ctypes.c_uint8 * 2),
        ('m2maxcurrent', ctypes.c_uint8 * 2),
        ('m1acdecelrate', ctypes.c_uint8 * 2),
        ('m2acdecelrate', ctypes.c_uint8 * 2),
        ('m1holdcurrent', ctypes.c_uint8 * 2),
        ('m2holdcurrent', ctypes.c_uint8 * 2),
        ('Serialbaudrate', ctypes.c_uint8 * 2),
        ('CANbaudrate', ctypes.c_uint8 * 2),
        ('enableport', ctypes.c_uint8 * 2),
        ('encoder1linecount', ctypes.c_uint8 * 2),
        ('encoder2linecount', ctypes.c_uint8 * 2),
        ('m1voltrange', ctypes.c_uint8 * 2),
        ('m2voltrange', ctypes.c_uint8 * 2),
        ('pwmportconfig', ctypes.c_uint8 * 2),
        ('reserved', ctypes.c_uint8 * 2),
        ('reserved2', ctypes.c_uint8 * 2),
        ('driverID', ctypes.c_uint8 * 2),
    ]

# Define the size constant (match with the C macro MBBMC_MSG_SET_DATA_LEN)
MBBMC_MSG_SET_DATA_LEN = ctypes.sizeof(MBBMCSetDataFields)

class MBBMCSetDataMsg(ctypes.Union):
    _fields_ = [
        ('fields', MBBMCSetDataFields),
        ('raw', ctypes.c_uint8 * MBBMC_MSG_SET_DATA_LEN),
    ]
    _anonymous_ = ('fields',)

        
class MCBDataReturnMode(enum.Enum):
    RUN = 0
    SET = 1


# -------------------- Helper Functions --------------------

def parse_scaled_float16(data: ctypes.Array, scale: float = 0.1) -> float:
    return round(int.from_bytes(data, byteorder="big") * scale, 2)


def parse_int32(data: ctypes.Array) -> int:
    return int.from_bytes(data, byteorder="big", signed=True)


def mcb_run_data_status_parser(data: ctypes.Array) -> dict:
    status_bytes = int.from_bytes(data, byteorder="big").to_bytes(2, byteorder="big")
    parsed_status = MCBRunDataMStatusFields.from_buffer_copy(status_bytes)
    return parsed_status.as_dict()


# -------------------- Main Parser --------------------

def mcb_run_data_parser(data: bytes) -> Optional[dict]:
    if len(data) == MBBMC_MSG_RUN_DATA_LEN:

        run_data = MCBRunDataMsg.from_buffer_copy(data)

        return {
            "m1rpm": parse_int32(run_data.m1data),
            "m2rpm": parse_int32(run_data.m2data),
            "m1current": parse_scaled_float16(run_data.m1current),
            "m2current": parse_scaled_float16(run_data.m2current),
            "m1temp": parse_scaled_float16(run_data.m1temp),
            "m2temp": parse_scaled_float16(run_data.m2temp),
            "supply_vol": parse_scaled_float16(run_data.supply_vol),
            "m1status": mcb_run_data_status_parser(run_data.m1status),
            "m2status": mcb_run_data_status_parser(run_data.m2status),
        }
        
    else:
        return None
    

def mcb_set_data_parser(data: bytes) -> Optional[dict]:
    
    if len(data) == MBBMC_MSG_SET_DATA_LEN:
        
        set_data = MBBMCSetDataMsg.from_buffer_copy(data)
        
        return {
            "m1mode": parse_int32(set_data.m1mode),
            "m2mode": parse_int32(set_data.m2mode),
            "m1dir": parse_int32(set_data.m1dir),
            "m2dir": parse_int32(set_data.m2dir),
            "m1polepairs": parse_int32(set_data.m1polepairs),
            "m2polepairs": parse_int32(set_data.m2polepairs),
            "m1maxspeed": parse_int32(set_data.m1maxspeed),
            "m2maxspeed": parse_int32(set_data.m2maxspeed),
            "m1maxcurrent": parse_int32(set_data.m1maxcurrent),
            "m2maxcurrent": parse_int32(set_data.m2maxcurrent),
            "m1acdecelrate": parse_int32(set_data.m1acdecelrate),
            "m2acdecelrate": parse_int32(set_data.m2acdecelrate),
            "m1holdcurrent": parse_int32(set_data.m1holdcurrent),
            "m2holdcurrent": parse_int32(set_data.m2holdcurrent),
            "Serialbaudrate": parse_int32(set_data.Serialbaudrate),
            "CANbaudrate": parse_int32(set_data.CANbaudrate),
            "enableport": parse_int32(set_data.enableport),
            "encoder1linecount": parse_int32(set_data.encoder1linecount),
            "encoder2linecount": parse_int32(set_data.encoder2linecount),
            "m1voltrange": parse_int32(set_data.m1voltrange),
            "m2voltrange": parse_int32(set_data.m2voltrange),
            "pwmportconfig": parse_int32(set_data.pwmportconfig),
            "driverID": parse_int32(set_data.driverID),
        }
    
