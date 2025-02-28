from datetime import datetime

def anonymize_date_grouping(date_str, grouping_type='decade'):
    """
    Anonymizes a date by grouping by decade or quarter.
    
    :param date_str: Date in format 'YYYY-MM-DD'
    :param grouping_type: The type of grouping ('decade' oder 'quarter')
    :return: Anonymized and grouped date in the format 'YYYY-MM-DD'
    """
    try:
        # Convert the date into a datetime object
        date = datetime.strptime(date_str, "%Y-%m-%d")
        
        year = date.year
        month = date.month
        
        if grouping_type == 'decade':
            # Group by decade
            decade_start_year = (year // 10) * 10  # Rounds the year to the beginning of the decade
            grouped_date = datetime(decade_start_year, 1, 1)
        
        elif grouping_type == 'quarter':
            # Group by quarter
            if 1 <= month <= 3:
                grouped_date = datetime(year, 1, 1)  # 1. quarter
            elif 4 <= month <= 6:
                grouped_date = datetime(year, 4, 1)  # 2. quarter
            elif 7 <= month <= 9:
                grouped_date = datetime(year, 7, 1)  # 3. quarter
            else:
                grouped_date = datetime(year, 10, 1)  # 4. quarter
        
        # Return in the desired format (YYYY-MM-DD)
        return grouped_date.strftime("%Y-%m-%d")
    
    except ValueError:
        # If the date cannot be processed, the original date is returned
        return date_str


def anonymize_deceased_date_grouping(date_str, grouping_type='decade'):
    """
    Anonymizes the 'deceasedDateTime' field to 12:00 of the same day and groups it by decade or quarter.
    
    :param date_str: DeceasedDateTime in format 'YYYY-MM-DDTHH:MM:SS-00:00'
    :param grouping_type: The type of grouping ('decade' or 'quarter')
    :return: anonymizes 'deceasedDateTime' in format 'YYYY-MM-DDT12:00:00-00:00'
    """
    try:
        # Convert the date with time zone into a datetime object
        deceased_datetime = datetime.fromisoformat(date_str)
        
        # Keep the time zone
        tzinfo = deceased_datetime.tzinfo
        
        # Set the time to 12:00 and keep the time zone
        anonymized_datetime = deceased_datetime.replace(hour=12, minute=0, second=0, microsecond=0)

        # Grouping by decade or quarter
        year = anonymized_datetime.year
        month = anonymized_datetime.month

        if grouping_type == 'decade':
            # Group by decade
            decade_start_year = (year // 10) * 10  # Rounds the year to the beginning of the decade
            grouped_date = anonymized_datetime.replace(year=decade_start_year, month=1, day=1)

        elif grouping_type == 'quarter':
            # Group by quarter
            if 1 <= month <= 3:
                grouped_date = anonymized_datetime.replace(month=1, day=1)  # 1. quarter
            elif 4 <= month <= 6:
                grouped_date = anonymized_datetime.replace(month=4, day=1)  # 2. quarter
            elif 7 <= month <= 9:
                grouped_date = anonymized_datetime.replace(month=7, day=1)  # 3. quarter
            else:
                grouped_date = anonymized_datetime.replace(month=10, day=1)  # 4. quarter

        # Keep the time zone
        if tzinfo:
            grouped_date = grouped_date.replace(tzinfo=tzinfo)
        else:
            grouped_date = grouped_date.replace(tzinfo=deceased_datetime.tzinfo)  # Keep the default time zone

        # Return in the desired format
        return grouped_date.isoformat()

    except ValueError:
        # If the date cannot be processed, the original date is returned
        return date_str
