import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='easy_gui',
    version='0.1.0',
    packages=['easy_gui'],
    license='MIT',
    author='Zach Bateman',
    description='Easy Python tkinter applications',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zachbateman/easy_gui.git',
    download_url='https://github.com/zachbateman/easy_gui/archive/v_0.1.0.tar.gz',
    keywords=['GUI', 'TKINTER', 'APPLICATION', 'SIMPLE', 'EASY'],
    package_data={'': ['resources/transparent.ico']},
    include_package_data=True,
    install_requires=['matplotlib'],
    classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: MIT License',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.6',
                   'Programming Language :: Python :: 3.7',
                   'Programming Language :: Python :: 3.8',
                   ]
)
