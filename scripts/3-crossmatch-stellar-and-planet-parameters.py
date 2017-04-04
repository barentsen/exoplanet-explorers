"""Read the summary table of Exoplanet Explorer classifications and crossmatch
against stellar parameters (from Huber) and planet fit parameters (from Ian).
"""
import pandas as pd
from astropy import units as u
import numpy as np


OUTPUT_FN = '../output/summary-with-parameters.csv'


if __name__ == '__main__':
    summary_real = pd.read_csv('../output/summary-real-candidates.csv', dtype={'candidatename': str, 'epic': str})

    # Add planet fit parameters
    signals = pd.read_csv('../data/real-signals-without-duplicates.csv', dtype={'candidatename': str})
    summary_with_signals = summary_real.merge(signals, on='candidatename', how='left')

    # Add stellar parameters
    params = pd.read_csv('../data/stellar-parameters.csv', sep='|', dtype={'epic': str})
    params['epic'] = params.epic.str.strip()
    summary_with_parameters = summary_with_signals.merge(params, on='epic', how='left')

    # Estimate planet radius from transit depth from the planet fit and stellar radius from Huber
    summary_with_parameters['Rearth'] = (summary_with_parameters['fit_rprs'] * summary_with_parameters['Rad']).values*u.Rsun.to(u.Rearth)
    # Estimate semi-major axis from Kepler's third law
    a = (((summary_with_parameters['fit_P'] / 365.)**2) * (summary_with_parameters['Mass']))**(1 / 3.)
    summary_with_parameters['a'] = a
    # Estimate stellar luminosity
    luminosity = (summary_with_parameters['Rad']**2) * ((summary_with_parameters['Teff'] / 5780)**4)
    summary_with_parameters['luminosity'] = luminosity
    # In Habitable Zone?
    # This uses a rough HZ definition following http://exoplanetarchive.ipac.caltech.edu/docs/poet_calculations.html
    summary_with_parameters['in_hz'] = ((a > (0.75*np.sqrt(luminosity))) & (a < (1.77*np.sqrt(luminosity))))

    # Write results to table
    summary_with_parameters.to_csv(OUTPUT_FN)
