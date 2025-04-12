from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='simpsave',  # 包名称
    version='3.2',  # 当前版本号
    install_requires=[],  # 依赖项列表
    packages=find_packages(),  # 自动发现包
    author='WaterRun',  # 作者名
    author_email='2263633954@qq.com',  # 作者邮箱
    description='A lightweight Python library for persisting basic variables using .ini files. Simple, fast, and ideal for small-scale data storage.',  # 优化后的简要描述
    long_description=long_description,  # 长描述，通常是 README.md 内容
    long_description_content_type='text/markdown',  # 长描述格式为 Markdown
    url='https://github.com/Water-Run/SimpSave',  # 项目主页
    classifiers=[
        'Programming Language :: Python :: 3',  # 支持的编程语言
        'Programming Language :: Python :: 3.10',  # 明确支持 Python 3.10+
        'License :: OSI Approved :: MIT License',  # 开源许可证
        'Operating System :: OS Independent',  # 跨平台支持
        'Intended Audience :: Developers',  # 目标用户
        'Topic :: Software Development :: Libraries :: Python Modules',  # 分类主题
    ],
    python_requires='>=3.10',  # Python 版本要求
)