

```bash
g++ main.cpp workerManager.cpp -include workerManager.h #测试 showMenu()
g++ main.cpp -include worker.h -include employee.h -include manager.h -include boss.h employee.cpp managerr.cpp boss.cpp  #test() 测试职工抽象类。#include "worderManager.h" 虽然写了但没用到的情况下编译不引入也没问题
g++ main.cpp -include worker.h -include employee.h -include manager.h -include boss.h employee.cpp managerr.cpp boss.cpp -include workerManager.h workerManager.cpp
```