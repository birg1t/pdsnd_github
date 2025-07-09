import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS_LIST = ['january', 'february', 'march', 'april', 'may', 'june','all']
DAYS_LIST = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        try:
            city_input = str(input("\nPlease insert the city name you want to see statistics of!\nChoose between Chicago, New York City or Washington:\n").lower())
            if city_input in CITY_DATA:
                city=city_input
                break 
            else:
                print( "\nLooks like this city is not in the list")
        except:
            print("\nThis is not a valid input for a city")
# TO DO: get user input for month (all, january, february, ... , june)
    while True:    
        try: 
            month_input = str(input("\nWhich month do you want to filter by?\nChoose a month between January and June. If you want to se all months, please answer with all:\n").lower())
            if month_input in MONTHS_LIST:
                month = month_input
                break
            else:
                print("\nLooks like this month is not in the list")
        except:
            print("\nThis is not a valid input for a Month")
#get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day_input = str(input("\nPlease insert a day of the week. E.g. Monday, Tuesday... or all:\n").lower())
            if day_input in DAYS_LIST:
                day = day_input
                break
            else:
                print("Looks like you didn't choose a correct input for a day.\n")
        except:
            print("This is not a valid input for a day.")

    print('-'*40)
    return city, month, day
    

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #displays the most common month
    print("The most common Month is: ",df["month"].mode()[0])

    # displays the most common day of week
    print("The most common day of the week is: ",df["day_of_week"].mode()[0])

    #displays the most common start hour
    print("Most common start hour is : ", df["Start Time"].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displays the most commonly used start station
    print("The most commonly used start station is:  ",df["Start Station"].mode()[0])

    # displays the most commonly used end station
    print("The most commonly used end station is:  ",df["End Station"].mode()[0])

    #displays the most frequent combination of start station and end station trip
    df["start_and_end"]= df["Start Station"]+" and " + df["End Station"]
    print("The most commonly used start and end station combination is:\n  ",df["start_and_end"].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    mean_trip_duration= int(df["Trip Duration"].mean())
    total_travel_time = int(df["Trip Duration"].sum())
    
    # displays the total travel time
    print("The total travel time was %s hh:mm:ss.ms " % datetime.timedelta(seconds=total_travel_time))

    #displays the mean travel time
    print("The mean travel time was %s hh:mm:ss.ms" % datetime.timedelta(seconds=mean_trip_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # displays the counts of user types
    print("Counts of user Types: ")
    print(df["User Type"].value_counts())

    # displays counts of gender
    try:
        print("Counts of gender: ")
        print(df["Gender"].value_counts())
    except:
        print("No Information about gender available\n")

    # displays the earliest, most recent, and most common year of birth   
    try:
        print("\nThe earliest, most recent and most common birth years are:")
        print("Earliest ",int(df["Birth Year"].min()))
        print("Most recent ",int(df["Birth Year"].max()))
        print("Most common ", int(df["Birth Year"].mode()[0]))
    except:
        print("No Birth Years can be evaluated")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        # asks user if they want to see raw data from the dataframe
        i=0
        while i < len(df):
            print_df = input('\nWould you like to see values from the dataframe?\nEnter yes or no.\n')
            
            if print_df.lower() != 'yes':
                break
            else:
                print(df.iloc[i:i+5])
                i= i+5
                  
        restart = input('\nWould you like to restart?\nEnter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
