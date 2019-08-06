from datetime import timedelta
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Input:
    User should input the name of the city and the filters.
    Invalid inputs will prompt the user to try again.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_dict = {'c': 'chicago',
                 'n': 'new york city',
                 'w': 'washington'}
    while True:
        # interpret user input based on the first letter (to allow for abbreviations)
        try:
            first_letter = input('Would you like to explore data from Chicago, New York, or Washington?\n')[0].lower()
            city = city_dict[first_letter]
            print('You will now be shown data from ' + city.title() + '. If you do not want to explore the data from this city, please restart the program now!')
            print('\n')
            break
        # if user input is blank
        except IndexError:
            print('It appears you did not give an answer! Please try again.')
            print('\n')
        # if first letter of the user input is not c (Chicago), n (New York) or w (Washington)
        except KeyError:
            print('Sorry, the program could not interpret your answer! Please try again.')
            print('\n')

    # get user input for day and month
    day, month = 'all', 'all' # default values if no filter is selected

    day_dict = {'m': 'monday',
                'tu': 'tuesday',
                'w': 'wednesday',
                'th': 'thursday',
                'f': 'friday',
                'sa': 'saturday',
                'su': 'sunday',
                '0': 'monday',
                '1': 'tuesday',
                '2': 'wednesday',
                '3': 'thursday',
                '4': 'friday',
                '5': 'saturday',
                '6': 'sunday'}

    month_dict = {'jan': 'january',
                  'feb': 'february',
                  'mar': 'march',
                  'apr': 'april',
                  'may': 'may',
                  'jun': 'june'}

    while True:
        filter = input('Would you like to filter the data by day, month, both, or not at all?\nPlease give one of the following answers: \'day\', \'month\', \'both\', or \'none\'.\n').lower()
        print('\n')

        # interpret user input for day based on first 2 characters (to allow for abbreviations)
        if filter in ['day', 'both']:
            while True:
                try:
                    day_key = input('Which day of the week?\nYou can input either the name of the day (e.g. \'Monday\', \'Mon\', or \'M\')\nor give an integer (Mon = 0, ..., Sun = 6)\n')[:2].lower()
                    print('\n')
                    # Tuesday, Thursday, Saturday, Sunday
                    if day_key[0] in ['t', 's']:
                        day = day_dict[day_key]
                    # for all other days, the first character is the key
                    else:
                        day = day_dict[day_key[0]]
                    print('You will now be shown data from ' + day.title() + '. If you do not want to explore the data from this day, please restart the program now!')
                    print('\n')
                    break
                # if user input is blank
                except SyntaxError:
                    print('It appears you did not give an answer! Please try again.')
                    print('\n')
                # if the initial characters of the user input do not give a valid key for the dictionary
                except KeyError:
                    print('Sorry, the program could not interpret your answer! Please try again.')
                    print('\n')
            if filter == 'day':
                break # if filter == both, we need the month to be selected


        if filter in ['month', 'both']:
            while True:
                try:
                    month_abb = input('Which month of the year?\nJanuary, February, March, April, May, or June?\n')[:3].lower()
                    month = month_dict[month_abb]
                    print('You will now be shown data from ' + month.title() + '. If you do not want to explore the data from this month, please restart the program now!')
                    print('\n')
                    break
                # if user input is blank
                except SyntaxError:
                    print('It appears you did not give an answer! Please try again.')
                    print('\n')
                # if the initial characters of the user input do not give a valid key for the dictionary
                except KeyError:
                    print('Sorry, the program could not interpret your answer! Please try again.')
                    print('\n')
            break

        if filter == 'none':
            break
        else:
            print('Sorry, the program could not interpret your answer! Please try again.')
            print('\n')

    print('-'*40)
    return (city, month, day)


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

    # load data file into pandas dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the start and end time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['Start Time'])

    # filter by month if applicable
    df['month'] = df['Start Time'].dt.month_name()
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def display(df):
    """Display 5 rows of a dataframe at a time"""
    row = 0
    while True:
        try:
            display = input('Would you like to see 5 lines of the data set?\n Please answer \'yes\' or \'no\'.\n')[0].lower()
            if display == 'y':
                print(df.iloc[row:row+5])
                row += 5
            elif display == 'n':
                break
        # if user input is blank
        except IndexError:
            print('It appears you did not give an answer! Please try again.')
            print('\n')
        else:
            print('Sorry, the program could not interpret your answer! Please try again.')
            print('\n')


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        print('In ' + city.title() + ':')
        print('Given the filter \'day=' + day + '\':')
        popular_month = df['month'].mode()[0]
        print('The most common month was {}.'.format(popular_month))
        month_counts = df['month'].value_counts()
        print('The number of bike rides for each month, in descending order, is given below:')
        print(month_counts)

    # display the most common day of week
    if day == 'all':
        print('In ' + city.title() + ':')
        print('Given the filter \'month=' + month + '\':')
        popular_day = df['day_of_week'].mode()[0]
        print('The most common day was {}.'.format(popular_day))
        day_counts = df['day_of_week'].value_counts()
        print('The number of bike rides for each day, in descending order, is given below:')
        print(day_counts)

    # display the most common start hour
    df['start hour'] = df['Start Time'].dt.hour # create start hour column

    print('In ' + city.title() + ':')
    print('Given the filters \'day={}\' and \'month={}\':'.format(day, month))
    popular_hour = df['start hour'].mode()[0]
    print('The most common start hour was {}:00 - {}:59.'.format(popular_hour, popular_hour))
    hour_counts = df['start hour'].value_counts()
    print('The number of bike rides for each hour, in descending order, is given below:')
    print(hour_counts)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, city, month, day):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('In ' + city.title() + ':')
    print('Given the filters \'day={}\' and \'month={}\':'.format(day, month))
    popular_station = df['Start Station'].mode()[0]
    print('The most common start station was {}.'.format(popular_station))

    # display most commonly used end station
    print('In ' + city.title() + ':')
    print('Given the filters \'day={}\' and \'month={}\':'.format(day, month))
    popular_station = df['End Station'].mode()[0]
    print('The most common end station was {}.'.format(popular_station))

    # display most frequent combination of start station and end station trip
    df['Journey'] = df['Start Station'] + ' : ' + df['End Station'] # start and end stations glued together

    print('In ' + city.title() + ':')
    print('Given the filters \'day={}\' and \'month={}\':'.format(day, month))
    popular_journey = df['Journey'].mode()[0]
    print('The most common journey was {} to {}.'.format(popular_journey.split(' : ')[0], popular_journey.split(' : ')[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, city, month, day):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('In ' + city.title() + ':')
    print('Given the filters \'day={}\' and \'month={}\':'.format(day, month))
    total_travel_time = sum(df['Trip Duration']) # in seconds
    print('The total travel time was', timedelta(seconds=total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() # in seconds
    print('The mean travel time was', timedelta(seconds=mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, month, day):
    """
    Displays statistics on bikeshare users.

    Results are limited for Washington.
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('In ' + city.title() + ':')
    print('Given the filters \'day={}\' and \'month={}\':'.format(day, month))
    # Display counts of user types
    print(df['User Type'].value_counts())

    # gender and birth year are not available for Washington
    if city != 'washington':
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        print('The earliest year of birth was {}'.format(earliest))
        recent = df['Birth Year'].max()
        print('The most recent year of birth was {}'.format(recent))
        common = df['Birth Year'].mode()[0]
        print('The most common year of birth was {}'.format(common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        (city, month, day) = get_filters()
        df = load_data(city, month, day)

        display(df)

        time_stats(df, city, month, day)
        station_stats(df, city, month, day)
        trip_duration_stats(df, city, month, day)
        user_stats(df, city, month, day)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
