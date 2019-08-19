from distutils.core import setup

setup(
    name='protodf',
    packages=['protodf'],
    version='0.1',
    license='MIT',
    description='A package which lets you run PySpark SQL on your Protobuf data',
    author='Rafi Aroch',
    author_email='rafi@aroch.com',
    url='https://github.com/aroch/protobuf-dataframe',
    download_url='https://github.com/aroch/protobuf-dataframe/archive/v0.1.tar.gz',
    keywords=['pyspark', 'dataframe', 'protobuf', 'spark-sql'],
    install_requires=[
        'pyspark'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
