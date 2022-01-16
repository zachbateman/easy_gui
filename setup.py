import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='easy_gui',
    version='0.4.4',
    packages=['easy_gui'],
    license='MIT',
    author='Zach Bateman',
    description='Easy Python GUI applications (tkinter wrapper)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zachbateman/easy_gui.git',
    download_url='https://github.com/zachbateman/easy_gui/archive/v_0.4.4.tar.gz',
    keywords=['GUI', 'TKINTER', 'APPLICATION', 'SIMPLE', 'EASY'],
    package_data={'': ['resources/transparent.ico']},
    include_package_data=True,
    install_requires=['matplotlib'],
    classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   'Programming Language :: Python :: 3.9',
                   'Programming Language :: Python :: 3.10',
                   ]
)
