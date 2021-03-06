from setuptools import setup


setup(name='uorm',
      version='0.4',
      description="""Very lightweight, memory-efficient (uses generator \
protocol), dependency-free anti-ORM (Object-Relational Mapper) for \
Pycopy (https://github.com/pfalcon/pycopy). Using this module, one can \
simplify typical database access operations, without trading well-known \
SQL for an obscure and inefficient ORM pseudo-language.
""",
      url='https://github.com/pfalcon/uorm',
      author='Paul Sokolovsky',
      author_email='pfalcon@users.sourceforge.net',
      license='MIT',
      py_modules=['uorm'],
      install_requires=['pycopy-sqlite3'])
