from setuptools import find_packages, setup


packages = find_packages(
    where="./", include=["django_mysql_utf8mb4", "django_mysql_utf8mb4.*"]
)
if not packages:
    raise ValueError("No packages detected.")

setup(
    name="django_mysql_utf8mb4",
    version="0.1.4",
    description="A migration, command and checks to ensure Django and MySQL are using the best-avaliable collation",
    url="https://github.com/software-opal/django_mysql_utf8mb4",
    author="Opal Symes",
    author_email="pypi@opal.codes",
    python_requires=">=3.5",
    license="",
    packages=packages,
    install_requires=["django>=2.0"],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python",
        "Topic :: Security",
    ],
)
