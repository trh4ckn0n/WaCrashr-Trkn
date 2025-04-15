from setuptools import setup

setup(
    name='WaCrashr-Trkn',
    version='1.0.0',
    description='WhatsApp Crash Tool with QR Code and URL Shortening via TOR',
    author='trhacknon',
    author_email='jeremydiliotti@gmail.com',
    url='https://github.com/trh4ckn0n/WaCrashr-Trkn',  
    packages=['WaCrashr_Trkn'],  
    install_requires=[
        'tk',
        'requests',
        'qrcode',
        'Pillow',
    ],
    entry_points={
        'console_scripts': [
            'whatsapp-crash=WaCrashr_Trkn.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',  
)
