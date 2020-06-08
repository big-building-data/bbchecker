import setuptools

setuptools.setup(
    name='bbchecker',
    version='0.0.1',
    author='Lucy Linder',
    author_email='lucy.derlin@gmail.com',
    description='Telegram BBData checker',
    license='Apache License 2.0',
    url='https://github.com/big-building-data/bbchecker',

    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),

    entry_points={
        'console_scripts': [
            'bbchecker = bbchecker.__main__:main',
        ]
    },
    install_requires=[
        'requests',
        'pytgbot==4.0.2',
    ]
)
