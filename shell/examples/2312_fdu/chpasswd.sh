
# 设置用户的密码
# BUG: 不能直接通过stdin来修改密码，需要使用临时文件
# name=lyx22
# passwd=1111
# echo $name:$passwd | chpasswd


# # 检查是否提供用户名文件
# if [ $# -ne 1 ]; then
#   echo "请提供包含用户名的文件作为参数"
#   exit 1
# fi
# userfile=$1
userfile=userlist.txt

# 检查用户名文件是否存在
if [ ! -f "$userfile" ]; then
  echo "用户名文件 '$userfile' 不存在"
  exit 1
fi

# temp_passwd_file=$(mktemp)
temp_passwd_file="user_passwords.txt"

# 逐行读取用户名并为其生成密码
while IFS= read -r username; do
  # 生成一个随机密码（12位）
  password=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 12)
  # 将用户名和密码保存到临时文件
  echo "$username:$password" >> "$temp_passwd_file"
done < "$userfile"

# 使用 chpasswd 命令批量设置密码
sudo chpasswd < "$temp_passwd_file"

# rm "$temp_passwd_file"
echo "密码已设置完成"

