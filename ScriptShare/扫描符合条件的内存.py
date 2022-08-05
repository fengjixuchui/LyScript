from LyScript32 import MyDebug

# 传入汇编指令,获取该指令的机器码
def get_assembly_machine_code(dbg,asm):
    machine_code_list = []

    # 开辟堆空间
    alloc_address = dbg.create_alloc(1024)
    print("分配堆: {}".format(hex(alloc_address)))

    # 得到汇编机器码
    machine_code = dbg.assemble_write_memory(alloc_address,asm)
    if machine_code == False:
        dbg.delete_alloc(alloc_address)

    # 得到汇编指令长度
    machine_code_size = dbg.assemble_code_size(asm)
    if machine_code == False:
        dbg.delete_alloc(alloc_address)

    # 读取机器码
    for index in range(0,machine_code_size):
        op = dbg.read_memory_byte(alloc_address + index)
        machine_code_list.append(op)

    # 释放堆空间
    dbg.delete_alloc(alloc_address)
    return machine_code_list

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    for item in ["push eax","mov eax,1","jmp eax","pop eax"]:
        # 转换成列表
        opcode = get_assembly_machine_code(dbg,item)
        #print("得到机器码列表: ",opcode)

        # 列表转换成字符串
        scan_string = " ".join([str(_) for _ in opcode])
        #print("搜索机器码字符串: ", scan_string)

        address = dbg.scan_memory_one(scan_string)
        print("第一个符合条件的内存块: {}".format(hex(address)))

    dbg.close()