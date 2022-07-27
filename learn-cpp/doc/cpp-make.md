

- [C和C++构建：Makefile编写详细指南](https://www.lsbin.com/280.html) #3 下面转了一半
- Linux 环境下通过 configure, make 编译安装的笔记参见 Documents.

## make 作为构建工具

Make使用Makefile作为构建脚本，我们在Makefile中编写项目编译链接指令，使用Make解析Makefile，并执行里面的指令。

流行的C/ C++替代构建系统有SCons、CMake、Bazel和Ninja。一些代码编辑器(如Microsoft Visual Studio)有自己的内置构建工具。对于Java，有Ant、Maven和Gradle。其他语言如Go和Rust也有自己的构建工具。

像Python、Ruby和Javascript这样的解释型语言不需要类似makefile的构建。makefile的目标是编译任何需要编译的文件，基于已经更改的文件。但当解释语言中的文件发生变化时，不需要重新编译任何文件。当程序运行时，使用文件的最新版本。

## GCC编译器选项


常用的GCC编译选项如下：

- `-o <file>`：指定输出文件名。
- `-Wall`：打印所有编译警告信息。
- `-Werror`：在产生警告的地方停止编译，迫使程序员重新修改代码。
- `-g`：生成gdb调试器使用的附加符号调试信息。
- `-E`：仅预处理文件（如导入头文件、预处理宏），不编译、汇编或链接。一般生成 `*.i` 源代码文件，文件包含源文件的完整代码形式。
- `-S`：仅编译，不汇编或链接。一般生成*.s文件，文件包含源代码的汇编代码。
- `-c`：编译和汇编，不链接。一般生产*.o或*.obj文件，文件包含源代码的二进制字节码。
- `ar rc lib<name>.a *.o`：编译静态库。
- `gcc -fPIC -shared -o lib<name>.so`：编译动态库。
- `gcc -c -I<dir> -o *.o`：使用指定头文件编译（库头文件），-I（大写i）指定编译使用的头文件目录（编译的时候需要库的头文件，链接的时候需要库的实现文件.a或.so，windows下是.lib或.dll）。
- `gcc -L<dir> -l<name>`：链接第三方库，包括动态库和静态库，`-L` 指定库文件目录，`-l` （大写l）指定库文件的名称，类Nnix下 前缀lib和后缀.a 省略，windows下需要完整名称，如 `-lapp.lib`。
- `-static`：强制链接时使用静态库链接。

对于静态库链接，搜索路径的顺序为：

- Ld会去找GCC命令中的 `-L` 参数。
- 然后找环境变量 `LIBRARY_PATH` 中的值。
- 找默认目录 `/lib`、`/usr/lib`、`/usr/local/lib`。

动态库的搜索路径顺序为：

- 找 `-L` 参数指定的目录。
- 找环境变量 `LD_LIBRARY_PATH` 中的路径。
- 找配置文件 `/etc/ld.so.conf` 中指定的路径。
- 找默认目录 `/lib` 和 `/usr/lib`。

C/C++开发一般是将编译和链接分开的，也就是说常用的一个命令是 `-c`，而编译.c/.cpp文件需要指定头文件目录，默认.cpp和.h在同一个目录中，但是如果使用库则不是了，需要使用 `-l<dir>` 指定头文件目录。

而链接的时候需要指定二进制文件，包括目标文件和库文件 `-L<dir>` 指定目录，`-l<name>` 指定库文件。

下面是GNU相关的常用命令：

- `file <filename>`：查看目标文件或可执行文件的类型。
- `nm <filename>`：查看二进制文件的符号表。
- `ldd <filename>`：查看可执行文件需要的共享库列表。

## GNU Make快速入门

下面是推荐的C/C++项目结构：

- `src`：放置项目源文件，里面可以再建立更多的目录（类似分包）。
- `bin/build`：目标文件或可执行文件，例如.o、.obj或.exe文件。
- `include`：库头文件，用于编译阶段。
- `lib`：库文件，包括静态库和动态库，用于链接阶段。
- `sources`：资源文件，例如配置文件、图片文件等。

e.g. 单个 `main.c` 文件


```makefile
# 文件名可以是makefile、Makefile或GNUMakefile
all: app

app: app.o
    gcc -o app app.o

app.o: main.c
    gcc -c -o app.o main.c

clean:
    rm app *o

run:
    ./app
```

**规则** 语法

```makefile
目标: 条件1 条件2 ...
    命令
```

- 其中命令左边空格是一个Tab (不能是空格)，目标和先决条件使用冒号 `:` 隔开
- 当make被要求执行一个规则时，它首先在 **先决条件** 中查找文件（一个条件可能对应一个文件）。如果任何先决条件都有关联的规则，则尝试先更新它们。
    - 如果先决条件不比target更新，则不会运行该命令
    - 例如, 连续运行两次 `make all`, 则会提示 ``make: Nothing to be done for `all'.`` 而不会执行.

### Makefile的更多内容

#### 注释和断行

注释以 `#` 开头，一直持续到行尾。长行可以通过反斜杠(`\`)断行并在几行中继续。

#### 虚假目标(或人为目标)

不代表文件的目标称为虚假目标。例如，上面例子中的“clean”，它只是一个命令的标签。如果目标是一个文件，它将根据其先决条件检查是否过时。“假目标”总是过时的，它的命令将被运行。标准的假目标是:all，clean，install。

#### 变量

变量以$开头，用圆括号(…)或大括号{…}括起来。单字符变量不需要圆括号，例如: `$(CC)`， `$(CC_FLAGS)`， `$@`， `$^`。

#### 自动变量

自动变量在匹配规则后由make设置。这包括:

- `$@`：目标文件名。
- `$*`：没有文件扩展名的目标文件名。
- `$<`：:第一个条件的文件名。
- `$^`：所有文件的先决条件，以空格分隔，丢弃重复的。
- `$+`：类似于$^，但包含重复项。
- `$?`：所有比目标更新的先决条件的名称，用空格分隔。

因此, 上例可以写成如下等价形式

```makefile
# 变量定义
app_name = app
clean_cmd = rm app *.o
COPTIONS = -c -o

# 使用变量: ${variable name}
all: ${app_name}

app: app.o
    gcc -o $@ $<

app.o: main.c
    gcc $(COPTIONS) $@ $^

# 2. 使用变量: $(variable name)
clean:
    $(clean_cmd)

run:
    ./app
```

#### 虚拟路径：VPATH & vpath

- 可以使用VPATH(大写)指定搜索依赖项和目标文件的目录。
- 你还可以使用vpath(小写)来更精确地描述文件类型及其搜索目录

```makefile
VPATH = src include
vpath %.c src
vpath %.h include
```



#### 模式规则

如果没有显式规则，可以使用模式匹配字符 `'%'` 作为文件名的模式规则来创建目标。例如,

```makefile
%.o: %.c
    $(COMPILE.c) $(OUTPUT_OPTION) $<
 
%: %.o
$(LINK.o) $^ $(LOADLIBES) $(LDLIBS) -o $@
```

#### 隐式模式规则

Make附带了大量的隐式模式规则，你可以通过 `make --print-data-base` 命令列出所有规则。
