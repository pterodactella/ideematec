# Project Setup

## Create Virtual Environment

To create a virtual environment, follow these steps:

1. Open your terminal.
2. Navigate to your project directory.
3. Run the following command to create a virtual environment:

## I use conda but you could use the pyenv

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
