from setuptools import setup

setup(name='exotelsdk',
      version='0.1',
      description='Python SDK for Exotel Call and SMS APIs',
      url='http://github.com/mvkaran/ExotelPy',
      author='MV Karan',
      author_email='karan@exotel.in',
      license='MIT',
      packages=['exotelsdk'],
      install_requires = ['requests==2.1.0', 'RequestsThrottlerExotel', \
       'python-dateutil'],
      zip_safe=False)
