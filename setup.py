import os
from setuptools import find_packages, setup

_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_version():
    with open(os.path.join(_CURRENT_DIR, "jax_am/__init__.py")) as file:
        for line in file:
            if line.startswith("__version__"):
                return line[line.find("=") + 1:].strip(' \'"\n')
        raise ValueError('`__version__` not defined in `jax_am/__init__.py`')

__version__ = get_version()


if __name__=='__main__':
    setup(
        name="jax-am",
        version=__version__,
        description="GPU-accelerated simulation toolbox for additive manufacturing based on JAX.",
        author="Xue et al.",
        author_email="tianjuxue@outlook.com",
        long_description=open(os.path.join(_CURRENT_DIR, "README.md")).read(),
        long_description_content_type='text/markdown',
        packages=find_packages(exclude=['*.test*']),
        python_requires=">=3.6",
        install_requires=[
            "jax",
            "jaxlib",
            "matplotlib",
            "numpy",
            "scipy",
            "orix",
            "meshio",
            "pyfiglet",
            "scikit-learn",
            # gmsh, fenics-basix removed in EmergentMatter fork:
            # they were FEM-only deps consumed by the now-deleted
            # jax_am/fem/ module. Verified zero imports remaining
            # in jax_am/{cfd,lbm,phase_field}. meshio kept — used
            # by jax_am/common.py + jax_am/lbm/core.py + most demos.
        ],
        url="https://github.com/tianjuxue/jax-am",
        license="GPL-3.0",
        classifiers=[
            'Programming Language :: Python :: 3',
            'Operating System :: MacOS',
            'Operating System :: POSIX :: Linux',
            'Topic :: Software Development',
            'Topic :: Scientific/Engineering',
            'Intended Audience :: Science/Research',
        ]
    )