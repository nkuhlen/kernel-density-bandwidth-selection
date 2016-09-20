# Bandwidth Selection for Kernel Density Estimation
This project analyses the performance of different bandwidth selection methods when applied to both simulated and real world data. In particular, I apply the procedures to estimate the world income distribution which allows to investigate the development of income inequality between countries.

Building the Project
--------------------

The project is written in Python and R. It is built using [Waf](https://code.google.com/p/waf/). After a successful build, the full documentation of the project can be found in:
				
		project_documentation/index.html 

To run Waf and execute the files, you need to:

1. Save the project on your computer (clone the repository or save the zip file).

2. Install Miniconda or Anaconda in case they are not already installed and make sure that a LaTeX distribution can be found on your path.

3. Make sure an R executable is added to your path. Under Mac OS X, this can be achieved by opening the bash profile in a shell and adding for example:

        # R directory
        export PATH="${PATH}:/Applications/R.app/Contents/MacOS"

    Details on how to open the bash profile in a shell and general instructions for adding programmes permanently to your path for Windows, Mac and Linux can be found [here](http://hmgaudecker.github.io/econ-python-environment/paths.html).

4. Navigate to the project folder in a shell and execute the following commands to create a conda environment (named as the current directory) with a minimal Python setup.

   **(Mac, Linux)**

        source set-env.sh

   **(Windows)**

        set-env.bat

     Details for setting up a Python environment can be found [here](http://hmgaudecker.github.io/econ-python-environment/).

5. Execute the following commands in the shell:

        python waf.py configure
        python waf.py build
        python waf.py install

    The execution of the first command will fail if any of the programmes required to run the project is not installed.

Note
----

In case you just want to quickly execute the whole project, apply the following changes to greatly reduce the runtime:
    
    src/model_specs/draws.json (line 2): "configuration_0": 10
