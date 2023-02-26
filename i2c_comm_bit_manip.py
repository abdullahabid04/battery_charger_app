from requirements import *


def get_charge_current(current):
    return int(round(int(current), 0))


def get_charge_voltage(voltage):
    return int(round(int(voltage), 0))


def get_charging_mode(mode):
    if mode in ('', "", None):
        return
    else:
        if mode in (DIS_CHARGE, WAIT_CHARGE):
            return bin(int(COMMUNICATION_FORMATS[MODE][MODE_DIS_CHARGE], base=2))
        elif mode in (CONSTANT_CHARGE_CURRENT, CONSTANT_CHARGE_VOLTAGE, REFLEX_CHARGE):
            return bin(int(COMMUNICATION_FORMATS[MODE][MODE_CHARGE], base=2))
        else:
            return


def get_number_of_cells(cells, volts):
    no_of_cells = 0
    if cells not in ('', "", 0, None):
        no_of_cells = cells
    if volts not in ('', "", 0, None):
        no_of_cells = volts
    return no_of_cells


def get_reflex_type(reflex_type):
    if reflex_type in ('', "", None):
        return
    else:
        if reflex_type == REFLEX_TYPE_A:
            return bin(int(COMMUNICATION_FORMATS[REFLEX_TYPE][REFLEX_TYPE_A], base=2))
        elif reflex_type == REFLEX_TYPE_B:
            return bin(int(COMMUNICATION_FORMATS[REFLEX_TYPE][REFLEX_TYPE_B], base=2))
        else:
            return


def get_dis_charge_mode(mode):
    if mode in ('', "", None):
        return
    else:
        if mode == DIS_CHARGE_SHORT:
            return bin(int(COMMUNICATION_FORMATS[DIS_CHARGE_TYPE][DIS_CHARGE_SHORT], base=2))
        elif mode == DIS_CHARGE_DEEP:
            return bin(int(COMMUNICATION_FORMATS[DIS_CHARGE_TYPE][DIS_CHARGE_DEEP], base=2))
        elif mode == DIS_CHARGE_LONG:
            return bin(int(COMMUNICATION_FORMATS[DIS_CHARGE_TYPE][DIS_CHARGE_LONG], base=2))
        else:
            return


def get_battery_type(charge_type, no_of_cells):
    if charge_type in ('', "", None) or no_of_cells in ('', "", 0, None):
        return
    else:
        if charge_type == CONSTANT_CHARGE_CURRENT:
            return bin(int(COMMUNICATION_FORMATS[BATTERY_TYPE][CC], base=2))
        elif charge_type == CONSTANT_CHARGE_VOLTAGE:
            if no_of_cells == 3:
                return bin(int(COMMUNICATION_FORMATS[BATTERY_TYPE][CP_LEAD_ACID_3], base=2))
            elif no_of_cells == 6:
                return bin(int(COMMUNICATION_FORMATS[BATTERY_TYPE][CP_LEAD_ACID_6], base=2))
            elif no_of_cells == 12:
                return bin(int(COMMUNICATION_FORMATS[BATTERY_TYPE][CP_LEAD_ACID_12], base=2))
            elif no_of_cells == 14:
                return bin(int(COMMUNICATION_FORMATS[BATTERY_TYPE][CP_LEAD_ACID_14], base=2))
            else:
                return
        elif charge_type == REFLEX_CHARGE:
            if no_of_cells == 11:
                return bin(int(COMMUNICATION_FORMATS[BATTERY_TYPE][REFLEX_NI_CAD_11], base=2))
            elif no_of_cells == 19:
                return bin(int(COMMUNICATION_FORMATS[BATTERY_TYPE][REFLEX_NI_CAD_19], base=2))
            elif no_of_cells == 20:
                return bin(int(COMMUNICATION_FORMATS[BATTERY_TYPE][REFLEX_NI_CAD_20], base=2))
            elif no_of_cells == 22:
                return bin(int(COMMUNICATION_FORMATS[BATTERY_TYPE][REFLEX_NI_CAD_22], base=2))
            else:
                return
        else:
            return


def get_data_to_send(mode, charge_type, dis_charge_type, no_of_cells, charge_current, charge_voltage, reflex_type):
    return
