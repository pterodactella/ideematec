# Project Setup

## Create Virtual Environment

To create a virtual environment, follow these steps:

1. Open your terminal.
2. Navigate to your project directory.
3. Run the following command to create a virtual environment:

For this project conda was used but using pyenv is also an option. Below you have the commands to activate both types of virtual envs. It's important to note that the main difference between them is that using pyenv would create the env as a subdirectory thus it has to be ignored through the .gitignore file.
## Using pyenv

```sh
python -m venv venv
```

### Using conda

If you prefer to use conda, run:

```sh
conda create -n myenv python=3.9
```

4. Activate the virtual environment:

   - On Windows:

```sh
.\venv\Scripts\activate
```

    - On macOS and Linux:

```sh
source venv/bin/activate
```

### Or if you're using conda

```sh
conda activate myenv
```

## Install Requirements

Once the virtual environment is activated, install the required packages by running:

```sh
pip install -r requirements.txt
```

## This PROJECT uses a precommit hook please install it using:
```sh
pre-commit install
```
