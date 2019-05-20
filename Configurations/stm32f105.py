#
# Copyright 2018 dotnfc <dotnfc@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Simple script for ida loadProcConfig configuration file generator
#
from cmsis_svd.parser import SVDParser

parser = SVDParser.for_packaged_svd('STMicro', 'STM32F105xx.svd')
allregs = []
blocksize = 0x400 - 1

fmt = "{:28}{:28}{:12}"
for peripheral in parser.get_device().peripherals:
    col1 = "area DATA " + peripheral.name
    base = peripheral.base_address
    if peripheral._address_block == None:
        limit= base + blocksize
    else:
        limit= base + peripheral._address_block.size - 1
        blocksize = peripheral._address_block.size - 1

    col2 = "0x{0:08X}:0x{1:08X}".format(base, limit)
    col3 = peripheral.name
    print(fmt.format(col1, col2, col3))
    
    for register in peripheral.registers:
        rname = peripheral.name + "_" + register.name # ._display_name
        raddr = "0x{0:08X}".format(base + register.address_offset)
        rdesc = register.description.replace ("\n", "")
        sreg = "{0:28}{1:16}{2}".format (rname, raddr, rdesc)
        allregs.append(sreg)

print "\n; **** REGISTERS\n"
for reg in allregs:
    print reg