##### 用户管理
# see https://www.runoob.com/linux/linux-user-manage.html 
### 添加
useradd -D # 查看默认配置
useradd -m -d /home/syc -s /bin/zsh -G root test     # -m 新建目录

# 禁止登陆 shell；为了启动apache、nginx、mysql等服务
useradd username -s /sbin/nologin

### 删除
userdel -r sam  # -r 删除主目录

### 添加 sudo 权限
# 方案1
usermod -a -G sudo steven       # 这里加到 sudo 用户组，而在 centOS 中默认的是 wheel 组
# 方案2 直接修改
chmod u+w /etc/sudoers      # 默认只读
vi /etc/sudoers 
# 在 root ALL=(ALL) AL 下面 添加 
# syc ALL=(ALL) ALL         表示用户需要输入密码执行sudo
# %youusergroup ALL=(ALL) NOPASSWD: ALL     表示用户组内的用户不用输入密码即可执行sudo命令
chmod u-w /etc/sudoers

### 用户组
groups # 查看当前登录用户的组内成员
groups gliethttp # 查看gliethttp用户所在的组
whoami # 查看当前登录用户名
# /etc/group文件包含所有组
# /etc/shadow和/etc/passwd系统存在的所有用户名


