from setuptools import setup, find_packages

setup(
    name="test-calculator",
    version="1.0.0",
    description="A simple calculator for testing CI/CD pipelines",
    author="Test Developer",
    author_email="test@example.com",
    py_modules=["calculator"],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "isort>=5.0.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
        ],
    },
)