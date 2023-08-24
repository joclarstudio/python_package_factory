# python_package_factory
A small tool to create a Python or Cython project package

## How to install it
clone this project, go to it and simply run
```
pip install .
```

## How to use it
In your terminal:

For a full Python project
```
python_package_factory --templates_dir templates/ --input_dir "your input directory path" --name "your awesome project name"
```

For a Cython project:
```
python_package_factory --templates_dir templates/ --input_dir "your input directory path" --name "your awesome project name" --cython 1
```
The templates directory is given in this repository.

Then you can go to the directory of your newly created project and run

```
pip install .
```

A cli is automatically created with your project name.

If you run:

```
project_name
```

For a full Python project you should see this message:
```
hello buddy ! You are not using Cython bad boy !
```
For a Cython project, this message:
```
hello buddy ! You are using Cython good boy !
```
Then you are good to go !


