from setuptools import find_packages, setup

package_name = 'Mapovac_sw'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='havlian',
    maintainer_email='havlian22@sps-prosek.cz',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'Comand_listener = Mapovac_sw.Comand_listener:main',
            'move = Mapovac_sw.move:main'
        ],
    },
)
