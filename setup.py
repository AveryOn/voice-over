from setuptools import setup

setup(
    name='voice-over',
    version='0.1',
    py_modules=[],
    packages=['voiceover'],
    entry_points={
        'console_scripts': [
            'voice-over = voiceover.__main__:main',
        ],
    },
)
