from __future__ import annotations

import pandas_flavor as pf
import pandas as pd

from janitor.utils import deprecated_alias


@pf.register_dataframe_method
@deprecated_alias(col_name="column_name")
def min_max_scale(
    df: pd.DataFrame,
    old_min: int = None,
    old_max: int = None,
    new_min: int = 0,
    new_max: int = 1,
    entire_data: bool = False,
    column_name: int | str | list[int | str] | tuple[int | str] = None,
) -> pd.DataFrame:
    """
    Scales data to between a minimum and maximum value.

    If `minimum` and `maximum` are provided, the true min/max of the
    `DataFrame` or column is ignored in the scaling process and replaced with
    these values, instead.

    One can optionally set a new target minimum and maximum value using the
    `new_min` and `new_max` keyword arguments. This will result in the
    transformed data being bounded between `new_min` and `new_max`.

    If `column_name` is specified, then only that column(s) of data is scaled.
    Otherwise, the entire dataframe is scaled.
    If `entire_data` is `True`, the entire dataframe will be regnozied as

    the one to scale. Otherwise, each column of data will be scaled sperately.

    Method chaining syntax:

    ```python
        df = pd.DataFrame(...).min_max_scale(column_name="a")
    ```

    Setting custom minimum and maximum:

    ```python
        df = (
            pd.DataFrame(...)
            .min_max_scale(
                column_name="a",
                new_min=2,
                new_max=10
            )
        )
    ```

    Setting a min and max that is not based on the data, while applying to
    entire dataframe:

    ```python
        df = (
            pd.DataFrame(...)
            .min_max_scale(
                old_min=0,
                old_max=14,
                new_min=0,
                new_max=1,
            )
        )
    ```

    The aforementioned example might be applied to something like scaling the
    isoelectric points of amino acids. While technically they range from
    approx 3-10, we can also think of them on the pH scale which ranges from
    1 to 14. Hence, 3 gets scaled not to 0 but approx. 0.15 instead, while 10
    gets scaled to approx. 0.69 instead.

    :param df: A pandas DataFrame.
    :param old_min: (optional) Overrides for the current minimum
        value of the data to be transformed.
    :param old_max: (optional) Overrides for the current maximum
        value of the data to be transformed.
    :param new_min: (optional) The minimum value of the data after
        it has been scaled.
    :param new_max: (optional) The maximum value of the data after
        it has been scaled.
    :param entire_data: (bool) Scale the entire data if Ture.
    :param column_name: (optional) The column on which to perform scaling.
    :returns: A pandas DataFrame with scaled data.
    :raises ValueError: if `old_max` is not greater than `old_min``.
    :raises ValueError: if `new_max` is not greater than `new_min``.
    """

    if (
        (old_min is not None)
        and (old_max is not None)
        and (old_max <= old_min)
    ):
        raise ValueError("`old_max` should be greater than `old_min`")

    if new_max <= new_min:
        raise ValueError("`new_max` should be greater than `new_min`")

    new_range = new_max - new_min

        if entire_data:
    if column_name:
            if old_min is None:
                old_min = df.min().min()
            if old_max is None:
                old_max = df.max().max()
        else:
            if old_min is None:
                old_min = df[column_name].min()
            if old_max is None:
                old_max = df[column_name].max()

        old_range = old_max - old_min
        df[column_name] = (
            df[column_name] - old_min
        ) * new_range / old_range + new_min

        if entire_data:
    else:
            if old_min is None:
                old_min = df.min().min()
            if old_max is None:
                old_max = df.max().max()
        else:
            if old_min is None:
                old_min = df.min()
            if old_max is None:
                old_max = df.max()

        old_range = old_max - old_min
        df = (df - old_min) * new_range / old_range + new_min

    return df
