import numpy as np
import pandas as pd
import scipy.stats as stats


x_input = [1.6, 4, 20, 40, 80]
y_input = [3.0654E-05, 7.50436E-05, 9.8309E-05, 0.000478644, 0.002098848]


def linest(x_arg, y_arg):
    x = np.array(x_arg)
    y = np.array(y_arg)
    n = len(x)

    # Regression analysis
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    y_predicted = slope * x + intercept
    residuals = y - y_predicted

    # Deg of freedom
    deg_freedom = n - 2

    # Sum of squares
    ss_total = np.sum((y - np.mean(y)) ** 2)
    ss_res = np.sum(residuals ** 2)
    ss_reg = ss_total - ss_res

    # SEE (Standard error of y estimate)
    see = np.sqrt(ss_res / deg_freedom)

    # Manual Std Error of Intercept
    denominator = np.sum((x - np.mean(x)) ** 2)
    se_intercept = (
        see * np.sqrt(np.sum(x ** 2) / (n * denominator)) if denominator != 0 else np.nan
    )

    # F-statistic
    ms_reg = ss_reg / 1
    ms_res = ss_res / deg_freedom
    f_stat = ms_reg / ms_res

    # Create dataframe
    output = np.array([
        [slope, intercept],
        [std_err, se_intercept],
        [r_value ** 2, see],
        [f_stat, deg_freedom],
        [ss_reg, ss_res]
    ])
    linest_df = pd.DataFrame(
        output,
        index=["slope/intercept", "stderr", "R2/SEE", "F/df", "SSR/SSE"],
        columns=["Col1 (slope)", "Col2 (intercept)"]
    )

    return linest_df.round(8)

print(linest(x_input, y_input))