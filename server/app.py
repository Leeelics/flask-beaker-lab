import os
import logging
from flask import Flask, redirect,render_template, send_from_directory, send_file, url_for

app = Flask(__name__, template_folder='')

logging.basicConfig(level=logging.DEBUG)

report_path = 'output/allure-report'  # 指定文件夹路径
# report_path = os.path.abspath('output/allure-report')

# 获取指定路径下的所有文件和文件夹


def get_contents(path):
    contents = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            contents.append(
                {'name': item, 'type': 'folder', 'path': item_path})
        else:
            contents.append({'name': item, 'type': 'file', 'path': item_path})
    return contents


def build_file_tree(root_dir):
    file_tree = {}
    for root, dirs, files in os.walk(root_dir):
        current_dir = file_tree
        for dir_name in root.split(os.sep):
            if dir_name not in current_dir:
                current_dir[dir_name] = {}
            current_dir = current_dir[dir_name]
        current_dir['_files'] = files
    return file_tree


# 渲染文件夹内容的模板
@app.route('/reports')
def index():
    contents = get_contents(report_path)
    return render_template('reports.html', contents=contents)

# 处理点击文件夹时的跳转


@app.route('/reports/<path:folder_path>')
def folder(folder_path):

    contents = get_contents(folder_path)
    print(f'----------{contents}---------------')
    for item in contents:
        a = os.getcwd()
        b = os.path.join(a, item['path'])
        print(f'----------{b}---------------')
        if item['name'] == 'index.html':
            print(f'-**********{b}*****-----------------------')
            # return url_for(b)
            return redirect(url_for('aaa_index', folder_path='output/allure-report/test01'))
    return render_template('index.html', contents=contents)


@app.route('/reports/<path:folder_path>/')
def aaa_index(folder_path):
    print(f'------------------------------------------------999sdfsfsfwe')
    return send_from_directory(folder_path, 'index.html')


if __name__ == '__main__':
    app.run(debug=True)
