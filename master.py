# -*- coding: utf_8 -*-
import binascii
import sys
import logging
import time
import traceback

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import modbus_tk.modbus_rtu_over_tcp as modbus_rtu_over_tcp
import modbus_rtu_over_tcp_special

logger = modbus_tk.utils.create_logger("console")

import struct

if __name__ == "__main__":
    try:
        # 连接MODBUS TCP从机
        # master = modbus_tcp.TcpMaster(host="192.168.1.254", port=4001)
        master = modbus_rtu_over_tcp_special.RtuOverTcpMasterSpecial(host="192.168.1.48", port=4001)
        # master = modbus_tcp.TcpMaster(host="192.168.1.48", port=4001)
        # master = modbus_tcp.TcpMaster(host="192.168.127.254", port=502)
        logger.info("connected")
        print('connected')
        # 读保持寄存器
        master.set_timeout(10)
        master.set_verbose(True)
        try:
            msg = time.strftime('%Y-%m-%y %H:%M:%S')
            res1 = master.execute(0xcb, 3, 0x1000, 0x0014)
            # res1 = master.execute(0x01, 0x02, 0x0000, 16)
            # res1 = master.execute(0xcb, 3, 4230, 124)
            # res1 = master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 10)
            # res1 = master.execute(1, 2, 1, 0xF)
            print('res1 = ', res1)
            # t1 = hex(res1[0])[2:] + hex(res1[1])[2:]
            # print("t1", t1)
            # t2 = struct.unpack('>f', binascii.unhexlify(t1.replace(' ', '')))[0]
            # print("t2", t2)
        except Exception as e:
            print("e=", e)


        # 读输入寄存器
        # logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 0, 16))  #功能码 4
        # # 读线圈寄存器
        # logger.info(master.execute(1, cst.READ_COILS, 0, 16))  #功能码   1
        # # 读离散输入寄存器
        # logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 16))  #功能码 2

        # 单个读写寄存器操作

        # # 写寄存器地址为0的线圈寄存器，写入内容为0（位操作）
        # logger.info(master.execute(3, cst.WRITE_SINGLE_COIL, 0x0143, output_value=1))  #功能码    5
        # logger.info(master.execute(3, cst.READ_COILS, 0x0140, 6))  #功能码  1

        # 多个寄存器读写操作
        # 写寄存器起始地址为0的保持寄存器，操作寄存器个数为4
        # logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0, output_value=[5, 4, 3, 2, 1]))  #功能码   15
        # logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 4))  #功能码   3
        # # 写寄存器起始地址为0的线圈寄存器
        # logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[1, 1, 1, 1]))  #功能码  16
        # logger.info(master.execute(1, cst.READ_COILS, 0, 4))  #功能码   1
    except modbus_tk.modbus.ModbusError as e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))
