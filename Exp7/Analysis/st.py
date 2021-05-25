import os

import numpy as np

from srim import TRIM, Ion, Layer, Target, SR
from srim.output import Results


# Construct a 3MeV Nickel ion

# Construct a layer of nick 20um thick with a displacement energy of 30 eV
def calcHatX(x):
    den = 2.33 * (1-x) + 0.0715 * x
    layer = Layer({
           
            'H': {
                'stoich': x,
            },
            'Si':{
                'stoich': (1-x),
            }},density = den , width = 1000000)

    ion = Ion('F', energy=3.0e6)
    # Construct a target of a single layer of Nickel
    target = Target([layer])

    # Initialize a TRIM calculation with given target and ion for 25 ions, quick calculation
    trim = SR(layer, ion,output_type = 1)

    # Specify the directory of SRIM.exe
    # For windows users the path will include C://...
    srim_executable_directory = '/tmp/srim'

    # takes about 10 seconds on my laptop
    results = trim.run(srim_executable_directory)
    # If all went successfull you should have seen a TRIM window popup and run 25 ions!



    srim_executable_directory = '/tmp/srim'
    # results = Results(srim_executable_directory)
    output_directory = '/opt/pysrim/output'
    #os.makedirs(output_directory, exist_ok=True)
    # TRIM.copy_output_files('/tmp/srim', output_directory,check_srim_output=False)
    Se = results.data[1]
    Sn = results.data[2]

    dedx = Se + Sn
    inE = 6.42 * 1000
    test = np.interp(inE,results.data[0],dedx)
    return test

if __name__ == "__main__":
    percent = 0.137
    print(percent,calcHatX(percent))
