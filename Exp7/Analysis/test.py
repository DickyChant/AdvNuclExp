import os

import numpy as np

from srim import TRIM, Ion, Layer, Target, SR
from srim.output import Results


# Construct a 3MeV Nickel ion

# Construct a layer of nick 20um thick with a displacement energy of 30 eV

Cst = 0.137
Rhost = 2.33 * (1-Cst) + 0.0715 * Cst
Ast = 28 * (1-Cst) + 1 * Cst
Fe = 71 / 100
Cr = 19 / 100
Ni = 10 / 100
Ass = Fe * 56 + Cr * 52 + Ni * 59
Rhoss = 7.93
RhoH = 0.0715
Nst = np.mean([1467,2177,2267,2394,2378])
dedxst = 159.816

def calcC(x,N):
    dedx = calcHatX(x)
    A = x * 1 + (1-x) * Ass
    Rho = x * RhoH + (1-x) * Rhoss
    C = Cst * dedx * N / dedxst / Nst * Rhost / Ast * A / Rho
    # print(x,C)
    return C

def calcHatX(x):
    H = x
    den = Rhoss * (1-x) + RhoH * x
    layer = Layer({
            'Fe': {
                'stoich': Fe  * (1-x),
            },
            'Ni': {
                'stoich': Ni  * (1-x),
            },
            'H': {
                'stoich': x,
            },
            'Cr':{
                'stoich': Cr  * (1-x),
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
    print("HV","N","Deepth","H Percent",sep=',')
    for HVidx,N in enumerate([89,956,1138,1078,750,282,116]):
        C = 0.01
        HV = HVidx * 0.04 + 1.26
        for i in range(10):
            C_update = calcC(C,N)
            if (C-C_update)/C_update <= 0.02:
                dedx = calcHatX(C_update)
                x = (HV*5-6.42)*1000000/dedx
                print(HV,N,x,C_update*100,sep=',')
                break
            else:
                C = C_update
