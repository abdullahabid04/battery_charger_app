import json
import os
import io

FILE_TYPE = ".json"
CHARGE_TYPES = "charging_types" + FILE_TYPE
COMM_FORMAT = "i2c_comm_data_format" + FILE_TYPE

with io.open(os.path.join(os.getcwd(), CHARGE_TYPES), 'r') as charging:
    CHARGING_MODES = json.load(charging)

with io.open(os.path.join(os.getcwd(), COMM_FORMAT), 'r') as charging_format:
    COMMUNICATION_FORMATS = json.load(charging_format)

LABELS_OF_BUTTONS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", ":", "0", ".", ]

CONSTANT_CHARGE_CURRENT = "CONSTANT_CURRENT"
CONSTANT_CHARGE_VOLTAGE = "CONSTANT_VOLTAGE"
REFLEX_CHARGE = "REFLEX_CHARGE"
DIS_CHARGE = "DIS_CHARGE"
WAIT_CHARGE = "WAIT_CHARGE"

CHARGE_TYPE_SELECTION = [CONSTANT_CHARGE_CURRENT, CONSTANT_CHARGE_VOLTAGE, REFLEX_CHARGE, DIS_CHARGE, WAIT_CHARGE]

CONSTANT_CURRENT_CHARGE = "constant_current_charge"
CC_CHARGE_CURRENT = "cc_charge_current"
CC_CHARGE_TIME = "cc_charge_time"
CC_CHARGE_VOLTAGE = "cc_charge_voltage"
CC_TERMINATE_ON = "cc_terminate_on"
CC_OPTIONAL_ALERTS = "cc_optional_alerts"

CONSTANT_VOLTAGE_CHARGE = "constant_voltage_charge"
CP_CHARGE_CURRENT = "cp_charge_current"
CP_CHARGE_TIME = "cp_charge_time"
CP_CHARGE_VOLTAGE = "cp_charge_voltage"
CP_OPTIONAL_ALERTS = "cp_optional_alerts"

CHARGE_REFLEX = "reflex_charge"
RC_CHARGE_CURRENT = "rc_charge_current"
RC_CHARGE_TIME = "rc_charge_time"
RC_NO_OF_CELLS = "rc_no_of_cells"
RC_REFLEX_TYPE = "rc_reflex_type"
RC_OPTIONAL_ALERTS = "rc_optional_alerts"

CHARGE_DIS = "dis_charge"
DC_DIS_CHARGE_CURRENT = "dc_dis_charge_current"
DC_DIS_CHARGE_TIME = "dc_dis_charge_time"
DC_DIS_CHARGE_VOLTAGE = "dc_dis_charge_voltage"
DC_OPTIONAL_ALERTS = "dc_optional_alerts"

CHARGE_WAIT = "wait_charge"
WC_WAIT_TIME = "wc_wait_time"

MODE = "mode"
REFLEX_TYPE = "reflex_type"
DIS_CHARGE_TYPE = "dis_charge_type"
BATTERY_TYPE = "battery_type"

MODE_CELL_TEST = "cell_test"
MODE_CHARGE = "charge"
MODE_DIS_CHARGE = "dis_charge_wait"
MODE_2_STEP_CC = "step_2_cc"
MODE_ANALYZE = "analyze"
MODE_ANALYZE_WAIT = "analyze_wait"

REFLEX_TYPE_A = "A"
REFLEX_TYPE_B = "B"

DIS_CHARGE_SHORT = "short"
DIS_CHARGE_LONG = "long"
DIS_CHARGE_DEEP = "deep"

CC = "CC"
CP_LEAD_ACID_3 = "CP_lead_acid_3"
CP_LEAD_ACID_6 = "CP_lead_acid_6"
CP_LEAD_ACID_12 = "CP_lead_acid_12"
CP_LEAD_ACID_14 = "CP_lead_acid_14"
REFLEX_NI_CAD_11 = "Reflex_Ni_CAD_11"
REFLEX_NI_CAD_19 = "Reflex_Ni_CAD_19"
REFLEX_NI_CAD_20 = "Reflex_Ni_CAD_20"
REFLEX_NI_CAD_22 = "Reflex_Ni_CAD_22"
