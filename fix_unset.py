import os
import re
import subprocess

env = os.environ.copy()

# 运行 yarn lint 命令
result = subprocess.run('yarn lint', stdout=subprocess.PIPE, shell=True, env=env)
# 解析输出结果
output = result.stdout.decode('utf-8')
lines = output.split('\n')

# 正则表达式，用于匹配变量名
pattern = re.compile(r"'(\w+)' is (defined but never used|assigned a value but never used)")

for line in lines:
    if '(unused-imports/no-unused-vars)' in line:
        match = pattern.search(line)
        if match:
            # 获取变量名
            var_name = match.group(1)

            # 获取文件名和行号
            file_info = line.split(' ')[-1]
            file_name, line_number = file_info.split(':')[:2]
            line_number = int(line_number)

            # 读取文件内容
            with open(file_name, 'r', encoding='utf-8') as file:
                content = file.readlines()

            # 在变量名前添加 '_'
            line_content = content[line_number - 1]
            content[line_number - 1] = re.sub(rf'\b{var_name}\b', '_' + var_name, line_content)

            # 写回文件
            with open(file_name, 'w', encoding='utf-8') as file:
                file.writelines(content)
