import struct
import threading

from modbus_tk.modbus_rtu_over_tcp import RtuOverTcpMaster
from modbus_tk.hooks import call_hooks
from modbus_tk.modbus_rtu import RtuQuery
from modbus_tk.modbus_tcp import TcpMaster
from modbus_tk.utils import to_data
from modbus_tk import LOGGER
from modbus_tk import defines
from modbus_tk.exceptions import (
    ModbusError, ModbusFunctionNotSupportedError, DuplicatedKeyError, MissingKeyError, InvalidModbusBlockError,
    InvalidArgumentError, OverlapModbusBlockError, OutOfModbusBlockError, ModbusInvalidResponseError,
    ModbusInvalidRequestError
)
from modbus_tk.hooks import call_hooks
from modbus_tk.utils import threadsafe_function, get_log_buffer


class RtuOverTcpMasterSpecial(RtuOverTcpMaster):

    def _recv(self, expected_length=-1):
        """Receive the response from the slave"""
        response = to_data('')
        length = 255
        while len(response) < length:
            rcv_byte = self._sock.recv(1)
            if rcv_byte:
                response += rcv_byte
            if expected_length >= 0 and len(response) >= expected_length:
                break
        retval = call_hooks("modbus_rtu_over_tcp.RtuOverTcpMaster.after_recv", (self, response))
        if retval is not None:
            return retval
        return response

    def _make_query(self):
        """Returns an instance of a Query subclass implementing the modbus RTU protocol"""
        return RtuQuery()

    @threadsafe_function
    def execute(
            self, slave, function_code, starting_address, quantity_of_x=0, output_value=0, data_format="",
            expected_length=-1, write_starting_address_FC23=0):
        """
        Execute a modbus query and returns the data part of the answer as a tuple
        The returned tuple depends on the query function code. see modbus protocol
        specification for details
        data_format makes possible to extract the data like defined in the
        struct python module documentation
        """

        pdu = ""
        is_read_function = False
        nb_of_digits = 0

        # open the connection if it is not already done
        self.open()

        # Build the modbus pdu and the format of the expected data.
        # It depends of function code. see modbus specifications for details.
        if function_code == defines.READ_COILS or function_code == defines.READ_DISCRETE_INPUTS:
            is_read_function = True
            pdu = struct.pack(">BHH", function_code, starting_address, quantity_of_x)
            byte_count = quantity_of_x // 8
            if (quantity_of_x % 8) > 0:
                byte_count += 1
            nb_of_digits = quantity_of_x
            if not data_format:
                data_format = ">" + (byte_count * "B")
            if expected_length < 0:
                # No length was specified and calculated length can be used:
                # slave + func + bytcodeLen + bytecode + crc1 + crc2
                expected_length = byte_count + 5

        elif function_code == defines.READ_INPUT_REGISTERS or function_code == defines.READ_HOLDING_REGISTERS:
            is_read_function = True
            pdu = struct.pack(">BHH", function_code, starting_address, quantity_of_x)
            if not data_format:
                data_format = ">" + (quantity_of_x * "H")
            if expected_length < 0:
                # No length was specified and calculated length can be used:
                # slave + func + bytcodeLen + bytecode x 2 + crc1 + crc2
                expected_length = 2 * quantity_of_x + 5
                expected_length += 2

        elif (function_code == defines.WRITE_SINGLE_COIL) or (function_code == defines.WRITE_SINGLE_REGISTER):
            if function_code == defines.WRITE_SINGLE_COIL:
                if output_value != 0:
                    output_value = 0xff00
                fmt = ">BHH"
            else:
                fmt = ">BH" + ("H" if output_value >= 0 else "h")
            pdu = struct.pack(fmt, function_code, starting_address, output_value)
            if not data_format:
                data_format = ">HH"
            if expected_length < 0:
                # No length was specified and calculated length can be used:
                # slave + func + adress1 + adress2 + value1+value2 + crc1 + crc2
                expected_length = 8

        elif function_code == defines.WRITE_MULTIPLE_COILS:
            byte_count = len(output_value) // 8
            if (len(output_value) % 8) > 0:
                byte_count += 1
            pdu = struct.pack(">BHHB", function_code, starting_address, len(output_value), byte_count)
            i, byte_value = 0, 0
            for j in output_value:
                if j > 0:
                    byte_value += pow(2, i)
                if i == 7:
                    pdu += struct.pack(">B", byte_value)
                    i, byte_value = 0, 0
                else:
                    i += 1
            if i > 0:
                pdu += struct.pack(">B", byte_value)
            if not data_format:
                data_format = ">HH"
            if expected_length < 0:
                # No length was specified and calculated length can be used:
                # slave + func + adress1 + adress2 + outputQuant1 + outputQuant2 + crc1 + crc2
                expected_length = 8

        elif function_code == defines.WRITE_MULTIPLE_REGISTERS:
            if output_value and data_format:
                byte_count = struct.calcsize(data_format)
            else:
                byte_count = 2 * len(output_value)
            pdu = struct.pack(">BHHB", function_code, starting_address, byte_count // 2, byte_count)
            if output_value and data_format:
                pdu += struct.pack(data_format, *output_value)
            else:
                for j in output_value:
                    fmt = "H" if j >= 0 else "h"
                    pdu += struct.pack(">" + fmt, j)
            # data_format is now used to process response which is always 2 registers:
            #   1) data address of first register, 2) number of registers written
            data_format = ">HH"
            if expected_length < 0:
                # No length was specified and calculated length can be used:
                # slave + func + adress1 + adress2 + outputQuant1 + outputQuant2 + crc1 + crc2
                expected_length = 8

        elif function_code == defines.READ_EXCEPTION_STATUS:
            pdu = struct.pack(">B", function_code)
            data_format = ">B"
            if expected_length < 0:
                # No length was specified and calculated length can be used:
                expected_length = 5

        elif function_code == defines.DIAGNOSTIC:
            # SubFuncCode  are in starting_address
            pdu = struct.pack(">BH", function_code, starting_address)
            if len(output_value) > 0:
                for j in output_value:
                    # copy data in pdu
                    pdu += struct.pack(">B", j)
                if not data_format:
                    data_format = ">" + (len(output_value) * "B")
                if expected_length < 0:
                    # No length was specified and calculated length can be used:
                    # slave + func + SubFunc1 + SubFunc2 + Data + crc1 + crc2
                    expected_length = len(output_value) + 6

        elif function_code == defines.READ_WRITE_MULTIPLE_REGISTERS:
            is_read_function = True
            byte_count = 2 * len(output_value)
            pdu = struct.pack(
                ">BHHHHB",
                function_code, starting_address, quantity_of_x, write_starting_address_FC23,
                len(output_value), byte_count
            )
            for j in output_value:
                fmt = "H" if j >= 0 else "h"
                # copy data in pdu
                pdu += struct.pack(">" + fmt, j)
            if not data_format:
                data_format = ">" + (quantity_of_x * "H")
            if expected_length < 0:
                # No lenght was specified and calculated length can be used:
                # slave + func + bytcodeLen + bytecode x 2 + crc1 + crc2
                expected_length = 2 * quantity_of_x + 5
        else:
            raise ModbusFunctionNotSupportedError("The {0} function code is not supported. ".format(function_code))

        # instantiate a query which implements the MAC (TCP or RTU) part of the protocol
        query = self._make_query()

        # add the mac part of the protocol to the request
        request = query.build_request(pdu, slave)

        # send the request to the slave
        retval = call_hooks("modbus.Master.before_send", (self, request))
        if retval is not None:
            request = retval
        if self._verbose:
            LOGGER.debug(get_log_buffer("-> ", request))
        self._send(request)

        call_hooks("modbus.Master.after_send", (self,))

        if slave != 0:
            # receive the data from the slave
            response = self._recv(expected_length)
            retval = call_hooks("modbus.Master.after_recv", (self, response))
            if retval is not None:
                response = retval
            if self._verbose:
                LOGGER.debug(get_log_buffer("<- ", response))

            # extract the pdu part of the response
            response_pdu = query.parse_response(response)

            # 去除地址 10 00
            response_pdu = response_pdu[0:1] + response_pdu[3:]

            # analyze the received data
            (return_code, byte_2) = struct.unpack(">BB", response_pdu[0:2])

            if return_code > 0x80:
                # the slave has returned an error
                exception_code = byte_2
                raise ModbusError(exception_code)
            else:
                if is_read_function:
                    # get the values returned by the reading function
                    byte_count = byte_2
                    data = response_pdu[2:]
                    if byte_count != len(data):
                        # the byte count in the pdu is invalid
                        raise ModbusInvalidResponseError(
                            "Byte count is {0} while actual number of bytes is {1}. ".format(byte_count, len(data))
                        )
                else:
                    # returns what is returned by the slave after a writing function
                    data = response_pdu[1:]

                # returns the data as a tuple according to the data_format
                # (calculated based on the function or user-defined)
                result = struct.unpack(data_format, data)
                if nb_of_digits > 0:
                    digits = []
                    for byte_val in result:
                        for i in range(8):
                            if len(digits) >= nb_of_digits:
                                break
                            digits.append(byte_val % 2)
                            byte_val = byte_val >> 1
                    result = tuple(digits)
                return result
