import pytest


@pytest.mark.functions
def test_min_max_scale(dataframe):
    df = dataframe.min_max_scale(column_name="a")
    assert df["a"].min() == 0
    assert df["a"].max() == 1


@pytest.mark.functions
def test_min_max_scale_custom_new_min_max(dataframe):
    df = dataframe.min_max_scale(column_name="a", new_min=1, new_max=2)
    assert df["a"].min() == 1
    assert df["a"].max() == 2


@pytest.mark.functions
def test_min_max_old_min_max_errors(dataframe):
    with pytest.raises(ValueError):
        dataframe.min_max_scale(column_name="a", old_min=10, old_max=0)


@pytest.mark.functions
def test_min_max_new_min_max_errors(dataframe):
    with pytest.raises(ValueError):
        dataframe.min_max_scale(column_name="a", new_min=10, new_max=0)


@pytest.mark.parametrize(
    "df, excepted, entire_data, column_name",
    [
        (
            pd.DataFrame({"a": [1, 2], "b": [0, 1]}),
            pd.DataFrame({"a": [0.5, 1], "b": [0, 0.5]}),
            True,
            None,
        ),
        (
            pd.DataFrame({"a": [1, 2], "b": [0, 1]}),
            pd.DataFrame({"a": [0, 1], "b": [0, 1]}),
            False,
            None,
        ),
        (
            pd.DataFrame({"a": [1, 2], "b": [0, 1], c: [0, 0]}),
            pd.DataFrame({"a": [0.5, 1], "b": [0, 0.5]}),
            True,
            ["a", "b"],
        ),
        (
            pd.DataFrame({"a": [1, 2], "b": [0, 1], c: [0, 0]}),
            pd.DataFrame({"a": [0, 1], "b": [0, 1]}),
            False,
            ["a", "b"],
        ),
    ],
)
def test_min_max_scale_entire_data(df, excepted, entire_data, column_name):
    result = df.min_max_scale(
        entire_data=entire_data,
        column_name=column_name,
    )

    assert result.equals(excepted)
