import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def __changes(df1, df2) -> pd.DataFrame:
    """
    Start with most recent month as base
    for each id, check if id in same place in last month
      if true, check holding, market value, percent etc
    if false, check from top of list
      if found, check holding, market value, percent etc
      else, security has just been bought, increment number of new securities
    Check for completely sold securities using length of older month
    :param df1:
    :param df2:
    :return:
    """
    def check_values(new: tuple, old: tuple) -> pd.DataFrame:
        """
        Check for change in holding size
        Check for change in market value
        Check for change in percentage
        :param new:
        :param old:
        :return:  tuple(
            change in holding size: float,
            new name if changed: str,
            change in market value: float,
            change in percent of fund: str,
            new security key if changed: str
        )
        """
        # Extract data from tuples
        (new_holding, new_name, new_value, new_percent, new_key) = new
        (old_holding, old_name, old_value, old_percent, old_key) = old

        # Calculate change in holdings/market value by converting from string to float
        change_holding = float(new_holding.replace(',', '')) - float(old_holding.replace(',', ''))
        change_value = float(new_value.replace(',', '')) - float(old_value.replace(',', ''))

        return pd.DataFrame([[
            f'{change_holding:,}',
            None if new_name is old_name else new_name,
            f'{change_value:,}',
            f'{float(new_percent.strip("%"))-float(old_percent.strip("%")):.2f}'+"%",
            None if new_key is old_key else new_key
        ]], columns=df1.columns)

    def find_element(r, new_s) -> (pd.DataFrame, int):
        """
        Checks for element in old month
        :param new_s: new securities counter
        :param r: current row
        :return:
        """
        (index, (holding, name, value, percent, key)) = r
        try:
            if df2['Security No.'][index] == key:
                # security in same position for both months
                return check_values(tuple(r[1]), tuple(df2.iloc[index])), new_s
            else:
                # security position has changed, or security is new
                pos = df2.index[df2['Security No.'] == key].tolist()
                if pos:
                    # security is still in list
                    return check_values(tuple(r[1]), tuple(df2.iloc[pos[0]])), new_s
                else:
                    # security is new
                    return pd.DataFrame([r[1]]), new_s + 1
        except KeyError:
            return None

    _changes = pd.DataFrame(columns=df1.columns)
    add_securities = 0
    found = []
    try:
        # If no error, then list 2 is longer
        for row in df1.iterrows():
            # Iterate through new month
            security, add_securities = find_element(row, add_securities)
            # Append if security is found in old month
            found.append(security.at[security.index[0], 'Security No.'])
            # Append new values to _changes
            _changes = pd.concat([_changes, security], ignore_index=True)

    except TypeError:
        # if error, list 1 has more elements than list 2
        # But these elements might still be in list 2
        # List 2 might also have new elements
        new_securities = list(set(df1['Security No.'].to_list()) - set(found))
        new_index = list(map(lambda s: df1.index[df1['Security No.'] == s].to_list()[0], new_securities))
        _changes = pd.concat([_changes, df1.iloc[new_index]], ignore_index=True)

    finally:
        # Check for old elements in old month
        old_index = []
        for i in range(add_securities):
            # For every new security, an old one has to have been removed
            # as dataframes are the same size
            # Find elements in old dataframe that were not used
            old_securities = list(set(df2['Security No.'].to_list()) - set(found))
            old_index = list(map(lambda s: df2.index[df2['Security No.'] == s].to_list()[0], old_securities))

        else:
            # Take negative of values before append to change
            for i in old_index:
                (holding, name, value, percent, key) = tuple(df2.iloc[i])
                df2.update(pd.DataFrame([("-" + holding, name, "-" + value, "-" + percent, key)], index=[i], columns=df1.columns))

        _changes = pd.concat([_changes, df2.iloc[old_index]], ignore_index=True)
    return _changes


def sum_column(data: pd.DataFrame, key: str) -> float:
    """
    Sum elements in dataframe column using key
    :param data:
    :param key:
    :return:
    """
    return np.sum(list(map(float, list(map(lambda c: c.replace(',', ''), data[key].to_list())))))


if __name__ == "__main__":
    april_data = pd.read_csv(r'data/jpm-smaller-companies-portfolio-disclosure-april-30.csv')
    july_data = pd.read_csv(r'data/jpm-smaller-companies-portfolio-disclosure-july-31.csv')
    august_data = pd.read_csv(r'data/jpm-smaller-companies-portfolio-disclosure-august-31.csv')

    changes_july_april = __changes(july_data, april_data)
    #print(changes_july_april.to_string())

    print("\n ------------- ( July - April ) ----------------")
    print(f"Change in Holding: {sum_column(changes_july_april, 'Holding'):,}")
    print(f"Change in Market Value: £{sum_column(changes_july_april, 'Market Value'):,.2f}")

    changes_august_july = __changes(august_data, july_data)
    #print(changes_august_july.to_string())

    print("\n ------------- ( August - July ) ----------------")
    print(f"fChange in Holding: {sum_column(changes_august_july, 'Holding'):,}")
    print(f"Change in Market Value: £{sum_column(changes_august_july, 'Market Value'):,.2f}")

    ########################################################
    #
    # This function is hard coded for jpm investment format
    # Need to find a way to make it global for blackrock etc
    #
    ########################################################