########################## SQL
sudo apt update
sudo apt install mysql-server
# 验证安装成功
mysqladmin --version
# 创建用户（默认直接 mysql 登陆无密码）
mysqladmin -u root password 123456
# 登陆
mysql -uroot -p
