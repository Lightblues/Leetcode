# ========== 批量生成用户 ===============
suffix=22
# 罗子钦 李煜新 于鹏 李施仪 李俨达 肖露露 洪丽凤 姜国超 刘晋汐 刘为灿 刘永 骆聪逸 秦思淼 许跃泷 丁泽澎
for name1 in lzq lyx yp lsy lyd xll hlf jgc ljx lwc ly lcy qsm xyl dzp; do
    name=$name1$suffix
    useradd -s/bin/bash -m $name
    echo $name:$name | chpasswd
done

# ========== 修改用户密码, 随机生成, 并记录 ===============
# Path: shell/servers/useradd.sh

# 检查是否提供用户名文件
if [ $# -ne 1 ]; then
  echo "请提供包含用户名的文件作为参数"
  exit 1
fi

userfile=$1
passwordfile="user_passwords.txt"

# 检查密码文件是否存在，如果存在则备份
if [ -f "$passwordfile" ]; then
  mv "$passwordfile" "${passwordfile}_backup_$(date +'%Y%m%d%H%M%S').txt"
fi

# 生成并保存用户名和密码
while IFS= read -r username; do
  # 生成随机密码（12位）
  password=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 12)
  
  # 输出用户名和密码到终端
  echo "用户名: $username, 密码: $password"
  
  # 将用户名和密码保存到文件
  echo "用户名: $username, 密码: $password" >> "$passwordfile"
done < "$userfile"

echo "用户名和密码已保存到 $passwordfile"

