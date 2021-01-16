
def get_country_with_codes():
    countries = []
    with open("country.txt", "r") as f:
        for country in f.readlines():

           country_code, country = get_country_code_and_country_from_string(country)
           country_and_code = (country, f"{country} ({country_code})")

           countries.append(country_and_code)
    return countries


def get_country_code_and_country_from_string(s):

    value = s.split('"')
    country_code = value[1]
    country = value[2].split("<")[0][1:]
    return country_code, country


def sort_job_sites(jobs):
    return sorted(jobs, key=lambda x: x[1])


def split_number_from_text():

    phone_numbers_list = []

    with open("phone_number_code.txt", "r") as f:
        phone_numbers = f.readlines()

        for phone_number in phone_numbers:
            value = phone_number.split("---")
            country_code = value[0].strip()
            country = value[1].strip()
            new_country_code = (f'{country_code}', f'(+{country_code}) {country}')
            phone_numbers_list.append(new_country_code)
    return phone_numbers_list




