# Pylit - Pylint and PEP8 Sublime Text integration
Inspect py file with PyLint and PEP8 and show results.

## Installation
Note with either method, you may need to restart Sublime Text 2 for the plugin to load.

You must install Pylint and PEP8 manualy!

### Package Control
TODO: Add to Package Control

### Manual
Clone git repo to Sublime packages dir.

    git clone git://github.com/d4rkr00t/Pylit.git Pylit

After installing plugin, configure path to phpcs executable file:

    {
        "remove_line_to_long": false, # remove message for line to long
        "pylint":{
            "osx": "pylint",
            "windows": "pylint",
            "linux": "pylint"
        },
        "pep8":{
            "osx": "pep8",
            "windows": "pep8",
            "linux": "pep8"
        }
    }

## Usage

Plugin has two commands:

### Pylit command:
In .py file press cmd+p and find "Pylit - Python code quality check" command.
Thats show list of pep8 and pylint recomandation and if you select its line coursour has been moved to place where fix is needed.

Example output:

![pylint](https://dl.dropboxusercontent.com/u/3678884/pylin-screenshot.png)

### Pylit Report command
In .py file press cmd+p and find "Pylit Report - Python code quality check and report" command.
This command will be generate a more complete report for current file.

Example output:

    # ====================================
    # PEP8
    # ====================================

    2:15: E401 multiple imports on one line
    5:1: E302 expected 2 blank lines, found 1
    14:80: E501 line too long (119 > 79 characters)
    14:119: E502 the backslash is redundant between brackets
    15:21: E128 continuation line under-indented for visual indent
    23:80: E501 line too long (117 > 79 characters)
    23:117: E502 the backslash is redundant between brackets
    24:21: E128 continuation line under-indented for visual indent
    29:68: E231 missing whitespace after ','
    40:1: W293 blank line contains whitespace

    # Pylit.py
    # ====================================

    # ====================================
    # PyLint
    # ====================================

    ************* Module Pylit
    C: 14,0: Line too long (119/80)
    C: 23,0: Line too long (117/80)
    C:  1,0: Missing docstring
    F:  2,0: Unable to import 'sublime'
    F:  2,0: Unable to import 'sublime_plugin'
    W:  5,0:Pylit: Class has no __init__ method
    C:  5,0:Pylit: Missing docstring
    C:  6,4:Pylit.run: Missing docstring
    E:  7,19:Pylit.run: Instance of 'Pylit' has no 'window' member
    W: 34,19:Pylit.run: Catching too general exception Exception
    C: 14,16:Pylit.run: Invalid name "p" for type variable (should match [a-z_][a-z0-9_]{2,30}$)
    C: 23,16:Pylit.run: Invalid name "p" for type variable (should match [a-z_][a-z0-9_]{2,30}$)
    E: 31,23:Pylit.run: Instance of 'Pylit' has no 'window' member
    C: 34,30:Pylit.run: Invalid name "e" for type variable (should match [a-z_][a-z0-9_]{2,30}$)
    W: 17,21:Pylit.run: Unused variable 'err'
    C: 43,4:Pylit.output_title: Missing docstring
    R: 43,4:Pylit.output_title: Method could be a function
    C: 49,4:Pylit.section_title: Missing docstring
    R: 49,4:Pylit.section_title: Method could be a function


    Report
    ======
    35 statements analysed.

    Duplication
    -----------

    +-------------------------+------+---------+-----------+
    |                         |now   |previous |difference |
    +=========================+======+=========+===========+
    |nb duplicated lines      |0     |0        |=          |
    +-------------------------+------+---------+-----------+
    |percent duplicated lines |0.000 |0.000    |=          |
    +-------------------------+------+---------+-----------+



    Raw metrics
    -----------

    +----------+-------+------+---------+-----------+
    |type      |number |%     |previous |difference |
    +==========+=======+======+=========+===========+
    |code      |38     |97.44 |39       |-1.00      |
    +----------+-------+------+---------+-----------+
    |docstring |0      |0.00  |0        |=          |
    +----------+-------+------+---------+-----------+
    |comment   |1      |2.56  |1        |=          |
    +----------+-------+------+---------+-----------+
    |empty     |0      |0.00  |0        |=          |
    +----------+-------+------+---------+-----------+



    Messages by category
    --------------------

    +-----------+-------+---------+-----------+
    |type       |number |previous |difference |
    +===========+=======+=========+===========+
    |convention |10     |10       |=          |
    +-----------+-------+---------+-----------+
    |refactor   |2      |2        |=          |
    +-----------+-------+---------+-----------+
    |warning    |3      |3        |=          |
    +-----------+-------+---------+-----------+
    |error      |2      |2        |=          |
    +-----------+-------+---------+-----------+



    Messages
    --------

    +-----------+------------+
    |message id |occurrences |
    +===========+============+
    |C0111      |5           |
    +-----------+------------+
    |C0103      |3           |
    +-----------+------------+
    |R0201      |2           |
    +-----------+------------+
    |F0401      |2           |
    +-----------+------------+
    |E1101      |2           |
    +-----------+------------+
    |C0301      |2           |
    +-----------+------------+
    |W0703      |1           |
    +-----------+------------+
    |W0612      |1           |
    +-----------+------------+
    |W0232      |1           |
    +-----------+------------+



    Global evaluation
    -----------------
    Your code has been rated at 2.86/10 (previous run: 3.06/10)

    Statistics by type
    ------------------

    +---------+-------+-----------+-----------+------------+---------+
    |type     |number |old number |difference |%documented |%badname |
    +=========+=======+===========+===========+============+=========+
    |module   |1      |1          |=          |0.00        |0.00     |
    +---------+-------+-----------+-----------+------------+---------+
    |class    |1      |1          |=          |0.00        |0.00     |
    +---------+-------+-----------+-----------+------------+---------+
    |method   |3      |3          |=          |0.00        |0.00     |
    +---------+-------+-----------+-----------+------------+---------+
    |function |0      |0          |=          |0           |0        |
    +---------+-------+-----------+-----------+------------+---------+