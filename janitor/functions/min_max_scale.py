from __future__ import annotations

import pandas_flavor as pf
import pandas as pd

from janitor.utils import deprecated_alias


@pf.register_dataframe_method
@deprecated_alias(col_name="column_name")
def min_max_scale(
    df: pd.DataFrame,
    feature_range: tuple[int | float, int | float] = (0, 1),
    column_name: int | str | list[int | str] | tuple[int | str] = None,
    entire_data: bool = False,
) -> pd.DataFrame:
    """
    Scales data to between a minimum and maximum value.

    If `minimum` and `maximum` are provided, the true min/max of the
    `DataFrame` or column is ignored in the scaling process and replaced with
    these values, instead.

    One can optionally set a new target minimum and maximum value using the
    `feature_range[0]` and `feature_range[1]` keyword arguments.
    This will result in the transformed data being bounded between
    `feature_range[0]` and `feature_range[1]`.

    If `column_name` is specified, then only that column(s) of data is scaled.
    Otherwise, the entire dataframe is scaled. If `entire_data` is `True`,
    the entire dataframe will be regnozied as the one to scale. Otherwise,
    each column of data will be scaled sperately.

    Method chaining syntax:

    ```python
        df = pd.DataFrame(...).min_max_scale(column_name="a")
    ```

    Setting custom minimum and maximum:

    ```python
        df = (
            pd.DataFrame(...)
            .min_max_scale(
                feature_range=(2, 10),
                column_name="a",
            )
        )
    ```

    Setting a min and max that is not based on the data, while applying to
    entire dataframe:

    ```python
        df = (
            pd.DataFrame(...)
            .min_max_scale()
        )
    ```

    The aforementioned example might be applied to something like scaling the
    isoelectric points of amino acids. While technically they range from
    approx 3-10, we can also think of them on the pH scale which ranges from
    1 to 14. Hence, 3 gets scaled not to 0 but approx. 0.15 instead, while 10
    gets scaled to approx. 0.69 instead.

    :param df: A pandas DataFrame.
    :param feature_range: (optional) Desired range of transformed data.
    :param column_name: (optional) The column on which to perform scaling.
    :param entire_data: (bool) Scale the entire data if Ture.
    :returns: A pandas DataFrame with scaled data.
    :raises ValueError: if `old_max` is not greater than `old_min``.
    :raises ValueError: if `feature_range[1]` is not greater than `feature_range[0]``.
    """

    if feature_range[1] <= feature_range[0]:
        raise ValueError(
            "`feature_range[1]` should be greater than `feature_range[0]`"
        )

    new_min, new_max = feature_range[0], feature_range[1]
    new_range = new_max - new_min

    if column_name:
        if entire_data:
            old_min = df[column_name].min().min()
            old_max = df[column_name].max().max()
        else:
            old_min = df[column_name].min()
            old_max = df[column_name].max()

        old_range = old_max - old_min
        df[column_name] = (
            df[column_name] - old_min
        ) * new_range / old_range + new_min

    else:
        if entire_data:
            old_min = df.min().min()
            old_max = df.max().max()
        else:
            old_min = df.min()
            old_max = df.max()

        old_range = old_max - old_min
        df = (df - old_min) * new_range / old_range + new_min

    return df
