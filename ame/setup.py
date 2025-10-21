from setuptools import setup, find_packages

setup(
    name="ame",
    version="0.2.0",
    description="Another Me Engine - Independent technical modules for AI avatar system",
    author="Another Me Team",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.24.0",
        "openai>=1.0.0",
        "chromadb>=0.4.0",
        "Pillow>=10.0.0",
        "python-magic>=0.4.27",
        "psutil>=5.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
