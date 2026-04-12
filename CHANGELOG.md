CHANGELOG
Latest Version: 1.1.0
=====================

Version 1.1.1 (4/11/2026)
-------------------------
    - Changed generateRandomNumber to take in 3 arguments
    - Price options function changed:
        -- Added argument 'plot' which as a boolean
        -- The multiple paths are plotted if 'plot' is true
        -- Added for loop to esnure path plotting works
        -- Imported matplotlib
        -- y-value is the stock price
        -- x price is the time (e.g., the x-value for .2 would be 2.4 months into maturity)
    - Created backtesting engine file
    - Made data colleciton and validation for backtesting engine
    - Notes/Goals:
        -- Finish backesting engine

Version 1.1.0 (4/10/2026)
-------------------------
    - Added monteCarloSimulations class, and functions to execute simulations
    - Set functions to static
    - Latest version added to change log
    - Changed 'Print' function argument to 'verbose'
    - Added blackScholes class, and function to execute pricing
    - Updated TOML file
    - Test file runs all methods in one file and reports back if they work
    - Fixed ADX logic
    - Added calculate greeks class, and functions to claculate the greeks
    - Notes/Goals:
        -- Add anti-variance Monte Carlo class
        -- Make a data set intake Monte Carlo class
        -- Make a data set intake Black Scholes class
        -- Change documentation website

Version 1.0.1 (4/10/2026)
-------------------------
    - Added test files to ensure scripts work
    - Base package replaced
    - Code pushed to GIT

Version 1.0.0 (4/9/2026)
------------------------
    - Documentation text file created
    - Functions and classes created
    - License file created
    - Documentation site created
    - TOML file created
    - README created
    - Summary: Base setup for packagin completed
    - Notes/Goals:
        -- Base package published (take down ASAP) (V 0.1.0)
        -- Website should be expanded for github links