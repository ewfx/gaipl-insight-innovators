from setuptools import setup, find_packages

setup(
    name="genai_ipe",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "streamlit",
        "langchain",
        "openai",
        "tqdm",
        "plotly",
        "python-dotenv",
        "faiss-cpu"
    ],
    entry_points={
        "console_scripts": [
            "run-ipe-ui=streamlit_ui:main"
        ]
    },
    author="Your Name",
    description="Gen AI Integrated Platform Environment (IPE)",
    license="MIT",
)
