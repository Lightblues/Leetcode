# ==================== 监控; 基本信息
# 架构
uname -a

# CPU 信息 
cat /proc/cpuinfo

# GPU
# https://askubuntu.com/questions/5417/how-to-get-the-gpu-info
sudo lshw -C display        # 一般这条就可以
lspci  -v -s  $(lspci | grep ' VGA ' | cut -d" " -f 1)

# 查看电源型号/状态
sudo dmidecode --type 39
# 功率监控
sudo powertop