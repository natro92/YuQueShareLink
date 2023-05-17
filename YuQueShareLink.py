# -*- encoding: utf-8 -*-
"""
@File    :   YuQueShareLink.py
@Contact :   2997453446@qq.com
@Blog :   natro92.github.io

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2023/5/16 21:04   natro92      1.0         将语雀链接在导出到博客时可以正常使用
"""

import re
import sys
import os
from datetime import datetime
import subprocess

# 在这里修改你想要提示自己的tag名称和categories名称
other_tags = ''
other_categories = ''


def replace_string_in_file(file_path):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()

    # 使用正则表达式匹配所有符合条件的字符串，并进行替换操作
    replaced_content = re.sub(r".png#\S+\)", ".png)", content)

    with open(file_path, "w", encoding="utf-8", errors="ignore") as file:
        file.write(replaced_content)


def add_headers_in_file(file_path):
    file_name = os.path.basename(file_path)
    replaced_content = re.sub(r".md", "", file_name)
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(file_path, 'r+', encoding="utf-8", errors="ignore") as f:
        contents = f.read()
        print('当前tags:', ['WriteUp', 'CTFshow0-1'])
        print('当前categories:', ['CTF'])
        new_tags = input('你想要修改tags吗？ (y/n) 默认n')
        if new_tags.lower() == 'y':
            tags_str = input('输入你的tags，注意用英文逗号分隔: ')
            tags = [tag.strip() for tag in tags_str.split(',')]
        else:
            tags = ['WriteUp', 'CTFshow0-1']

        new_categories = input('你想要修改tags吗？(y/n) 默认n')
        if new_categories.lower() == 'y':
            categories_str = input('输入你的categories，注意用英文逗号分隔: ')
            categories = [category.strip() for category in categories_str.split(',')]
        else:
            categories = ['CTF']

        new_contents = '---\n' \
                       'title: ' + file_name + '\n' \
                                               'date: ' + time_str + '\n' \
                                                                     'tags:\n'
        for tag in tags:
            new_contents += '  - ' + tag + '\n'
        new_contents += 'categories:\n'
        for category in categories:
            new_contents += '  - ' + category + '\n'
        new_contents += '---\n' \
                        + contents

        f.seek(0)
        f.write(new_contents)


def hexo_generate_and_deploy():
    # cmd命令 cd后修改为你自己的blog文件夹位置
    # 字符串前面加r防止解析，或者将单斜杠转换为双斜杠
    cmd = r'cd C:\Users\natro92\Desktop\blog && hexo g && hexo d'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    print(p.stdout.read().decode())
    a = input('按任意键继续')


def git_backup():
    # 实现备份git功能
    # 切换到本地的git仓库目录
    repo_dir = r'C:\Users\natro92\Desktop\blog'
    # python3.6特性，格式化文本
    cmd_cd = f'cd {repo_dir} && '
    cmd_add = 'git add .'
    commit_msg = '%date:~0,4%%date:~5,2%%date:~8,2%'
    cmd_commit = f'git commit -m "{commit_msg}"'
    cmd_push = 'git push'
    cmd = cmd_cd + cmd_add + ' && ' + cmd_commit + ' && ' + cmd_push
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    print(result.stdout.decode())


if __name__ == "__main__":
    
    print("请提供需要处理的文件路径, 且文件需要和该py脚本处在同一文件夹下，比如：我的博客.md")
    file_path = input("路径：")
    is_end_of_md = re.search(r"\.md", file_path)
    if not is_end_of_md:
        file_path += ".md"
    try:
        replace_string_in_file(file_path)
    except Exception as e:
        print(e)
    with open(file_path, 'r', encoding="utf-8", errors="ignore") as file:
        first_line = file.readline()
        if not first_line.startswith('---'):
            print('File starts with ---title:')
            next_step = input("是否继续生成hexo文件头(y/n) 默认y")
            if next_step == 'y' or next_step == '':
                add_headers_in_file(file_path)
                print("添加header格式成功")
    upload_step = input("是否更新内容并且上传(y/n) 默认y")
    if upload_step == 'y' or upload_step == '':
        hexo_generate_and_deploy()
    git_step = input("是否将源文件git到私有仓库(y/n) 默认y")
    if git_step == 'y' or git_step == '':
        git_backup()
        a = input('按任意键退出')
        if a:
            sys.exit()
