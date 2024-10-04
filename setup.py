from setuptools import find_packages,setup


setup(
    name='mcqgenerator',
    version='0.0.1',
    author='Mohamed Karim Jegham',
    author_email='mohamedkarim.jegham@ensi-uma.tn',
    install_requires=['openai','langchain','streamlit','python-dotenv','PyPDF2'],
    packages=find_packages()
)