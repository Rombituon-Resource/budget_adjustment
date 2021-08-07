from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in budget_adjustment/__init__.py
from budget_adjustment import __version__ as version

setup(
	name='budget_adjustment',
	version=version,
	description='An ERPNext Application to reallocate budget from one or more accounts to other accounts. A budget adjustment voucher is submitted and it changes the original budget will be reflected.',
	author='Chris',
	author_email='christophernjogu@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
