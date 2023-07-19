import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_prompt(prompt, options):
    """Compares the input with a validated list of options"""
    while True:
        user_prompt = input(prompt).lower()
        if user_prompt in options:
            return user_prompt
        else:
            print('n/That is not a valid option. Please, choose from: {", ".join(options)}')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city_options = ['chicago', 'new york city', 'washington']
    month_options = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    day_options = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
	
	print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_prompt("Please, type one of three options: chicago, new york city, washington: ", city_options)

    # TO DO: get user input for month (all, january, february, ... , june)
    month = get_prompt("Please, type the name of the required month (from january to june, or type 'all' if you want to see all): ", month_options)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_prompt("Please, type the day of the week: ", day_options)

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    if month != 'all':
        df = df[df['month'] == month.title()]
    if day != 'all':
        df = df[df['day'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].value_counts().keys()[0]
    print('The most common month was: {}'.format(common_month))
    

    # TO DO: display the most common day of week
    common_day = df['day'].value_counts().keys()[0]
    print('The most common day of week was: {}'.format(common_day))

    # TO DO: display the most common start hour
    common_start = df['hour'].value_counts().keys()[0]
    print('The most common start hour was: {}'.format(common_start))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_st = df['Start Station'].value_counts().keys()[0]
    print('The most commonly used start station was: {}'.format(common_start_st))
    
    # TO DO: display most commonly used end station
    common_end_st = df['End Station'].value_counts().keys()[0]
    print('The most commonly used end station was {}'.format(common_end_st))
    
    # TO DO: display most frequent combination of start station and end station trip
    df['Start_End_Station'] = 'Start Station = ' + df['Start Station'] + ';\nEnd Station = ' + df['End Station']
    combi_station = df['Start_End_Station'].value_counts().keys()[0]
    print('The most frequent combination of start station and end station was:\n{}'.format(combi_station))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time_min = int(df['Trip Duration'].sum() // 60)
    total_time_sec = int(round(df['Trip Duration'].sum() % 60))
    print('The total travel time was: {} minutes and {} seconds'.format(total_time_min, total_time_sec))
    
    # TO DO: display mean travel time
    mean_time_min = int(df['Trip Duration'].mean() // 60)
    mean_time_sec = int(round(df['Trip Duration'].mean() % 60))
    print('The mean travel time was: {} minutes and {} seconds'.format(mean_time_min, mean_time_sec))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('Calculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('These are the user types and their frequency: ')
    print(df['User Type'].value_counts().to_string())

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print('\nThese are the Gender of users and their frequency: ')
        print(df['Gender'].value_counts().to_string())
    else:
        print('\nSorry, there is no information on the gender of users for this city')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth = int(df['Birth Year'].min())
        latest_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode())
        print('\nThe earliest year of birth was {}, the most recent was {} and the most common was {}'.format(earliest_birth, latest_birth, common_birth))
    else:
        print("\nSorry, there is no information on the user\'s birth year for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw data from the dataframe"""
    print('\nYou have just seen all the statistics from the data.')
    display = input('\nDo you now want to see 5 lines of raw data from the data frame? Enter yes or no.\n').lower()
    start = 0
    end = 5
    while display == 'yes':
		if end >= len(df):
            print("\nSorry, no more data to show.")
			break
		else:
			print(tabulate(df.iloc[start : end], headers = 'keys', tablefmt = 'psql'))
			start += 5
			end += 5
			display = input('\nDo you want to see 5 more lines of raw data? Enter yes or no.\n').lower()
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
