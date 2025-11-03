# import required libraries
import os
import time 
import warnings
import pandas as pd
from datetime import datetime
warnings.filterwarnings('ignore')
from trading_ig import IGService
from trading_ig.config import config
from zoneinfo import ZoneInfo

class updateData:
    def __init__(self, epic: str):
       self.epic = epic
       self.ig_service = None
    
    def set_connection(self):
        """
        A method that sets up connection to IG API.
        """
        # initialize IG service
        self.ig_service = IGService(
                        config.username,
                        config.password,
                        config.api_key,
                        config.acc_type
                    )

        # login 
        self.ig_service.create_session()
        print("Connected successfully!")

    def transform_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transforms the DataFrame to have separate columns for bid, ask, and last data types.

        Parameters
        ----------
        df: dataframe 

        Returns
        -------
        transformed_df: dataframe which is already transformed 
        """
        # define the new columns for the transformed DataFrame
        columns = ['bid_Open', 'bid_High', 'bid_Low', 'bid_Close',
                   'ask_Open', 'ask_High', 'ask_Low', 'ask_Close',
                   'last_Open', 'last_High', 'last_Low', 'last_Close',
                   'Volume']

        # create a new DataFrame with the desired columns
        transformed_df = pd.DataFrame(index=df.index)

        # extract bid data
        transformed_df['Open'] = df[('bid', 'Open')]
        transformed_df['High'] = df[('bid', 'High')]
        transformed_df['Low'] = df[('bid', 'Low')]
        transformed_df['Close'] = df[('bid', 'Close')]
     
        # extract volume
        transformed_df['Volume'] = df[('last', 'Volume')]

        # return the transofrmed dataframe 
        return transformed_df
    
    def fetch_gold_data(self, existing_csv_path, resolution, date_column = 'Date'):
        """
        Fetch historical gold data from IG with specified resolution and date range.
    
        Parameters
        ----------
        ig_service (IGService): The initialized IGService object.
        resolution (str): The data resolution (e.g., '1Min', '1H', '1D').
        from_date (str): The start date for data retrieval in ISO 8601 format.
        numpoints (int): The maximum number of data points to retrieve.
    
        Returns
        -------
        pandas.DataFrame: A DataFrame containing the historical data.
        """
        
        # check if the file exists
        if not os.path.exists(existing_csv_path):
            print(f"File {existing_csv_path} does not exist. Creating a new file.")
            # create an empty DataFrame with predefined columns
            empty_df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
            empty_df.set_index('Date', inplace = True)
            empty_df.to_csv(existing_csv_path)

        # read existing csv_path to determin start date / time
        existing_data = pd.read_csv(existing_csv_path, parse_dates=[date_column], index_col=date_column)

        # convert to processable string format
        from_date = existing_data.index[-1].strftime('%Y-%m-%dT%H:%M:%S')
        
        # define the epic for gold
        # epic = "CS.D.USCGC.TODAY.IP"  # Example epic for gold (Check IG API for correct epic)

        # get the current date and time
        to_date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        # request historical data
        response = self.ig_service.fetch_historical_prices_by_epic(
            self.epic,
            resolution=resolution,
            start_date=from_date,
            end_date=to_date,
        )

        # convert the response to a DataFrame
        df = response['prices']
        transformed_df = self.transform_dataframe(df)
    
        # retrun the transformed dataframe 
        return transformed_df

    def update_gold_data(self, existing_csv_path, new_data, date_column='Date'):
        """
        Updates the existing gold data CSV file with new data retrieved from the IG API.
    
        Parameters
        ----------
        existing_csv_path: Path to the existing 1-hour CSV file
        new_data: The new data DataFrame retrieved from the IG API
        date_column: The name of the date column (default is 'Date')

        Returns
        -------
        combined_df: combined dataset (old data + new data)
        """
        # check if the file exists
        if not os.path.exists(existing_csv_path):
            print(f"File {existing_csv_path} does not exist. Creating a new file.")
            # create an empty dataframe with predefined columns
            empty_df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
            empty_df.set_index('Date', inpalce = True)
            empty_df.to_csv(existing_csv_path)


        # load the existing 1-hour data CSV file
        existing_data = pd.read_csv(existing_csv_path, parse_dates=[date_column], index_col=date_column)
    
        # convert the 'DateTime' to datetime and set it as the index
        new_data['Date'] = pd.to_datetime(new_data.index)
        new_data.set_index('Date', inplace=True)
    
        # drop any duplicate index entries
        new_data = new_data[~new_data.index.duplicated(keep='first')]
    
        # merge the dataframes
        # Concatenate the new data with the existing data
        combined_data = pd.concat([existing_data, new_data])
    
        # drop any duplicate rows that may exist after concatenation
        combined_data = combined_data[~combined_data.index.duplicated(keep='last')]
    
        # sort the combined data by date to maintain chronological order
        combined_data.sort_index(inplace=True)
    
        # save the Updated CSV
        # Save the combined data back to the CSV file
        # combined_data.to_csv(existing_csv_path)
        return combined_data

    def update_every_minute(self, csv_path, resolution='1Min'):
        """
        A method to update the gold data every minute.

        Parameters
        ----------
        csv_path : str
            Path to the existing CSV file where data is stored.
        resolution : str, optional
            Data resolution for fetching new data (default is '1Min').
        """
        # self.set_connection()  # Ensure the IG connection is active
        
        while True:
            # fetch the latest data from IG API
            new_data = self.fetch_gold_data(existing_csv_path=csv_path, resolution=resolution)
            
            # update the existing CSV file with the new data
            updated_data = self.update_gold_data(existing_csv_path=csv_path, new_data=new_data)
            
             # Save the updated data to the CSV file after each update
            #updated_data.to_csv(csv_path)
            #print("Data saved successfully after 20 minutes.")
            
            # Wait for 20 minutes before the next update
            #time.sleep(1200)

            # save the updated data back to the CSV file
            updated_data.to_csv(csv_path)
            print("Data updated successfully.")
            
            # wait for 5 minute before the next update
            time.sleep(300)


if __name__ == "__main__":
    # instantiate the class
    updateDataHandler = updateData(epic='CS.D.USCGC.TODAY.IP')
    # log in to My IG
    updateDataHandler.set_connection()

    # fetch data from IG API
    root_path = os.getcwd()
    # 1 min data file path (for resample)
    existing_1min_data_path = os.path.join(root_path, 'data\gold_minutely_data.csv')
    # 1 hour data file path
    existing_1hr_data_path = os.path.join(root_path, 'data\gold_hourly_data.csv')
    # 1 day data file path
    existing_1d_data_path = os.path.join(root_path, 'data\gold_daily_data.csv')

    transformed_1m_df = updateDataHandler.fetch_gold_data(
        existing_1min_data_path, resolution="1Min", date_column='Date')
    # print(transformed_1m_df)

    transformed_1hr_df = updateDataHandler.fetch_gold_data(
        existing_1hr_data_path, resolution="1h", date_column='Date')
    # print(transformed_1hr_df)

    transformed_1d_df = updateDataHandler.fetch_gold_data(
        existing_1d_data_path, resolution="1D", date_column='Date')
    # print(transformed_1d_df)

    # update dataset
    updated_1m_df = updateDataHandler.update_gold_data(
        existing_1min_data_path, transformed_1m_df)
    # print(updated_1m_df.tail(5))
    # save to the file
    updated_1m_df.to_csv(existing_1min_data_path)

    updated_1hr_df = updateDataHandler.update_gold_data(
        existing_1hr_data_path, transformed_1hr_df)
    # print(updated_1hr_df.tail(5))
    # save to the file
    updated_1hr_df.to_csv(existing_1hr_data_path)

    updated_1d_df = updateDataHandler.update_gold_data(
        existing_1d_data_path, transformed_1d_df)
    # print(updated_1d_df.tail(5))
    # save to the file
    updated_1d_df.to_csv(existing_1d_data_path)

    updateDataHandler.update_every_minute(csv_path=existing_1min_data_path)
