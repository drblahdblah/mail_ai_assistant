from setuptools import setup, find_packages

setup(
    name='email_ai_assistant',
    version='0.1.0',
    description='Local AI Email Assistant with RAG, Ollama, and LangChain',
    author='David Jones',
    author_email='drblahdblah@gmail.com',
    packages=find_packages(include=['backend', 'backend.*', 'frontend', 'frontend.*', 'scripts', 'scripts.*']),
    python_requires='>=3.10',
    install_requires=[
        'langchain>=0.1.20',
        'llama-index>=0.10.32',
        'faiss-cpu>=1.7.4',
        'ollama>=0.1.6',
        'sentence-transformers>=2.2.2',
        'scikit-learn>=1.4.2',
        'mail-parser>=3.15.0',
        'python-dateutil>=2.8.2',
        'gradio>=4.30.0',
        'agentq>=0.0.4',
        'networkx>=3.2.1',
        'tqdm>=4.66.2',
        'rich>=13.7.1',
        'pydantic>=2.7.1',
        'openai>=1.30.3',
    ],
    entry_points={
        'console_scripts': [
            'email-ai-ingest=scripts.ingest_emails:main',
            'email-ai-run=scripts.run_local_app:main',
            'email-ai-ui=frontend.ui:main',
        ],
    },
)
