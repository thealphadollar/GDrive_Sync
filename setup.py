from setuptools import setup


# access readme for long description
def readme():
    with open('README.md') as f_in:
        return f_in.read()


setup(
    name='drive_sync',  # name of the program
    version='0.95',  # current version
    description='GDrive_Sync is an automatic folder syncing client for Google Drive',
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities',
      ],
    keywords='google-drive GDrive automatic sync GDrive manager',
    url='http://github.com/thealphadollar/GDrive_Sync',  # link to repository
    author='thealphadollar',
    author_email='shivam.cs.iit.kgp@gmail.com',
    license='MIT',
    packages=['gdrive_sync'],  # folders to be included
    include_package_data=True,
    install_requires=[
        'pydrive',
        'python-crontab',
        'future'
      ],
    dependency_links=[],  # add github links of dependencies not present in pypi but have a setup file
    entry_points={
        'console_scripts': ['drive_sync=gdrive_sync.main:main']
    },
    zip_safe=False)
