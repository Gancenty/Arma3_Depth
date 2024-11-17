from colorama import Fore, Back, Style, init

# 初始化 colorama
init(autoreset=True)

# 使用不同的颜色
print(Fore.RED + "这是红色文字")
print(Fore.GREEN + "这是绿色文字" + Fore.BLACK + Back.YELLOW + "，黄背景")
print(Style.BRIGHT + Fore.BLUE + "亮蓝色文字")

print(set(range(0, 10 + 2)))