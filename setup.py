from setuptools import setup, find_packages

setup(name='pyconindia',
      version='0.1.0',
      description='PyCon India',
      author='PyCon India Organizers',
      packages=find_packages(),
      include_package_data=True,
      entry_points={
        'console_scripts': [
            'publicitymail=publicity.mail:main',
        ],
      },
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Envelopes',
          'Jinja2',
      ],
      )

