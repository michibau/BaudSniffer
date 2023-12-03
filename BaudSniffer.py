"""Implementation of a baud sniffer."""

import os
import platform
import time
from typing import List, Tuple

import serial

### For Linux: /dev/ttyS1 etc. ; For Windows: COM1 etc.
SETTING_SERIAL_PORT = "COM4"
TIMEOUT_SERIAL_PORT_SEC = 10
BYTE_SIZE_TO_READ = 10

connection_list: List[Tuple[str, int]] = []

BAUDRATE_LIST = [
    110,
    300,
    600,
    1200,
    1800,
    2400,
    4800,
    9600,
    38400,
    14400,
    19200,
    38400,
    57600,
    115200,
    128000,
    256000,
]
SERIALPORT_SETTINGS_LIST = [
    "8N1",
    "8N2",
    "8E1",
    "8E2",
    "8O1",
    "8O2",
    "7N1",
    "7N2",
    "7E1",
    "7E2",
    "7O1",
    "7O2",
]


def _open_port(
    baud_set: int, bytesize_set: str, parity_set: str, stopbit_set: str
) -> bytes:
    new_bytesize_set = _set_bytesize(bytesize_set)
    new_parity_set = _set_parity(parity_set)
    new_stopbit_set = _set_stopbit(stopbit_set)

    port = serial.Serial(
        SETTING_SERIAL_PORT,
        baud_set,
        new_bytesize_set,
        new_parity_set,
        new_stopbit_set,
        timeout=TIMEOUT_SERIAL_PORT_SEC,
    )
    with port as s:
        data_serial = s.read(BYTE_SIZE_TO_READ)
    return data_serial


def _set_stopbit(stop_bit: str) -> int:
    return {"1": serial.STOPBITS_ONE, "2": serial.STOPBITS_TWO}[stop_bit]


def _set_bytesize(byte_size: str) -> int:
    byte_size_map = {
        "8": serial.EIGHTBITS,
        "7": serial.SEVENBITS,
        "6": serial.SIXBITS,
        "5": serial.FIVEBITS,
    }
    return byte_size_map[byte_size]


def _set_parity(parity: str) -> str:
    parity_map = {
        "N": serial.PARITY_NONE,
        "E": serial.PARITY_EVEN,
        "O": serial.PARITY_ODD,
        "M": serial.PARITY_MARK,
        "S": serial.PARITY_SPACE,
    }

    return parity_map[parity]


# serial port parameter = 8N1, 7N1 and so on
def _try_baudrate(serialport_parameter: str) -> None:
    new_serialport_parameter = _slice_serialport_parameter(serialport_parameter)
    for baudrate in BAUDRATE_LIST:
        serialdata = _open_port(
            baudrate,
            new_serialport_parameter[0],
            new_serialport_parameter[1],
            new_serialport_parameter[2],
        )
        bytes_in_text = serialdata.decode(encoding="UTF-8", errors="ignore")
        _display_text(baudrate, serialport_parameter, serialdata, bytes_in_text)

        is_valid_connection_option = _estimate_connection_quality(
            bytes_in_text, serialdata
        )
        if is_valid_connection_option:
            connection_list.append((serialport_parameter, baudrate))


def _slice_serialport_parameter(
    serialport_parameter_string: str
) -> Tuple[str, str, str]:
    if len(serialport_parameter_string) > 3:
        print("Paramemter to long: ", serialport_parameter_string)

    bytesize = serialport_parameter_string[slice(1)]  # ex. 8
    parity = serialport_parameter_string[slice(1, 2)]  # ex. N
    stopbit = serialport_parameter_string[slice(2, 3)]  # ex. 1

    return (bytesize, parity, stopbit)


def _estimate_connection_quality(text: str, serialdata: bytes) -> bool:
    """
    Check if a connection is valid based on specific criteria.

    Criteria:
    1. Check if UTF-8 encoded text is equal to serial data bytes.
    2. Ensure text is not empty.
    3. Verify that text contains only printable characters.

    Args:
    ----
        text (str): text
        serialdata (bytes): serial data

    Returns:
    -------
        bool: flag if connection can be established
    """
    if text.encode() == serialdata and text and text.isprintable():
        print("\n########### Connection probably ok #############\n")
        return True
    return False


def _display_text(
    actual_baud: int, actual_serialport_parameter: str, serial_data: bytes, text: str
) -> None:
    print("Parameter: ", actual_serialport_parameter, " | Baud:", actual_baud, " bps")
    print("\n")
    print("Text (UTF-8):\t", text)
    print("Serial Data:\t", serial_data)
    print("\n")


def _display_best_connection() -> None:
    best_baudrate = 0
    best_combination_text = ""

    connection_list.sort()
    print("\n\t Found the following Settings:\n")
    print("\n\t Serial Settings \t Baudrate\n")

    for port_num, baud_rate in connection_list:
        print(
            "\t",
            port_num,
            "\t\t\t\t",
            baud_rate,
            "bps",
        )

    for port_num, baud_rate in connection_list:
        if best_baudrate < baud_rate:
            best_baudrate = baud_rate
            best_combination_text = port_num + " " + str(baud_rate) + " bps"
    print("\n\n\tBest Connection:", best_combination_text)


def _stop_program() -> None:
    input("\nPress any key to exit ...\n")
    exit


def _return_duration() -> float:
    estimated_time_in_min = (
        len(BAUDRATE_LIST) * len(SERIALPORT_SETTINGS_LIST) * TIMEOUT_SERIAL_PORT_SEC
    ) * 0.0166667  # 1s = 0.0166667 min
    return round(estimated_time_in_min, 2)


def _check_for_wsl() -> None:
    if "Linux " in platform.platform():
        test = os.popen("ls /mnt/c").read()
        if test.__contains__("Windows"):
            print("\n\n\n\t\tAttention: \n")
            print(
                "\t\tIf you try to run the tool on WSL (Windows-Subsystem for Linux) please adjust the COM Port Parameter and use Windows."
            )
            print("\t\tThe script will fail at the moment for this constellation.")
            _stop_program()


def _check_for_windows() -> None:
    if "Windows" in platform.platform() and "COM" not in SETTING_SERIAL_PORT:
        print("\n\n\t\tPlease adjust the COM Port for Windows.")
        _stop_program()


def _check_for_linux() -> None:
    if "Linux" in platform.platform() and "COM" in SETTING_SERIAL_PORT:
        print("\n\n\t\tPlease adjust the COM Port for Linux.")
        _stop_program()


if __name__ == "__main__":
    script_start_time = time.time()
    _check_for_wsl()
    _check_for_windows()
    _check_for_linux()
    print("\nUsed Serial Port: \n", SETTING_SERIAL_PORT, "\n")
    print("Estimated Time: ", _return_duration(), "min\n")
    for serial_setting in SERIALPORT_SETTINGS_LIST:
        _try_baudrate(serial_setting)
    _display_best_connection()
    script_end_time = time.time()
    print(
        "\nRuntime: ",
        round((script_end_time - script_start_time) * 0.0166667, 2),
        " min",
    )  # 1s = 0.0166667 min
    _stop_program()
