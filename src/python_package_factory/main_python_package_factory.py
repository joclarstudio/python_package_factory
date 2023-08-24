
import os
import shutil
import argcomplete
import argparse

# This little tool aims at facilitating the creation of pip installable project with cython configuration if asked
# project_name/
#     README.md [optional]
#     NOTICE [optional]
#     MANIFEST.in [optional]
#     LICENSE [optional]
#     AUTHORS.md [optional]
#     CHANGELOG.md [optional]
#     CONTRIBUTING.md [optional]
#     src/ [mandatory] 
#         project_name/
#             __init__.py
#             main_project_main.py
#             cysrc/ [mandatory if cython flag acitvated]
#                 toto/
#                     __init__.py
#                     toto.pyx
#                     c_toto.cpp
#                     c_toto.h

def common_creation_file(template_file_path: str,
                         output_file_path: str,
                         project_name: str) -> None:
    
    try:
        with open(template_file_path, "r") as inT:
                with open(output_file_path, "w") as osetupF:
                    for line in inT.readlines():
                        newline = line.replace("PROJECT_NAME", project_name)
                        osetupF.write(newline)
    except Exception:
        raise ValueError("Could not create the python setup file")

def create_setup_py_file(templates_dir: str,
                         project_root_path: str,
                         project_name: str,
                         is_cython: bool) -> None:
    """ 
    """
    setup_py_path: str = os.path.join( project_root_path, "setup.py" )
    template_setup_path: str = os.path.join(templates_dir, "cython_setup_py_template.txt") if is_cython else os.path(templates_dir, "setup_py_template.txt")
    common_creation_file(template_file_path= template_setup_path, output_file_path=setup_py_path, project_name=project_name)

def create_setup_cfg_file(templates_dir: str,
                          project_root_path: str,
                          project_name: str,
                          is_cython: bool) -> None:
    """ 
    """
    setup_cfg_path: str = os.path.join( project_root_path, "setup.cfg" )
    template_setup_path: str = os.path.join(templates_dir, "cython_setup_cfg_template.txt") if is_cython else os.path(templates_dir, "setup_cfg_template.txt")
    common_creation_file(template_file_path= template_setup_path, output_file_path=setup_cfg_path, project_name=project_name)

def create_pyproject_toml_file(templates_dir: str,
                               project_root_path: str, 
                               is_cython: bool):
    """ """
    pyproject_path: str = os.path.join( project_root_path, "pyproject.toml")
    template_setup_path: str = os.path.join(templates_dir, "cython_pyproject_toml_template.txt") if is_cython else os.path(templates_dir, "pyproject_toml_template.txt")
    shutil.copyfile(template_setup_path, pyproject_path)

def create_main_python_src_file(templates_dir: str,
                                src_dir_path: str,
                                project_name: str,
                                is_cython: bool) -> None:
    """ """
    template_src_path: str = os.path.join(templates_dir, "cython_main_src_project_py_template.txt") if is_cython else os.path(templates_dir, "main_src_project_py_template.txt")
    main_src_path: str = os.path.join(src_dir_path, "main_" + project_name + ".py")
    common_creation_file(template_file_path= template_src_path, output_file_path=main_src_path, project_name=project_name)

def create_src_directory(templates_dir: str,
                         project_name: str,
                         project_root_path: str,
                         is_cython: bool) -> None:
    """ """
    try:
        src_dir_path: str = os.path.join(project_root_path, "src", project_name)
        os.makedirs(src_dir_path)

        # Create a blank __init__.py file necessary for Python for packaging
        with open(os.path.join(src_dir_path, "__init__.py"), "w") as initF:
            pass

        create_main_python_src_file(templates_dir =  templates_dir,
                                    src_dir_path = src_dir_path,    
                                    project_name = project_name, 
                                    is_cython = is_cython)

        if is_cython:
            cy_hello_dir_path: str = os.path.join(src_dir_path, "cysrc", "hello")
            os.makedirs(cy_hello_dir_path)

            # Create a blank __init__.py file necessary for Python for packaging
            with open(os.path.join(cy_hello_dir_path, "__init__.py"), "w") as initF:
                pass

            # Copy all cython files
            pyx_path: str = os.path.join(cy_hello_dir_path, "hello.pyx")
            cpp_path: str = os.path.join(cy_hello_dir_path, "c_hello.cpp")
            header_path: str = os.path.join(cy_hello_dir_path, "c_hello.h")
            shutil.copyfile(os.path.join(templates_dir, "cython_hello_pyx_template.txt"), pyx_path)
            shutil.copyfile(os.path.join(templates_dir, "cpp_hello_header_template.txt"), header_path)
            shutil.copyfile(os.path.join(templates_dir, "cpp_hello_src_template.txt"), cpp_path)

    except Exception:
        raise ValueError(f"Could not create the directory {src_dir_path}")

def create_mandatory_file(templates_dir: str,
                          project_name: str,
                          project_root_path: str,
                          is_cython: bool = False) -> None:
    """ 
    """
    # Creation of setup.py file
    create_setup_py_file(templates_dir=templates_dir,
                         project_root_path = project_root_path, 
                         project_name = project_name,
                         is_cython=is_cython)

    # Creation of setup.cfg file
    create_setup_cfg_file(templates_dir=templates_dir,
                          project_root_path = project_root_path, 
                          project_name = project_name,
                          is_cython=is_cython)
    
    # Creation of pyproject.toml
    create_pyproject_toml_file(templates_dir=templates_dir,
                               project_root_path = project_root_path, 
                               is_cython = is_cython)

    # Creation of the src directory
    create_src_directory(templates_dir=templates_dir,
                         project_name = project_name,
                         project_root_path = project_root_path,
                         is_cython = is_cython)

def main_start_algo(templates_dir: str = None,
                    input_dir_path: str = None,
                    input_project_name: str = None,
                    input_mode: str = "proto", #proto or pluto
                    is_cython: bool = False) -> None :
    """ 
    """
    if os.path.isdir(input_dir_path):
        project_root_path: str = os.path.join(input_dir_path, input_project_name)
        if os.path.isdir(project_root_path) or os.path.isfile(project_root_path):
            print(f"You already have a project with the same name in your given directory")
        else:
            try:
                os.mkdir(project_root_path)

                create_mandatory_file(templates_dir=templates_dir,
                                      project_name = input_project_name, 
                                      project_root_path = project_root_path,
                                      is_cython=is_cython)

                
            except Exception:
                raise ValueError(f"Could not create the directory {project_root_path}")
    else:
        print(f"The input directory {input_dir_path} does not exist")

def get_parser():
    """
    Argument parser for Python Package Factory (CLI).

    Returns:
        the parser.
    """
    parser = argparse.ArgumentParser(description=("Python Package Factory"))

    parser.add_argument(
        "--templates_dir", required=True, type=str, help="Templates files used to create the project."
    )

    parser.add_argument(
        "--input_dir", required=True, type=str, help="Directory where the project will be created."
    )

    parser.add_argument(
        "--name", required=True, type=str, help="Name of the project."
    )

    parser.add_argument(
        "--cython", required=False, type=int, help="set to 1 for a Cython project", default=0
    )

    
    #TODO add all the parameters
    return parser


def python_package_factory_cli():

    parser = get_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    is_cython: bool = True if args.cython == 1 else False

    main_start_algo(templates_dir= args.templates_dir,
                    input_dir_path = args.input_dir,
                    input_project_name = args.name,
                    is_cython= is_cython)