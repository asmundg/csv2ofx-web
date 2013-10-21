from setuptools import find_packages, setup

setup(name='csv2ofxweb',
      packages=find_packages(),
      install_requires=['flask',
                        'flask-bootstrap',
                        'flask-wtf',
                        'csv2ofx'],
      entry_points={
          'console_scripts': ['csv2ofx-web = csv2ofxweb.app:main']},
      package_data={'': ['*.cfg', 'templates/*.html']})
