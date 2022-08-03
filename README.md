# x64dbg 自动化控制插件

<br>
<div align=center>
  <img width="100" src="https://cdn.lyshark.com/archive/LyScript/bug_black.png"/><tr>
    <img width="100" src="https://cdn.lyshark.com/archive/LyScript/python.png"/>
 <br><br><br>
  
  [简体中文](README.md) | [ENGLISH](README-EN.md) | [русский язык ](README-RU.md)

  <br>
  
[![Build status](https://cdn.lyshark.com/archive/LyScript/build.svg)](https://github.com/lyshark/LyScript) [![Open Source Helpers](https://cdn.lyshark.com/archive/LyScript/users.svg)](https://github.com/lyshark/LyScript) [![Crowdin](https://cdn.lyshark.com/archive/LyScript/email.svg)](mailto:me@lyshark.com) [![Download x64dbg](https://cdn.lyshark.com/archive/LyScript/x64dbg.svg)](https://github.com/lyshark/LyScript/releases/tag/LyScript) [![OSCS Status](https://www.oscs1024.com/platform/badge/lyshark/LyScript.svg?size=small)](https://www.oscs1024.com/project/lyshark/LyScript?ref=badge_small)

[![python3](https://cdn.lyshark.com/archive/LyScript/python3.svg)](https://github.com/lyshark/LyScript) [![platform](https://cdn.lyshark.com/archive/LyScript/platform.svg)](https://github.com/lyshark/LyScript)

<br><br>
一款 x64dbg 自动化控制插件，通过Python控制X64dbg，实现了远程动态调试，解决了逆向工作者分析漏洞，寻找指令片段，原生脚本不够强大的问题，通过与Python相结合利用Python语法的灵活性以及丰富的第三方库，提高分析效率，实现自动化分析代码。
  
</div>
<br>

python包请安装与插件一致的版本，在cmd命令行下执行pip 命令即可安装。

 - 安装标准包：`pip install LyScript32` 或者 `pip install LyScript64`

其次您需要手动下载对应x64dbg版本的驱动文件，并放入指定目录下。

 - 插件下载：<a href="https://cdn.lyshark.com/software/LyScript32.zip">LyScript32 (32位插件)</a> 或者 <a href="https://cdn.lyshark.com/software/LyScript64.zip">LyScript64 (64位插件)</a>

插件下载好以后，请将该插件复制到x64dbg目录下的plugins目录下，程序运行后会自动加载插件文件。

![](https://img2022.cnblogs.com/blog/1379525/202203/1379525-20220327190905044-1815692787.png)

当插件加载成功后，会在日志位置看到具体的绑定信息以及输出调试，该插件并不会在插件栏显示。

![image](https://user-images.githubusercontent.com/52789403/161062658-0452fe0c-3e11-4df4-a83b-b026f74884d0.png)

如果需要远程调试，则只需要在初始化`MyDebug()`类是传入对端IP地址即可，如果不填写参数则默认使用`127.0.0.1`地址，请确保对端放行了`6589`端口，否则无法连接。

![image](https://user-images.githubusercontent.com/52789403/161062393-df04aabb-2d70-4434-80b9-a46974bccf8a.png)

运行x64dbg程序并手动载入需要分析的可执行文件，然后我们可以通过`connect()`方法连接到调试器，连接后会创建一个持久会话直到python脚本结束则连接会被强制断开，在此期间可调用`is_connect()`检查该链接是否还存在，具体代码如下所示。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    # 初始化
    dbg = MyDebug()

    # 连接到调试器
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 检测套接字是否还在
    ref = dbg.is_connect()
    print("是否在连接: ", ref)

    dbg.close()
```
<br><br>

### 寄存器类

**get_register() 函数:** 该函数主要用于实现，对特定寄存器的获取操作，用户需传入需要获取的寄存器名字即可。

 - 参数1：传入寄存器字符串

可用范围："DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", "ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP"

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eax = dbg.get_register("eax")
    ebx = dbg.get_register("ebx")

    print("eax = {}".format(hex(eax)))
    print("ebx = {}".format(hex(ebx)))

    dbg.close()
```
如果您使用的是64位插件，则寄存器的支持范围将变为E系列加R系列。

可用范围扩展： "DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", "ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP", "RAX", "RBX", "RCX", "RDX", "RSI", "SIL", "RDI", "DIL", "RBP", "BPL", "RSP", "SPL", "RIP", "R8", "R8D", "R8W", "R8B", "R9", "R9D", "R9W", "R9B", "R10", "R10D", "R10W", "R10B", "R11", "R11D", "R11W", "R11B", "R12", "R12D", "R12W", "R12B", "R13", "R13D", "R13W", "R13B", "R14", "R14D", "R14W", "R14B", "R15", "R15D", "R15W", "R15B"

```Python
from LyScript64 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    rax = dbg.get_register("rax")
    eax = dbg.get_register("eax")
    ax = dbg.get_register("ax")

    print("rax = {} eax = {} ax ={}".format(hex(rax),hex(eax),hex(ax)))

    r8 = dbg.get_register("r8")
    print("获取R系列寄存器: {}".format(hex(r8)))

    dbg.close()
```

**set_register() 函数:** 该函数实现设置指定寄存器参数，同理64位将支持更多寄存器的参数修改。

 - 参数1：传入寄存器字符串
 - 参数2：十进制数值

可用范围："DR0", "DR1", "DR2", "DR3", "DR6", "DR7", "EAX", "AX", "AH", "AL", "EBX", "BX", "BH", "BL", "ECX", "CX", "CH", "CL", "EDX", "DX", "DH", "DL", "EDI", "DI", "ESI", "SI", "EBP", "BP", "ESP", "SP", "EIP"

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    eax = dbg.get_register("eax")
    
    dbg.set_register("eax",100)

    print("eax = {}".format(hex(eax)))

    dbg.close()
```

**get_flag_register() 函数:** 用于获取某个标志位参数，返回值只有真或者假。

 - 参数1：寄存器字符串

可用寄存器范围："ZF", "OF", "CF", "PF", "SF", "TF", "AF", "DF", "IF" 

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    cf = dbg.get_flag_register("cf")
    print("标志: {}".format(cf))
    
    dbg.close()
```

**set_flag_register() 函数:** 用于设置某个标志位参数，返回值只有真或者假。
 
 - 参数1：寄存器字符串
 - 参数2：[ 设置为真 True] / [设置为假 False]

可用寄存器范围："ZF", "OF", "CF", "PF", "SF", "TF", "AF", "DF", "IF" 

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    zf = dbg.get_flag_register("zf")
    print(zf)

    dbg.set_flag_register("zf",False)

    zf = dbg.get_flag_register("zf")
    print(zf)

    dbg.close()
```
<br>

### 调试类

**set_debug() 函数:** 用于影响调试器，例如前进一次，后退一次，暂停调试，终止等。

 - 参数1: 传入需要执行的动作

可用动作范围：[暂停 Pause] [运行 Run] [步入 StepIn]  [步过 StepOut] [到结束 StepOver] [停止 Stop] [等待 Wait]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    while True:
        dbg.set_debug("StepIn")
        
        eax = dbg.get_register("eax")
        
        if eax == 0:
            print("找到了")
            break
        
    dbg.close()
```

**set_debug_count() 函数:** 该函数是`set_debug()`函数的延续，目的是执行自动步过次数。

 - 参数1：传入需要执行的动作
 - 参数2：执行重复次数

可用动作范围：[暂停 Pause] [运行 Run] [步入 StepIn]  [步过 StepOut] [到结束 StepOver] [停止 Stop] [等待 Wait]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    dbg.set_debug_count("StepIn",10)

    dbg.close()
```

**is_debugger() /is_running() 函数:** is_debugger可用于验证当前调试器是否处于调试状态，is_running则用于验证是否在运行。

- 无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.is_debugger()
    print(ref)

    ref = dbg.is_running()
    print(ref)

    dbg.close()
```

**set_breakpoint() 函数:** 设置断点与取消断点进行了分离，设置断点只需要传入十进制内存地址。

 - 参数1：传入内存地址（十进制）
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    ref = dbg.set_breakpoint(eip)

    print("设置状态: {}".format(ref))
    dbg.close()
```

**delete_breakpoint() 函数:** 该函数传入一个内存地址，可取消一个内存断点。

 - 参数1：传入内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    ref = dbg.set_breakpoint(eip)
    print("设置状态: {}".format(ref))

    del_ref = dbg.delete_breakpoint(eip)
    print("取消状态: {}".format(del_ref))

    dbg.close()
```

**check_breakpoint() 函数:** 用于检查下过的断点是否被命中，命中返回True否则返回False。

 - 参数1：传入内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    ref = dbg.set_breakpoint(eip)
    print("设置状态: {}".format(ref))

    is_check = dbg.check_breakpoint(4134331)
    print("是否命中: {}".format(is_check))

    dbg.close()
```

**get_all_breakpoint() 函数:** 用于获取当前调试程序中，所有下过的断点信息，包括是否开启，命中次数等。

 - 无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    ref = dbg.get_all_breakpoint()
    print(ref)
    dbg.close()
```

**set_hardware_breakpoint() 函数:** 用于设置一个硬件断点，硬件断点在32位系统中最多设置4个。

 - 参数1：内存地址（十进制）
 - 参数2：断点类型

断点类型可用范围：[类型 0 = HardwareAccess / 1 = HardwareWrite / 2 = HardwareExecute]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug(address="127.0.0.1",port=6666)
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")

    ref = dbg.set_hardware_breakpoint(eip,2)
    print(ref)

    dbg.close()
```

**delete_hardware_breakpoint() 函数:** 用于删除一个硬件断点，只需要传入地址即可，无需传入类型。

 - 参数1：内存地址（十进制）

断点类型可用范围：[类型 0 = HardwareAccess / 1 = HardwareWrite / 2 = HardwareExecute]

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug(address="127.0.0.1",port=6666)
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")

    ref = dbg.set_hardware_breakpoint(eip,2)
    print(ref)

    # 删除断点
    ref = dbg.delete_hardware_breakpoint(eip)
    print(ref)

    dbg.close()
```
<br>

### 模块类

**get_module_base() 函数:** 该函数可用于获取程序载入的指定一个模块的基地址。

 - 参数1：模块名字符串

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    
    user32_base = dbg.get_module_base("user32.dll")
    print(user32_base)

    dbg.close()
```

**get_all_module() 函数:** 用于输出当前加载程序的所有模块信息，以字典的形式返回。

 - 参数：无参数

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_all_module()

    for i in ref:
        print(i)

    print(ref[0])
    print(ref[1].get("name"))
    print(ref[1].get("path"))

    dbg.close()
```

**get_local_() 系列函数:** 获取当前EIP所在模块基地址，长度，以及内存属性，此功能无参数传递，获取的是当前EIP所指向模块的数据。

 - dbg.get_local_base()    获取模块基地址
 - dbg.get_local_size()    获取模块长度
 - dbg.get_local_protect() 获取模块保护属性

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_local_base()
    print(hex(ref))

    ref2 = dbg.get_local_size()
    print(hex(ref2))

    ref3 = dbg.get_local_protect()
    print(ref3)

    dbg.close()
```

**get_module_from_function() 函数:** 获取指定模块中指定函数的内存地址，可用于验证当前程序在内存中指定函数的虚拟地址。

 - 参数1：模块名
 - 参数2：函数名

成功返回地址，失败返回false

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_module_from_function("user32.dll","MessageBoxW")
    print(hex(ref))

    ref2 = dbg.get_module_from_function("kernel32.dll","test")
    print(ref2)

    dbg.close()
```

**get_module_from_import() 函数:** 获取当前程序中指定模块的导入表信息，输出为列表嵌套字典。

 - 参数1：传入模块名称

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_module_from_import("ucrtbase.dll")
    print(ref)

    ref1 = dbg.get_module_from_import("win32project1.exe")

    for i in ref1:
        print(i.get("name"))

    dbg.close()
```

**get_module_from_export() 函数:** 该函数用于获取当前加载程序中的导出表信息。

 - 参数1：传入模块名

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_module_from_export("msvcr120d.dll")

    for i in ref:
        print(i.get("name"), hex(i.get("va")))

    dbg.close()
```

**get_section() 函数:** 该函数用于输出主程序中的节表信息。

 - 无参数传递

 ```Python
 from LyScript32 import MyDebug
 
if __name__ == "__main__":
    dbg = MyDebug(address="127.0.0.1",port=6666)
    connect_flag = dbg.connect()

    ref = dbg.get_section()
    print(ref)

    dbg.close()
```

**get_base_from_address() 函数:** 根据传入的内存地址得到该模块首地址。

 - 参数1：传入内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    eip = dbg.get_register("eip")

    ref = dbg.get_base_from_address(eip)
    print("模块首地址: {}".format(hex(ref)))
```

**get_base_from_name() 函数:** 根据传入的模块名得到该模块所在内存首地址。

 - 参数1：传入模块名

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    eip = dbg.get_register("eip")

    ref_base = dbg.get_base_from_name("win32project.exe")
    print("模块首地址: {}".format(hex(ref_base)))

    dbg.close()
```

**get_oep_from_name() 函数:** 根据传入的模块名，获取该模块实际装载OEP位置。

 - 参数1：传入模块名

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    oep = dbg.get_oep_from_name("win32project.exe")
    print(hex(oep))

    dbg.close()
```

**get_oep_from_address() 函数:** 根据传入内存地址，得到该地址模块的OEP位置。

 - 参数1：传入内存地址

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    eip = dbg.get_register("eip")

    oep = dbg.get_oep_from_address(eip)
    print(hex(oep))

    dbg.close()
```
<br>

### 内存类

**read_memory_() 系列函数:** 读内存系列函数，包括 ReadByte,ReadWord,ReadDword 三种格式，在64位下才支持Qword

 - 参数1：需要读取的内存地址（十进制）

目前支持：
 - read_memory_byte() 读字节
 - read_memory_word() 读word
 - read_memory_dword() 读dword
 - read_memory_qword() 读qword （仅支持64位）
 - read_memory_ptr() 读指针

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()


    eip = dbg.get_register("eip")

    ref = dbg.read_memory_byte(eip)
    print(hex(ref))

    ref2 = dbg.read_memory_word(eip)
    print(hex(ref2))

    ref3 = dbg.read_memory_dword(eip)
    print(hex(ref3))

    ref4 = dbg.read_memory_ptr(eip)
    print(hex(ref4))

    dbg.close()
```

**write_memory_() 系列函数:** 写内存系列函数，WriteByte,WriteWord,WriteDWORD,WriteQword

 - 参数1：需要写入的内存
 - 参数2：需要写入的byte字节

目前支持：
 - write_memory_byte() 写字节
 - write_memory_word() 写word
 - write_memory_dword() 写dword
 - write_memory_qword() 写qword （仅支持64位）
 - write_memory_ptr() 写指针

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    addr = dbg.create_alloc(1024)
    print(hex(addr))

    ref = dbg.write_memory_byte(addr,10)

    print(ref)

    dbg.close()
```

**scan_memory_one() 函数:** 实现了内存扫描，当扫描到第一个符合条件的特征时，自动输出。

 - 参数1：特征码字段

 这个函数需要注意，如果我们的x64dbg工具停在系统领空，则会默认搜索系统领空下的特征，如果像搜索程序里面的，需要先将EIP切过去在操作。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    ref = dbg.scan_memory_one("ff 25")
    print(ref)
    dbg.close()
```

**scan_memory_all() 函数:** 实现了扫描所有符合条件的特征字段，找到后返回一个列表。

 - 参数1：特征码字段

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.scan_memory_all("ff 25")

    for index in ref:
        print(hex(index))

    dbg.close()
```

**get_local_protect() 函数:** 获取内存属性传值，该函数进行更新，取消了只能得到EIP所指的位置的内存属性，用户可随意检测。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print(eip)

    ref = dbg.get_local_protect(eip)
    print(ref)
```

**set_local_protect() 函数:** 新增设置内存属性函数，传入eip内存地址，设置属性32，以及设置内存长度1024即可。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    
    eip = dbg.get_register("eip")
    print(eip)

    b = dbg.set_local_protect(eip,32,1024)
    print("设置属性状态: {}".format(b))

    dbg.close()
```

**get_local_page_size() 函数:** 用于获取当前EIP所指领空下，内存pagesize分页大小。

 - 无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    size = dbg.get_local_page_size()
    print("pagesize = {}".format(size))

    dbg.close()
```

**get_memory_section() 函数:** 该函数主要用于获取内存映像中，当前调试程序的内存节表数据。

 - 无参数传递
 
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_memory_section()
    print(ref)
    dbg.close()
```
<br>

### 堆栈类

**create_alloc() 函数：** 函数`CreateRemoteAlloc()`可在远程开辟一段堆空间，成功返回内存首地址。

 - 参数1：开辟的堆长度（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.create_alloc(1024)
    print("开辟地址: ", hex(ref))

    dbg.close()
```

**delete_alloc() 函数：** 函数`delete_alloc()`用于注销一个远程堆空间。

 - 参数1：传入需要删除的堆空间内存地址。

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.create_alloc(1024)
    print("开辟地址: ", hex(ref))

    flag = dbg.delete_alloc(ref)
    print("删除状态: ",flag)

    dbg.close()
```

**push_stack() 函数:** 将一个十进制数压入堆栈中，默认在堆栈栈顶。

 - 参数1：十进制数据

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.push_stack(10)

    print(ref)

    dbg.close()
```

**pop_stack() 函数:** pop函数用于从堆栈中推出一个元素，默认从栈顶弹出。

 - 无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    tt = dbg.pop_stack()
    print(tt)

    dbg.close()
```

**peek_stack() 函数:** peek则用于检查堆栈内的参数，可设置偏移值，不设置则默认检查第一个也就是栈顶。

 - 参数1：十进制偏移

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    # 无参数检查
    check = dbg.peek_stack()
    print(check)

    # 携带参数检查
    check_1 = dbg.peek_stack(2)
    print(check_1)

    dbg.close()
```
<br>

### 进程线程类

**get_thread_list() 函数:** 该函数可输出当前进程所有在运行的线程信息。

 - 无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_thread_list()
    print(ref[0])
    print(ref[1])

    dbg.close()
```

**get_process_handle() 函数:** 用于获取当前进程句柄信息。

 - 无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_process_handle()
    print(ref)

    dbg.close()
```

**get_process_id() 函数:** 用于获取当前加载程序的PID

 - 无参数传递

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_process_id()
    print(ref)

    dbg.close()
```

**get_teb_address() / get_peb_address() 系列函数:** 用于获取当前进程环境块，和线程环境快。

 - get_teb_address()  传入参数是线程ID
 - get_peb_address() 传入参数是进程ID

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.get_teb_address(6128)
    print(ref)

    ref = dbg.get_peb_address(9012)
    print(ref)

    dbg.close()
```
<br>

### 反汇编类

**get_disasm_code() 函数:** 该函数主要用于对特定内存地址进行反汇编，传入两个参数。

 - 参数1：需要反汇编的地址(十进制) 
 - 参数2：需要向下反汇编的长度

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 得到EIP位置
    eip = dbg.get_register("eip")

    # 反汇编前100行
    disasm_dict = dbg.get_disasm_code(eip,100)

    for ds in disasm_dict:
        print("地址: {} 反汇编: {}".format(hex(ds.get("addr")),ds.get("opcode")))

    dbg.close()
```

**get_disasm_one_code() 函数:** 在用户指定的位置读入一条汇编指令，用户可根据需要对其进行判断。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print("EIP = {}".format(eip))

    disasm = dbg.get_disasm_one_code(eip)
    print("反汇编一条: {}".format(disasm))

    dbg.close()
```

**get_disasm_operand_code() 函数:** 用于获取汇编指令中的操作数，例如`jmp 0x0401000`其操作数就是`0x0401000`。

 - 参数1：传入内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print("EIP = {}".format(eip))

    opcode = dbg.get_disasm_operand_code(eip)
    print("操作数: {}".format(hex(opcode)))

    dbg.close()
```

**get_disasm_operand_size() 函数:** 用于得当前内存地址下汇编代码的机器码长度。

 - 参数1：传入内存地址（十进制）

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print("EIP = {}".format(eip))

    opcode = dbg.get_disasm_operand_size(eip)

    print("机器码长度: {}".format(hex(opcode)))

    dbg.close()
```

**assemble_write_memory() 函数:** 实现了用户传入一段正确的汇编指令，程序自动将该指令转为机器码，并写入到指定位置。

 - 参数1：写出内存地址（十进制）
 - 参数2：写出汇编指令

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    print(eip)

    ref = dbg.assemble_write_memory(eip,"mov eax,1")
    print("是否写出: {}".format(ref))

    dbg.close()
```

**assemble_code_size() 函数:** 该函数实现了用户传入一个汇编指令，自动计算出该指令占多少个字节。

 - 参数1：汇编指令字符串

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.assemble_code_size("sub esp, 0x324")
    print(ref)

    dbg.close()
```

<br>

### 其他通用类

**set_comment_notes() 函数:** 给指定位置代码增加一段注释，如下演示在eip位置增加注释。

 - 参数1：注释内存地址
 - 参数2：注释内容

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    eip = dbg.get_register("eip")
    ref = dbg.set_comment_notes(eip,"hello lyshark")
    print(ref)

    dbg.close()
```

**run_command_exec() 函数:** 执行内置命令，例如bp,dump等。

 - 参数1：命令语句

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    ref = dbg.run_command_exec("bp MessageBoxA")
    print(ref)

    dbg.close()
```

**set_loger_output() 函数:** 日志的输出尤为重要，该模块提供了自定义日志输出功能，可将指定日志输出到x64dbg日志位置。

 - 参数1：日志内容

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()

    for i in range(0,100):
        ref = dbg.set_loger_output("hello lyshark -> {} \n".format(i))
        print(ref)

    dbg.close()
```
<br>

### 扩展Script模块

LyScriptTools模块是一个x64dbg的扩展包，该模块主要针对内置Script脚本命令的类版封装，使得用户可以方便的调用x64dbg中的内置脚本命令，该封装原理是利用了LyScript模块中的`run_command_exec()`命令实现的，如下所有的命令封装都是围绕这个API函数进行的。

该插件需要在安装有`LyScript32/64`包之上再安装一个`LyScriptTools32/64`扩展包，该包已经提交到pypi官方仓库。

 - 安装只需要执行 `pip install LyScriptTools32` 或者 `pip install LyScriptTools64`

<br>

<b>通用函数功能参考自：</b><a href="https://www.cnblogs.com/iBinary/p/16359195.html">iBinary</a>

<br>

插件目前分为四部分，其中`LyScriptModule`是针对模块操作的封装，`LyScriptMemory`是内存封装，`LyScriptDisassemble`是反汇编封装，`LyScriptOther`是一些杂类。

<b>from LyScriptTools32 import LyScriptModule</b>

 - mod.party(addr) ---> 获取模块的模式编号, addr = 0则是用户模块,1则是系统模块
 - mod.base(addr)  --->  获取模块基址
 - mod.size(addr)  --->  返回模块大小
 - mod.hash(addr)  --->  返回模块hash
 - mod.entry(addr) --->  返回模块入口
 - mod.system(addr)--->  如果addr是系统模块则为true否则则是false
 - mod.user(addr)  --->  如果是用户模块则返回true 否则为false
 - mod.main()      --->  返回主模块基地址
 - mod.rva(addr)   --->  如果addr不在模块则返回0,否则返回 addr所位于模块的 RVA偏移
 - mod.offset(addr)--->  获取地址所对应的文件偏移量,如果不在模块则返回0
 - mod.isexport(addr) ---> 判断该地址是否是从模块导出的函数,true是 false则不是

<b>from LyScriptTools32 import LyScriptMemory</b>

 - mem.valid(addr) 判断addr是否有效,有效则返回True
 - mem.base(addr)  或者当前addr的基址
 - mem.size(addr)  获取当前addr内存的大小
 - mem.iscode(addr) 判断当前 addr是否是可执行页面,成功返回TRUE
 - mem.decodepointer(ptr) 解密指针,相当于调用了API. DecodePointer ptr
 - ReadByte(addr / reg); 从addr或者寄存器中读取一个字节内存并且返回
 - Byte(addr) byte(addr)  同上
 - ReadWord(addr)  Word(addr) word(addr) 同上 读取两个字节
 - ReadDDword(addr) Dword(addr) dword(addr) 同上 读取四个字节
 - ReadQword(addr) Qword(addr) qword(addr) 同上 读取8个字节,但是只能是64位程序方可使用
 - ReadPtr(addr) 从地址中读取指针(4/8字节)并返回读取的指针值
 - ReadPointer(addr) ptr(addr) Pointer(addr) pointer(addr) 都同上
 - ptr(mod.main()) --> 00905A4D
 - byte(mod.main()) --> 0x0000004D

<b>from LyScriptTools32 import LyScriptDisassemble</b>

 - dis.len(addr)      获取addr处的指令长度。
 - dis.iscond(addr)   判断当前addr位置是否是条件指令(比如jxx) 返回值: 是的话True 否则False
 - dis.isbranch(addr) 判断当前地址是否是分支指令   返回值: 同上
 - dis.isret(addr)    判断是否是ret指令          返回值: 同上  
 - dis.iscall(addr)   判断是否是call指令         返回值: 同上  
 - dis.ismem(addr)    判断是否是内存操作数        返回值: 同上
 - dis.isnop(addr)    判断是否是nop             返回值: 同上
 - dis.isunusual(addr)判断当前地址是否指示为异常地址 返回值: 同上
 - dis.branchdest(addr)：将指令的分支目标位于（如果按 Enter 键，它将遵循什么）。addr
 - dis.branchexec(addr)：如果 分支 at 要执行，则为 true。addr
 - dis.imm(addr)       获取当前指令位置的立即数(这一行指令中出现的立即数)
 - dis.brtrue(addr)：指令在 的分支目标。addr
 - dis.brfalse(addr)：下一条指令的地址（如果指令 at 是条件分支）。addr
 - dis.next(addr)：    获取addr的下一条地址
 - dis.prev(addr)：    获取addr上一条低地址
 - dis.iscallsystem(addr) 判断当前指令是否是系统模块指令

<b>from LyScriptTools32 import LyScriptOther</b>

 - arg.get(index); 获取当前函数堆栈中的第几个参数,假设返回地址在堆栈上,并且我们在函数内部.
 - arg.set(index,value);设置的索引位置的值为
 - ex.firstchance()：最后一个异常是否为第一次机会异常。
 - ex.addr()：最后一个异常地址。例如，导致异常的指令的地址。
 - ex.code()：最后一个异常代码。
 - ex.flags()：最后一个异常标志。
 - ex.infocount()：上次异常信息计数（参数数）。
 - ex.info(index)：最后一个异常信息，如果索引超出范围，则为零。

如上是一些常用的函数封装，他们的调用方式如下面所示。
```Python
from LyScript32 import MyDebug
from LyScriptTools32 import LyScriptModule
from LyScriptTools32 import LyScriptMemory
from LyScriptTools32 import LyScriptDisassemble
from LyScriptTools32 import LyScriptOther

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 模块类
    mod = LyScriptModule()

    party = mod.base(dbg,"0x4c55ac")
    print("party: {}".format(hex(party)))

    # 读取参数时应注意转为十六进制
    eip = dbg.get_register("eip")
    ret = mod.base(dbg, "{}".format(hex(eip)))
    print("基地址: {}".format(hex(ret)))
    
    dbg.close()
```

当然如果你觉得上面这些通用函数不够用，或者没有补充全面，你完全可以调用任意类内的`ot.GetScriptValue()`函数自己去封装实现。

<br><br>

### 通用API例程 (官方案例)

LyScript 模块中的通用案例，用于演示插件内置方法如何组合使用，用户可以自行研究学习API函数是如何灵活的调用的，并自己编写一些有用的案例。

**PEFile 载入内存格式:** 案例演示，如何将一个可执行文件中的内存数据通过PEfile模块打开。
```Python
from LyScript32 import MyDebug
import pefile

if __name__ == "__main__":
    # 初始化
    dbg = MyDebug()
    dbg.connect()

    # 得到text节基地址
    local_base = dbg.get_local_base()

    # 根据text节得到程序首地址
    base = dbg.get_base_from_address(local_base)

    byte_array = bytearray()
    for index in range(0,4096):
        read_byte = dbg.read_memory_byte(base + index)
        byte_array.append(read_byte)

    oPE = pefile.PE(data = byte_array)
    timedate = oPE.OPTIONAL_HEADER.dump_dict()
    print(timedate)
```
如下通过`LyScirpt`模块配合`PEFile`模块解析内存镜像中的`section`节表属性。
```Python
from LyScript32 import MyDebug
import pefile

if __name__ == "__main__":
    # 初始化
    dbg = MyDebug()
    dbg.connect()

    # 得到text节基地址
    local_base = dbg.get_local_base()

    # 根据text节得到程序首地址
    base = dbg.get_base_from_address(local_base)

    byte_array = bytearray()
    for index in range(0,8192):
        read_byte = dbg.read_memory_byte(base + index)
        byte_array.append(read_byte)

    oPE = pefile.PE(data = byte_array)

    for section in oPE.sections:
        print("%10s %10x %10x %10x" %(section.Name.decode("utf-8"), section.VirtualAddress, section.Misc_VirtualSize, section.SizeOfRawData))
    dbg.close()
```

**验证PE程序启用的保护方式:** 验证保护方式需要通过`dbg.get_all_module()`遍历加载过的模块，并依次读入`DllCharacteristics`与操作数进行与运算得到保护方式。
```Python
from LyScript32 import MyDebug
import pefile

if __name__ == "__main__":
    # 初始化
    dbg = MyDebug()
    dbg.connect()

    # 得到所有加载过的模块
    module_list = dbg.get_all_module()

    print("-" * 100)
    print("模块名 \t\t\t 基址随机化 \t\t DEP保护 \t\t 强制完整性 \t\t SEH异常保护 \t\t")
    print("-" * 100)

    for module_index in module_list:
        print("{:15}\t\t".format(module_index.get("name")),end="")

        # 依次读入程序所载入的模块
        byte_array = bytearray()
        for index in range(0, 4096):
            read_byte = dbg.read_memory_byte(module_index.get("base") + index)
            byte_array.append(read_byte)

        oPE = pefile.PE(data=byte_array)

        # 随机基址 => hex(pe.OPTIONAL_HEADER.DllCharacteristics) & 0x40 == 0x40
        if ((oPE.OPTIONAL_HEADER.DllCharacteristics & 64) == 64):
            print("True\t\t\t",end="")
        else:
            print("False\t\t\t",end="")
        # 数据不可执行 DEP => hex(pe.OPTIONAL_HEADER.DllCharacteristics) & 0x100 == 0x100
        if ((oPE.OPTIONAL_HEADER.DllCharacteristics & 256) == 256):
            print("True\t\t\t",end="")
        else:
            print("False\t\t\t",end="")
        # 强制完整性=> hex(pe.OPTIONAL_HEADER.DllCharacteristics) & 0x80 == 0x80
        if ((oPE.OPTIONAL_HEADER.DllCharacteristics & 128) == 128):
            print("True\t\t\t",end="")
        else:
            print("False\t\t\t",end="")
        if ((oPE.OPTIONAL_HEADER.DllCharacteristics & 1024) == 1024):
            print("True\t\t\t",end="")
        else:
            print("False\t\t\t",end="")
        print()
    dbg.close()
```

**全模块特征匹配:** 针对所有模块中的特征码模糊匹配，找到会返回内存地址。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    for entry in dbg.get_all_module():
        eip = entry.get("entry")

        if eip != 0:
            dbg.set_register("eip",eip)

            search = dbg.scan_memory_one("ff 25 ??")
            print(hex(search))

    dbg.close()
```

**搜索汇编特征:** 使用python实现方法，通过特定方法扫描内存范围，如果出现我们所需要的指令集序列，则输出该指令的具体内存地址。
```Python
from LyScript32 import MyDebug

# 检索指定序列中是否存在一段特定的指令集
def SearchOpCode(OpCodeList,SearchCode,ReadByte):
            pass

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 得到EIP位置
    eip = dbg.get_register("eip")

    # 反汇编前1000行
    disasm_dict = dbg.get_disasm_code(eip,1000)

    # 搜索一个指令序列,用于快速查找构建漏洞利用代码
    SearchCode = [
        ["push 0xC0000409", "call 0x003F1B38", "pop ecx"],
        ["mov ebp, esp", "sub esp, 0x324"]
    ]

    # 检索内存指令集
    for item in range(0,len(SearchCode)):
        Search = SearchCode[item]
        # disasm_dict = 返回汇编指令 Search = 寻找指令集 1000 = 向下检索长度
        ret = SearchOpCode(disasm_dict,Search,1000)
        if ret != None:
            print("指令集: {} --> 首次出现地址: {}".format(SearchCode[item],hex(ret)))

    dbg.close()
```

**得到汇编指令机器码:** 该功能主要实现，得到用户传入汇编指令所对应的机器码，这段代码你可以这样来实现。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    addr = dbg.create_alloc(1024)

    print("堆空间: {}".format(hex(addr)))

    asm_size = dbg.assemble_code_size("mov eax,1")
    print("汇编代码占用字节: {}".format(asm_size))

    write = dbg.assemble_write_memory(addr,"mov eax,1")

    byte_code = bytearray()

    for index in range(0,asm_size):
        read = dbg.read_memory_byte(addr + index)
        print("{:02x} ".format(read),end="")

    dbg.delete_alloc(addr)
```
封装上方代码，你就可以实现一个汇编指令获取工具了，如下`get_opcode_from_assemble()`函数。
```Python
from LyScript32 import MyDebug

# 传入汇编代码,得到对应机器码
def get_opcode_from_assemble(dbg_ptr,asm):
              pass

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 获取汇编代码
    byte_array = get_opcode_from_assemble(dbg,"xor eax,eax")
    for index in byte_array:
        print(hex(index),end="")
    print()

    # 汇编一个序列
    asm_list = ["xor eax,eax", "xor ebx,ebx", "mov eax,1"]
    for index in asm_list:
        byte_array = get_opcode_from_assemble(dbg, index)
        for index in byte_array:
            print(hex(index),end="")
        print()

    dbg.close()
```

**实现劫持EIP指针:** 这里我们演示一个案例，你可以自己实现一个`write_opcode_from_assemble()`函数批量将列表中的指令集写出到内存。
```Python
from LyScript32 import MyDebug

# 传入汇编指令列表,直接将机器码写入对端内存
def write_opcode_from_assemble(dbg_ptr,asm_list):
              pass

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 写出指令集到内存
    asm_list = ['mov eax,1','mov ebx,2','add eax,ebx']
    write_addr = write_opcode_from_assemble(dbg,asm_list)
    print("写出地址: {}".format(hex(write_addr)))

    # 设置执行属性
    dbg.set_local_protect(write_addr,32,1024)

    # 将EIP设置到指令集位置
    dbg.set_register("eip",write_addr)

    dbg.close()
```
如何执行函数呢？很简单，看以下代码是如何实现的，相信你能看懂，运行后会看到一个错误弹窗，说明程序执行流已经被转向了。
```Python
from LyScript32 import MyDebug

# 传入汇编指令列表,直接将机器码写入对端内存
def write_opcode_from_assemble(dbg_ptr,asm_list):
              pass

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 得到messagebox内存地址
    msg_ptr = dbg.get_module_from_function("user32.dll","MessageBoxA")
    call = "call {}".format(str(hex(msg_ptr)))
    print("函数地址: {}".format(call))

    # 写出指令集到内存
    asm_list = ['push 0','push 0','push 0','push 0',call]
    write_addr = write_opcode_from_assemble(dbg,asm_list)
    print("写出地址: {}".format(hex(write_addr)))

    # 设置执行属性
    dbg.set_local_protect(write_addr,32,1024)

    # 将EIP设置到指令集位置
    dbg.set_register("eip",write_addr)

    # 执行代码
    dbg.set_debug("Run")

    dbg.close()
```

**内存字节变更后回写:** 封装字节函数`write_opcode_list()`传入内存地址，对该地址中的字节更改后再回写到原来的位置。

 - 加密算法在内存中会通过S盒展开解密，有时需要特殊需求，捕捉解密后的S-box写入内存，或对矩阵进行特殊处理后替换，这样写即可实现。

```Python
from LyScript32 import MyDebug

# 对每一个字节如何处理
def write_func(x):
    x = x + 10
    return x

# 对指定内存地址机器码进行相应处理
def write_opcode_list(dbg_ptr, address, count, function_ptr):
    for index in range(0, count):
        read = dbg_ptr.read_memory_byte(address + index)

        ref = function_ptr(read)
        print("处理后结果: {}".format(ref))

        dbg.write_memory_byte(address + index, ref)
    return True

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 得到EIP
    eip = dbg.get_register("eip")

    # 对指定内存中的数据+10后写回去
    write_opcode_list(dbg,eip,100,write_func)

    dbg.close()
```

**将ShellCode从文本中注入到内存:** 从文本中读取`ShellCode`代码，将该代码注入到目标进程的堆中，并把当前内存属性设置为可执行。
```Python
from LyScript32 import MyDebug

# 将shellcode读入内存
def read_shellcode(path):
    shellcode_list = []
    with open(path,"r",encoding="utf-8") as fp:
        for index in fp.readlines():
            shellcode_line = index.replace('"',"").replace(" ","").replace("\n","").replace(";","")
            for code in shellcode_line.split("\\x"):
                if code != "" and code != "\\n":
                    shellcode_list.append("0x" + code)
    return shellcode_list

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 开辟堆空间
    address = dbg.create_alloc(1024)
    print("开辟堆空间: {}".format(hex(address)))
    if address == False:
        exit()

    # 设置内存可执行属性
    dbg.set_local_protect(address,32,1024)

    # 从文本中读取shellcode
    shellcode = read_shellcode("d://shellcode.txt")

    # 循环写入到内存
    for code_byte in range(0,len(shellcode)):
        bytef = int(shellcode[code_byte],16)
        dbg.write_memory_byte(code_byte + address, bytef)

    # 设置EIP位置
    dbg.set_register("eip",address)

    input()
    dbg.delete_alloc(address)

    dbg.close()
```
如果把这个过程反过来，就是将特定位置的汇编代码保存到本地。
```Python
from LyScript32 import MyDebug

# 将特定内存保存到文本中
def write_shellcode(dbg,address,size,path):
    with open(path,"a+",encoding="utf-8") as fp:
        for index in range(0, size - 1):
            # 读取机器码
            read_code = dbg.read_memory_byte(address + index)

            if (index+1) % 16 == 0:
                print("\\x" + str(read_code))
                fp.write("\\x" + str(read_code) + "\n")
            else:
                print("\\x" + str(read_code),end="")
                fp.write("\\x" + str(read_code))

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")
    write_shellcode(dbg,eip,128,"d://lyshark.txt")
    dbg.close()
```

**指令集探针快速检索:** 快速检索当前程序中所有模块中是否存在特定的指令集片段，存在则返回内存地址。
```Python
from LyScript32 import MyDebug

# 将bytearray转为字符串
def get_string(byte_array):
    ref_string = str()
    for index in byte_array:
        ref_string = ref_string + "".join(str(index))
    return ref_string

# 传入汇编代码,得到对应机器码
def get_opcode_from_assemble(dbg_ptr,asm):
  pass

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 需要搜索的指令集片段
    search_asm = ['pop ecx','mov edi,edi', 'push eax', 'jmp esp']
    opcode = []

    # 将汇编指令转为机器码,放入opcode
    for index in range(len(search_asm)):
        byt = bytearray()
        byt = get_opcode_from_assemble(dbg, search_asm[index])
        opcode.append(get_string(byt))

    # 循环搜索指令集内存地址
    for index,entry in zip(range(0,len(opcode)), dbg.get_all_module()):
        eip = entry.get("entry")
        base_name = entry.get("name")
        if eip != 0:
            dbg.set_register("eip",eip)
            search_address = dbg.scan_memory_all(opcode[index])

            if search_address != False:
                print("指令: {} --> 模块: {} --> 个数: {}".format(search_asm[index],base_name,len(search_address)))

                for search_index in search_address:
                    print("[*] {}".format(hex(search_index)))
            else:
                print("a")

        time.sleep(0.3)
    dbg.close()
 ```
 
 **使用内置脚本得到返回值:** 使用内置`run_command_exec()`函数时，用户只能得到内置脚本执行后的状态值，如果想要得到内置命令的返回值则你可以这样写。
 ```Python
 from LyScript32 import MyDebug
 
 dbg = MyDebug()
 conn = dbg.connect()
 
 # 首先定义一个脚本变量
 ref = dbg.run_command_exec("$addr=1024")
 
 # 将脚本返回值放到eax寄存器，或者开辟一个堆放到堆里
 dbg.run_command_exec("eax=$addr")
 
 # 最后拿到寄存器的值
 hex(dbg.get_register("eax"))
 ```
通过中转的方式，可以很好的得到内置脚本的返回值，如下我将其封装成了一个独立的方法。
```Python
from LyScript32 import MyDebug

# 得到脚本返回值
def GetScriptValue(dbg,script):
    try:
        ref = dbg.run_command_exec("push eax")
        if ref != True:
            return None
        ref = dbg.run_command_exec(f"eax={script}")
        if ref != True:
            return None
        reg = dbg.get_register("eax")
        ref = dbg.run_command_exec("pop eax")
        if ref != True:
            return None
        return reg
    except Exception:
        return None
    return None

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eax = "401000"
    ref = GetScriptValue(dbg,"mod.base({})".format(eax))
    print(hex(ref))
    
    dbg.close()
```

**批量载入移除被调试进程:** 默认的LyScript插件没有批量载入功能，导致用户只能手动将被调试进程拖入到x64dbg中才可以调试，使用python模拟快捷键即可解决这个问题。
```Python
import win32api
import win32gui, win32con
import win32clipboard
import re
import time
from LyScript32 import MyDebug

class cWindow:
    def __init__(self):
        self._hwnd = None

    def SetAsForegroundWindow(self):
        win32gui.SetForegroundWindow(self._hwnd)

    def Maximize(self):
        # 最大化
        win32gui.ShowWindow(self._hwnd, win32con.SW_MAXIMIZE)

    def _window_enum_callback(self, hwnd, regex):
        if self._hwnd is None and re.match(regex, str(win32gui.GetWindowText(hwnd))) is not None:
            self._hwnd = hwnd

    def find_window_regex(self, regex):
        self._hwnd = None
        win32gui.EnumWindows(self._window_enum_callback, regex)

    def hide_always_on_top_windows(self):
        win32gui.EnumWindows(self._window_enum_callback_hide, None)

    def _window_enum_callback_hide(self, hwnd, unused):
        if hwnd != self._hwnd:
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & win32con.WS_EX_TOPMOST:
                className = win32gui.GetClassName(hwnd)
                if not (className == 'Button' or className == 'Shell_TrayWnd'):
                    win32gui.ShowWindow(hwnd, win32con.SW_FORCEMINIMIZE)

    def OpenFile(self,path):
        # 按下F3
        win32api.keybd_event(0x72, 0, 0, 0)
        win32api.keybd_event(0x72, 0, win32con.KEYEVENTF_KEYUP, 0)

        # 打开剪贴板
        win32clipboard.OpenClipboard()
        # 清空剪贴板
        win32clipboard.EmptyClipboard()
        # 设置剪贴板内容
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, path)
        # 获取剪贴板内容
        date = win32clipboard.GetClipboardData()
        print("[*] OpenFile = {}".format(date))
        # 关闭剪贴板
        win32clipboard.CloseClipboard()
        time.sleep(0.2)

        # 按下ctrl+v
        win32api.keybd_event(0x11, 0, 0, 0)
        win32api.keybd_event(0x56, 0, 0, 0)
        win32api.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)

        # 按下回车
        win32api.keybd_event(0x0D, 0, 0, 0)
        win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)

    def deatch(self):
        # 按下Ctrl+Alt+F2
        win32api.keybd_event(0x11, 0, 0, 0)
        win32api.keybd_event(0x12, 0, 0, 0)
        win32api.keybd_event(0x71, 0, 0, 0)
        win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x12, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x71, 0, win32con.KEYEVENTF_KEYUP, 0)

# 打开调试程序
def OpenFile(path):
    regex = ".*x32dbg.*"
    cWindows = cWindow()
    cWindows.find_window_regex(regex)
    cWindows.SetAsForegroundWindow()
    cWindows.SetAsForegroundWindow()
    cWindows.OpenFile(path)

# 关闭调试程序
def DeatchFile():
    regex = ".*x32dbg.*"
    cWindows = cWindow()
    cWindows.find_window_regex(regex)
    cWindows.SetAsForegroundWindow()
    cWindows.SetAsForegroundWindow()
    cWindows.deatch()

# 得到脚本返回值
def GetScriptValue(dbg,script):
    try:
        ref = dbg.run_command_exec("push eax")
        if ref != True:
            return None
        ref = dbg.run_command_exec(f"eax={script}")
        if ref != True:
            return None
        reg = dbg.get_register("eax")
        ref = dbg.run_command_exec("pop eax")
        if ref != True:
            return None
        return reg
    except Exception:
        return None
    return None

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    # 批量打开一个列表
    for item in ["D:\Win32Project.exe","D:\Windows Tools\C32ASM\c32asm.exe"]:
        OpenFile(item)
        time.sleep(3)

        for i in range(1,100):
            dbg.set_debug("StepIn")
            time.sleep(0.2)

        eip = dbg.get_register("eip")
        print("eip = > {}".format(hex(eip)))

        time.sleep(3)
        DeatchFile()
```

**获取节表内存属性:** 默认情况下插件可以得到当前节表，但无法直接取到节表内存属性，如果需要得到某个节的内存属性，可以这样写。

节表属性是一个数字，数字含义如下:
 - ER 执行/读取 32
 - E 执行 30
 - R 读取 2
 - W 写入 2
 - C 未知 4
 - N 空属性 1

```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    conn = dbg.connect()

    section = dbg.get_section()
    for i in section:
        section_address = hex(i.get("addr"))
        section_name = i.get("name")
        section_size = i.get("size")
        section_type = dbg.get_local_protect(i.get("addr"))
        print(f"地址: {section_address} -> 名字: {section_name} -> 大小: {section_size}bytes -> ",end="")

        if(section_type == 32):
            print("属性: 执行/读取")
        elif(section_type == 30):
            print("属性: 执行")
        elif(section_type == 2):
            print("属性: 只读")
        elif(section_type == 4):
            print("属性: 读写")
        elif(section_type == 1):
            print("属性: 空属性")
        else:
            print("属性: 读/写/控制")

    dbg.close()
    pass
```

**封装获取反汇编代码:** 反汇编时可以使用`get_disasm_code()`函数，但如果想要自己实现可以这样写。
```Python
from LyScript32 import MyDebug

if __name__ == "__main__":
    dbg = MyDebug()
    conn = dbg.connect()

    # 获取当前EIP地址
    eip = dbg.get_register("eip")
    print("eip = {}".format(hex(eip)))

    # 向下反汇编字节数
    count = eip + 15
    while True:
        # 每次得到一条反汇编指令
        dissasm = dbg.get_disasm_one_code(eip)

        print("0x{:08x} | {}".format(eip, dissasm))

        # 判断是否满足退出条件
        if eip >= count:
            break
        else:
            # 得到本条反汇编代码的长度
            dis_size = dbg.assemble_code_size(dissasm)
            eip = eip + dis_size

    dbg.close()
    pass
```

**得到当前EIP机器码:** 获取到当前EIP指针所在位置的机器码，你可以灵活运用反汇编代码的组合实现。
```Python
from LyScript32 import MyDebug

# 得到机器码
def GetHexCode(dbg,address):
    ref_bytes = []
    # 首先得到反汇编指令,然后得到该指令的长度
    asm_len = dbg.assemble_code_size( dbg.get_disasm_one_code(address) )

    # 循环得到每个机器码
    for index in range(0,asm_len):
        ref_bytes.append(dbg.read_memory_byte(address))
        address = address + 1
    return ref_bytes

if __name__ == "__main__":
    dbg = MyDebug()
    conn = dbg.connect()

    # 获取当前EIP地址
    eip = dbg.get_register("eip")
    print("eip = {}".format(hex(eip)))

    # 得到机器码
    ref = GetHexCode(dbg,eip)
    for i in range(0,len(ref)):
        print("0x{:02x} ".format(ref[i]),end="")

    dbg.close()
    pass
```
如果将如上的两个方法结合起来，那么基本上就实现了获取反汇编窗口中的所有内容。
```Python
from LyScript32 import MyDebug

# 得到机器码
def GetHexCode(dbg,address):
    ref_bytes = []
    # 首先得到反汇编指令,然后得到该指令的长度
    asm_len = dbg.assemble_code_size( dbg.get_disasm_one_code(address) )
    # 循环得到每个机器码
    for index in range(0,asm_len):
        ref_bytes.append(dbg.read_memory_byte(address))
        address = address + 1
    return ref_bytes

if __name__ == "__main__":
    dbg = MyDebug()
    conn = dbg.connect()

    # 获取当前EIP地址
    eip = dbg.get_register("eip")
    print("eip = {}".format(hex(eip)))

    # 向下反汇编字节数
    count = eip + 20
    while True:
        # 每次得到一条反汇编指令
        dissasm = dbg.get_disasm_one_code(eip)

        print("0x{:08x} | {:50} | ".format(eip, dissasm),end="")

        # 得到机器码
        ref = GetHexCode(dbg, eip)
        for i in range(0, len(ref)):
            print("0x{:02x} ".format(ref[i]), end="")
        print()

        # 判断是否满足退出条件
        if eip >= count:
            break
        else:
            # 得到本条反汇编代码的长度
            dis_size = dbg.assemble_code_size(dissasm)
            eip = eip + dis_size

    dbg.close()
    pass
```

**封装汇编指令提取器:** 当用户传入指定汇编指令的时候，自动的将其转换成对应的机器码，代码很简单，首先`dbg.create_alloc(1024)`在进程内存中开辟堆空间，用于存放我们的机器码，然后调用`dbg.assemble_write_memory(alloc_address,"sub esp,10")`将一条汇编指令变成机器码写到对端内存，然后再`op = dbg.read_memory_byte(alloc_address + index)`依次将其读取出来即可。

```Python
from LyScript32 import MyDebug

# 传入汇编指令,获取该指令的机器码
def get_assembly_machine_code(dbg,asm):
    pass

if __name__ == "__main__":
    dbg = MyDebug()
    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    machine_code_list = []

    # 开辟堆空间
    alloc_address = dbg.create_alloc(1024)
    print("分配堆: {}".format(hex(alloc_address)))

    # 得到汇编机器码
    machine_code = dbg.assemble_write_memory(alloc_address,"sub esp,10")
    if machine_code == False:
        dbg.delete_alloc(alloc_address)

    # 得到汇编指令长度
    machine_code_size = dbg.assemble_code_size("sub esp,10")
    if machine_code == False:
        dbg.delete_alloc(alloc_address)

    # 读取机器码
    for index in range(0,machine_code_size):
        op = dbg.read_memory_byte(alloc_address + index)
        machine_code_list.append(op)

    # 释放堆空间
    dbg.delete_alloc(alloc_address)

    # 输出机器码
    print(machine_code_list)
    dbg.close()
```
我们继续封装如上方法，封装成一个可以直接使用的`get_assembly_machine_code`函数。
```Python
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

    # 转换第一对
    opcode = get_assembly_machine_code(dbg,"mov eax,1")
    for index in opcode:
        print("0x{:02X} ".format(index),end="")
    print()

    # 转换第二对
    opcode = get_assembly_machine_code(dbg,"sub esp,10")
    for index in opcode:
        print("0x{:02X} ".format(index),end="")
    print()

    dbg.close()
```

**扫描符合条件的内存:** 通过使用上方封装的`get_assembly_machine_code()`并配合`scan_memory_one(scan_string)`函数，在对端内存搜索是否存在符合条件的指令。
```Python
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
```

**获取下一条汇编指令:** 下一条汇编指令的获取需要注意如果是被命中的指令则此处应该是CC断点占用一个字节，如果不是则正常获取到当前指令即可。

- 1.我们需要检查当前内存断点是否被命中，如果没有命中则说明此处我们需要获取到原始的汇编指令长度，然后与当前eip地址相加获得。
- 2.如果命中了断点，则此处有两种情况
  - 1.1 如果是用户下的断点，则此处调试器会在指令位置替换为CC，也就是汇编中的init停机指令，该指令占用1个字节，需要eip+1得到。
  - 1.2 如果是系统断点，EIP所停留的位置，则我们需要正常获取当前指令地址，此处调试器没有改动汇编指令仅仅只下下了异常断点。

```Python
from LyScript32 import MyDebug

# 获取当前EIP指令的下一条指令
def get_disasm_next(dbg,eip):
    next = 0

    # 检查当前内存地址是否被下了绊子
    check_breakpoint = dbg.check_breakpoint(eip)

    # 说明存在断点，如果存在则这里就是一个字节了
    if check_breakpoint == True:

        # 接着判断当前是否是EIP，如果是EIP则需要使用原来的字节
        local_eip = dbg.get_register("eip")

        # 说明是EIP并且命中了断点
        if local_eip == eip:
            dis_size = dbg.get_disasm_operand_size(eip)
            next = eip + dis_size
            next_asm = dbg.get_disasm_one_code(next)
            return next_asm
        else:
            next = eip + 1
            next_asm = dbg.get_disasm_one_code(next)
            return next_asm
        return None

    # 不是则需要获取到原始汇编代码的长度
    elif check_breakpoint == False:
        # 得到当前指令长度
        dis_size = dbg.get_disasm_operand_size(eip)
        next = eip + dis_size
        next_asm = dbg.get_disasm_one_code(next)
        return next_asm
    else:
        return None

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    next = get_disasm_next(dbg,eip)
    print("下一条指令: {}".format(next))

    prev = get_disasm_next(dbg,12391436)
    print("下一条指令: {}".format(prev))

    dbg.close()
```

**获取上一条汇编指令:** 上一条指令的获取难点就在于，我们无法确定当前指令的上一条指令到底有多长，所以只能用笨办法，逐行扫描对比汇编指令，如果找到则取出其上一条指令即可。
```Python
from LyScript32 import MyDebug

# 获取当前EIP指令的上一条指令
def get_disasm_prev(dbg,eip):
    prev_dasm = None
    # 得到当前汇编指令
    local_disasm = dbg.get_disasm_one_code(eip)

    # 只能向上扫描10行
    eip = eip - 10
    disasm = dbg.get_disasm_code(eip,10)

    # 循环扫描汇编代码
    for index in range(0,len(disasm)):
        # 如果找到了,就取出他的上一个汇编代码
        if disasm[index].get("opcode") == local_disasm:
            prev_dasm = disasm[index-1].get("opcode")
            break

    return prev_dasm

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    next = get_disasm_prev(dbg,eip)
    print("上一条指令: {}".format(next))

    dbg.close()
```

**判断是否为特定指令:** 判断当前传入的内存地址处的汇编指令集，看是否是`call,nop,jmp,ret`指令，如果是返回True否则返回False。
```Python
from LyScript32 import MyDebug

# 是否是跳转指令
def is_call(dbg,address):
    try:
        dis = dbg.get_disasm_one_code(address)
        if dis != False or dis != None:
            if dis.split(" ")[0].replace(" ","") == "call":
                return True
            return False
        return False
    except Exception:
        return False
    return False

# 是否是jmp
def is_jmp(dbg,address):
    try:
        dis = dbg.get_disasm_one_code(address)
        if dis != False or dis != None:
            if dis.split(" ")[0].replace(" ","") == "jmp":
                return True
            return False
        return False
    except Exception:
        return False
    return False

# 是否是ret
def is_ret(dbg,address):
    try:
        dis = dbg.get_disasm_one_code(address)
        if dis != False or dis != None:
            if dis.split(" ")[0].replace(" ","") == "ret":
                return True
            return False
        return False
    except Exception:
        return False
    return False

# 是否是nop
def is_nop(dbg,address):
    try:
        dis = dbg.get_disasm_one_code(address)
        if dis != False or dis != None:
            if dis.split(" ")[0].replace(" ","") == "nop":
                return True
            return False
        return False
    except Exception:
        return False
    return False

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    call = is_call(dbg, eip)
    print("是否是Call指令: {}".format(call))
    dbg.close()
````
同如上所示，我们也可以验证指令集是否是条件跳转命令，验证方式只需要稍微改动代码即可。
```Python
from LyScript32 import MyDebug

# 是否是条件跳转指令
def is_cond(dbg,address):
    try:
        dis = dbg.get_disasm_one_code(address)
        if dis != False or dis != None:

            if dis.split(" ")[0].replace(" ","") in ["je","jne","jz","jnz","ja","jna","jp","jnp","jb","jnb","jg","jng","jge","jl","jle"]:
                return True
            return False
        return False
    except Exception:
        return False
    return False

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    call = is_cond(dbg, eip)
    print("是否是条件跳转指令: {}".format(call))
    dbg.close()
```

**内存区域交换与差异对比:** 内存交换可调用`memory_xchage`将两个内存颠倒顺序，内存差异对比可调用`memory_cmp`对比内存差异并返回列表。
```Python
from LyScript32 import MyDebug

# 交换两个内存区域
def memory_xchage(dbg,memory_ptr_x,memory_ptr_y,bytes):
    ref = False
    for index in range(0,bytes):
        # 读取两个内存区域
        read_byte_x = dbg.read_memory_byte(memory_ptr_x + index)
        read_byte_y = dbg.read_memory_byte(memory_ptr_y + index)

        # 交换内存
        ref = dbg.write_memory_byte(memory_ptr_x + index,read_byte_y)
        ref = dbg.write_memory_byte(memory_ptr_y + index, read_byte_x)
    return ref

# 对比两个内存区域
def memory_cmp(dbg,memory_ptr_x,memory_ptr_y,bytes):
    cmp_memory = []
    for index in range(0,bytes):

        item = {"addr":0, "x": 0, "y": 0}

        # 读取两个内存区域
        read_byte_x = dbg.read_memory_byte(memory_ptr_x + index)
        read_byte_y = dbg.read_memory_byte(memory_ptr_y + index)

        if read_byte_x != read_byte_y:
            item["addr"] = memory_ptr_x + index
            item["x"] = read_byte_x
            item["y"] = read_byte_y
            cmp_memory.append(item)
    return cmp_memory

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    # 内存交换
    flag = memory_xchage(dbg, 12386320,12386352,4)
    print("内存交换状态: {}".format(flag))

    # 内存对比
    cmp_ref = memory_cmp(dbg, 12386320,12386352,4)
    for index in range(0,len(cmp_ref)):
        print("地址: 0x{:08X} -> X: 0x{:02x} -> y: 0x{:02x}".format(cmp_ref[index].get("addr"),cmp_ref[index].get("x"),cmp_ref[index].get("y")))

    dbg.close()
```

**内存与磁盘机器码比较:** 通过调用`read_memory_byte()`函数，或者`open()`打开文件，等就可以得到程序磁盘与内存中特定位置的机器码参数，然后通过对每一个列表中的字节进行比较，就可得到特定位置下磁盘与内存中的数据是否一致的判断。
```Python
#coding: utf-8
import binascii,os,sys
from LyScript32 import MyDebug

# 得到程序的内存镜像中的机器码
def get_memory_hex_ascii(address,offset,len):
    count = 0
    ref_memory_list = []
    for index in range(offset,len):
        # 读出数据
        char = dbg.read_memory_byte(address + index)
        count = count + 1

        if count % 16 == 0:
            if (char) < 16:
                print("0" + hex((char))[2:])
                ref_memory_list.append("0" + hex((char))[2:])
            else:
                print(hex((char))[2:])
                ref_memory_list.append(hex((char))[2:])
        else:
            if (char) < 16:
                print("0" + hex((char))[2:] + " ",end="")
                ref_memory_list.append("0" + hex((char))[2:])
            else:
                print(hex((char))[2:] + " ",end="")
                ref_memory_list.append(hex((char))[2:])
    return ref_memory_list

# 读取程序中的磁盘镜像中的机器码
def get_file_hex_ascii(path,offset,len):
    count = 0
    ref_file_list = []

    with open(path, "rb") as fp:
        # file_size = os.path.getsize(path)
        fp.seek(offset)

        for item in range(offset,offset + len):
            char = fp.read(1)
            count = count + 1
            if count % 16 == 0:
                if ord(char) < 16:
                    print("0" + hex(ord(char))[2:])
                    ref_file_list.append("0" + hex(ord(char))[2:])
                else:
                    print(hex(ord(char))[2:])
                    ref_file_list.append(hex(ord(char))[2:])
            else:
                if ord(char) < 16:
                    print("0" + hex(ord(char))[2:] + " ", end="")
                    ref_file_list.append("0" + hex(ord(char))[2:])
                else:
                    print(hex(ord(char))[2:] + " ", end="")
                    ref_file_list.append(hex(ord(char))[2:])
    return ref_file_list

if __name__ == "__main__":
    dbg = MyDebug()

    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    module_base = dbg.get_base_from_address(dbg.get_local_base())
    print("模块基地址: {}".format(hex(module_base)))

    # 得到内存机器码
    memory_hex_byte = get_memory_hex_ascii(module_base,0,1024)

    # 得到磁盘机器码
    file_hex_byte = get_file_hex_ascii("d://Win32Project1.exe",0,1024)

    # 输出机器码
    for index in range(0,len(memory_hex_byte)):
        # 比较磁盘与内存是否存在差异
        if memory_hex_byte[index] != file_hex_byte[index]:
            # 存在差异则输出
            print("\n相对位置: [{}] --> 磁盘字节: 0x{} --> 内存字节: 0x{}".
                  format(index,memory_hex_byte[index],file_hex_byte[index]))
    dbg.close()
```

**内存ASCII码解析:** 通过封装的`get_memory_hex_ascii`得到内存机器码，然后再使用如下过程实现输出该内存中的机器码所对应的ASCII码。
```Python
from LyScript32 import MyDebug
import os,sys

# 转为ascii
def to_ascii(h):
    list_s = []
    for i in range(0, len(h), 2):
        list_s.append(chr(int(h[i:i+2], 16)))
    return ''.join(list_s)

# 转为16进制
def to_hex(s):
    list_h = []
    for c in s:
        list_h.append(hex(ord(c))[2:])
    return ''.join(list_h)

# 得到程序的内存镜像中的机器码
def get_memory_hex_ascii(address,offset,len):
    count = 0
    ref_memory_list = []
    for index in range(offset,len):
        # 读出数据
        char = dbg.read_memory_byte(address + index)
        count = count + 1

        if count % 16 == 0:
            if (char) < 16:
                ref_memory_list.append("0" + hex((char))[2:])
            else:
                ref_memory_list.append(hex((char))[2:])
        else:
            if (char) < 16:
                ref_memory_list.append("0" + hex((char))[2:])
            else:
                ref_memory_list.append(hex((char))[2:])
    return ref_memory_list


if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    # 得到模块基地址
    module_base = dbg.get_base_from_address(dbg.get_local_base())

    # 得到指定区域内存机器码
    ref_memory_list = get_memory_hex_ascii(module_base,0,1024)

    # 解析ascii码
    break_count = 1
    for index in ref_memory_list:
        if break_count %32 == 0:
            print(to_ascii(hex(int(index, 16))[2:]))
        else:
            print(to_ascii(hex(int(index, 16))[2:]),end="")
        break_count = break_count + 1

    dbg.close()
```

**内存特征码匹配:** 通过二次封装`get_memory_hex_ascii()`实现扫描内存特征码功能，如果存在则返回True否则返回False。
```Python
from LyScript32 import MyDebug
import os,sys

# 得到程序的内存镜像中的机器码
def get_memory_hex_ascii(address,offset,len):
    count = 0
    ref_memory_list = []
    for index in range(offset,len):
        # 读出数据
        char = dbg.read_memory_byte(address + index)
        count = count + 1

        if count % 16 == 0:
            if (char) < 16:
                ref_memory_list.append("0" + hex((char))[2:])
            else:
                ref_memory_list.append(hex((char))[2:])
        else:
            if (char) < 16:
                ref_memory_list.append("0" + hex((char))[2:])
            else:
                ref_memory_list.append(hex((char))[2:])
    return ref_memory_list


# 在指定区域内搜索特定的机器码,如果完全匹配则返回
def search_hex_ascii(address,offset,len,hex_array):
    # 得到指定区域内存机器码
    ref_memory_list = get_memory_hex_ascii(address,offset,len)

    array = []

    # 循环输出字节
    for index in range(0,len + len(hex_array)):

        # 如果有则继续装
        if len(hex_array) != len(array):
            array.append(ref_memory_list[offset + index])

        else:
            for y in range(0,len(array)):
                if array[y] != ref_memory_list[offset + index + y]:
                    return False

        array.clear()
    return False

if __name__ == "__main__":
    dbg = MyDebug()
    dbg.connect()

    eip = dbg.get_register("eip")

    # 得到模块基地址
    module_base = dbg.get_base_from_address(dbg.get_local_base())
    
    re = search_hex_ascii(module_base,0,100,hex_array=["0x4d","0x5a"])
    
    dbg.close()
```
特征码扫描一般不需要自己写，自己写的麻烦，而且不支持通配符，可以直接调用我们API中封装好的`scan_memory_one()`它可以支持`??`通配符模糊匹配，且效率要高许多。

**堆栈地址有符号无符号转换:** peek_stack命令传入的是堆栈下标位置默认从0开始，并输出一个`十进制有符号`长整数，首先实现有符号与无符号数之间的转换操作，为后续堆栈扫描做准备。
```Python
from LyScript32 import MyDebug

# 有符号整数转无符号数
def long_to_ulong(inter,is_64 = False):
    if is_64 == False:
        return inter & ((1 << 32) - 1)
    else:
        return inter & ((1 << 64) - 1)

# 无符号整数转有符号数
def ulong_to_long(inter,is_64 = False):
    if is_64 == False:
        return (inter & ((1 << 31) - 1)) - (inter & (1 << 31))
    else:
        return (inter & ((1 << 63) - 1)) - (inter & (1 << 63))

if __name__ == "__main__":
    dbg = MyDebug()

    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    for index in range(0,10):

        # 默认返回有符号数
        stack_address = dbg.peek_stack(index)

        # 使用转换
        print("默认有符号数: {:15} --> 转为无符号数: {:15} --> 转为有符号数: {:15}".
              format(stack_address, long_to_ulong(stack_address),ulong_to_long(long_to_ulong(stack_address))))

    dbg.close()
```

**扫描堆栈并反汇编一条:** 我们使用`get_disasm_one_code()`函数，扫描堆栈地址并得到该地址处的第一条反汇编代码。
```Python
from LyScript32 import MyDebug

# 有符号整数转无符号数
def long_to_ulong(inter,is_64 = False):
    if is_64 == False:
        return inter & ((1 << 32) - 1)
    else:
        return inter & ((1 << 64) - 1)

# 无符号整数转有符号数
def ulong_to_long(inter,is_64 = False):
    if is_64 == False:
        return (inter & ((1 << 31) - 1)) - (inter & (1 << 31))
    else:
        return (inter & ((1 << 63) - 1)) - (inter & (1 << 63))

if __name__ == "__main__":
    dbg = MyDebug()

    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    for index in range(0,10):

        # 默认返回有符号数
        stack_address = dbg.peek_stack(index)

        # 反汇编一行
        dasm = dbg.get_disasm_one_code(stack_address)

        # 根据地址得到模块基址
        if stack_address <= 0:
            mod_base = 0
        else:
            mod_base = dbg.get_base_from_address(long_to_ulong(stack_address))

        print("stack => [{}] addr = {:10} base = {:10} dasm = {}".format(index, hex(long_to_ulong(stack_address)),hex(mod_base), dasm))

    dbg.close()
```

**得到堆栈返回模块基址:** 首先我们需要得到程序全局状态下的所有加载模块的基地址，然后得到当前堆栈内存地址内的实际地址，并通过实际内存地址得到模块基地址，对比全局表即可拿到当前模块是返回到了哪里。
```Python
from LyScript32 import MyDebug

# 有符号整数转无符号数
def long_to_ulong(inter,is_64 = False):
    if is_64 == False:
        return inter & ((1 << 32) - 1)
    else:
        return inter & ((1 << 64) - 1)

# 无符号整数转有符号数
def ulong_to_long(inter,is_64 = False):
    if is_64 == False:
        return (inter & ((1 << 31) - 1)) - (inter & (1 << 31))
    else:
        return (inter & ((1 << 63) - 1)) - (inter & (1 << 63))

if __name__ == "__main__":
    dbg = MyDebug()

    connect_flag = dbg.connect()
    print("连接状态: {}".format(connect_flag))

    # 得到程序加载过的所有模块信息
    module_list = dbg.get_all_module()

    # 向下扫描堆栈
    for index in range(0,10):

        # 默认返回有符号数
        stack_address = dbg.peek_stack(index)

        # 反汇编一行
        dasm = dbg.get_disasm_one_code(stack_address)

        # 根据地址得到模块基址
        if stack_address <= 0:
            mod_base = 0
        else:
            mod_base = dbg.get_base_from_address(long_to_ulong(stack_address))

        # print("stack => [{}] addr = {:10} base = {:10} dasm = {}".format(index, hex(long_to_ulong(stack_address)),hex(mod_base), dasm))
        if mod_base > 0:
            for x in module_list:
                if mod_base == x.get("base"):
                    print("stack => [{}] addr = {:10} base = {:10} dasm = {:15} return = {:10}"
                          .format(index,hex(long_to_ulong(stack_address)),hex(mod_base), dasm,
                                  x.get("name")))

    dbg.close()
```

























