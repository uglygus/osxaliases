import osxaliases
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="osxaliases-pkg-uglygus",  # Replace with your own username
    version=osxaliases.__version__,
    author="Example Author",
    author_email="author@example.com",
    description="simplified wrapper for multiprocessing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points = {
        'console_scripts': [
        'osxaliases = osxaliases.osxaliases:main',
      ],
    },
)
