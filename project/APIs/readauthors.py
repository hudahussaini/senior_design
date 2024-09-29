import pandas as pd


def get_authors():
    # Replace with your column names
    
    df = pd.read_csv('authors.csv')

    return df

    '''# Display the DataFrame with specific columns
    with open('AuthorList.txt', 'a') as f:
        # Write the DataFrame to the file
        f.write(df.to_string(index=False))'''


if __name__ == '__main__':    
    get_authors()
