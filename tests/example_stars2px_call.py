#############
## LOGGING ##
#############

import logging
from astrobase import log_sub, log_fmt, log_date_fmt

DEBUG = False
if DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO
LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    level=level,
    style=log_sub,
    format=log_fmt,
    datefmt=log_date_fmt,
)

LOGDEBUG = LOGGER.debug
LOGINFO = LOGGER.info
LOGWARNING = LOGGER.warning
LOGERROR = LOGGER.error
LOGEXCEPTION = LOGGER.exception

#############
## IMPORTS ##
#############

import numpy as np
from tesspointfork.tess_stars2px import tess_stars2px_function_entry

###########
## TESTS ##
###########

def test_burke(verbose=True):

    # This is an example of using tess_stars2px functionality 
    # from a program rather than the typical command line interface
    # the function example only takes ra and dec [deg] 
    #  Your program should provide these
    #  The other ways of getting coordinates 'TIC MAST query' 'By name' 'file list'
    #  are not supported in the wrapper function.  Just ra and decs
    # Location for pi mensae
    ra = 84.291188
    dec = -80.469119
    ticid = 261136679 # arbitrary convenience tracking integer

    outID, outEclipLong, outEclipLat, outSec, outCam, outCcd, \
    outColPix, outRowPix, scinfo = tess_stars2px_function_entry(
        ticid, ra, dec
    )

    for i in range(len(outID)):
        LOGINFO('{0:d} {1:d} {2:d} {3:d} {4:f} {5:f}'.format(outID[i], outSec[i], \
          outCam[i], outCcd[i], outColPix[i], outRowPix[i]))

    # For efficiency purposes if you save scinfo between calls
    #  you will save time in setting up the the telescope fields
    outID, outEclipLong, outEclipLat, outSec, outCam, outCcd, \
    outColPix, outRowPix, scinfo = tess_stars2px_function_entry(
        ticid, ra, dec, scInfo=scinfo
    )
    LOGINFO('Faster to re-use scinfo in repeated calls')
    for i in range(len(outID)):
        LOGINFO('{0:d} {1:d} {2:d} {3:d} {4:f} {5:f}'.format(outID[i], outSec[i], \
          outCam[i], outCcd[i], outColPix[i], outRowPix[i]))

    LOGINFO('Also accepts multiple targets')
    ra = np.array([219.90085,10.897379], dtype=np.float)
    dec = np.array([-60.835619,-17.986606], dtype=np.float)
    ticid = np.array([0,1], dtype=np.int)
    outID, outEclipLong, outEclipLat, outSec, outCam, outCcd, \
            outColPix, outRowPix, scinfo = tess_stars2px_function_entry(
                    ticid, ra, dec, scInfo=scinfo
    )
    for i in range(len(outID)):
        LOGINFO('{0:d} {1:d} {2:d} {3:d} {4:f} {5:f}'.format(outID[i], outSec[i], \
          outCam[i], outCcd[i], outColPix[i], outRowPix[i]))

    LOGINFO('test_burke passed.')


def test_default():

    rng = np.random.default_rng(42)

    # NOTE: this isn't uniform sampling of a sphere; it's just for checking how
    # long tess-point takes.
    N = 1000
    ra = rng.uniform(low=0, high=360, size=N)
    dec = rng.uniform(low=-90, high=90, size=N)
    ticid = np.arange(0,N)

    LOGINFO(79*'.')
    LOGINFO(f'Begin default test of N={N} tess_stars2px_function_entry calls')
    outID, outEclipLong, outEclipLat, outSec, outCam, outCcd, \
            outColPix, outRowPix, scinfo = tess_stars2px_function_entry(
                    ticid, ra, dec
    )
    LOGINFO(f'End default test of N={N} tess_stars2px_function_entry calls')
    LOGINFO(79*'.')

    LOGINFO(f'test_default passed, with {len(outSec)} hits.')


def test_custom_opstable():

    ops_table_path = (
        '/Users/luke/Dropbox/proj/extend_tess/data/20211013_vanderspek_EM2/Y1-7_ops.tbl'
    )
    sector_interval = (1,100)

    rng = np.random.default_rng(42)

    # NOTE: this isn't uniform sampling of a sphere; it's just for checking how
    # long tess-point takes.
    N = 1000
    ra = rng.uniform(low=0, high=360, size=N)
    dec = rng.uniform(low=-90, high=90, size=N)
    ticid = np.arange(0,N)

    LOGINFO(79*'.')
    LOGINFO(f'Begin test_custom_opstable of N={N} tess_stars2px_function_entry calls')
    outID, outEclipLong, outEclipLat, outSec, outCam, outCcd, \
            outColPix, outRowPix, scinfo = tess_stars2px_function_entry(
                ticid, ra, dec, ops_table_path=ops_table_path,
                sector_interval= sector_interval
    )
    LOGINFO(f'End test_custom_opstable of N={N} tess_stars2px_function_entry calls')
    LOGINFO(79*'.')

    LOGINFO(f'test_default passed, with {len(outSec)} hits.')



if __name__ == '__main__':

    test_custom_opstable()

    test_default()

    #test_burke(verbose=False)
