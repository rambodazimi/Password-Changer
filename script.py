import requests
import base64
from bs4 import BeautifulSoup
import webbrowser


# Author: Rambod Azimi
# This Python script gets the IP address of the printer with username and password
# Then, it do the authorization process and goes to the following menus:
# Print Server Settings --> Print Server --> Web Admin
# Finally, it displays the content of that page (Admin name, password, http port, ...)

url = 'http://192.168.1.93'
username = 'admin'
password = '1234'

credentials = f'{username}:{password}'.encode('utf-8')
encoded_credentials = base64.b64encode(credentials).decode('utf-8')

headers = {
    'Authorization': f'Basic {encoded_credentials}'
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')
print_server_settings_link = soup.find('a', text='Print Server Settings')

if print_server_settings_link:
    print_server_settings_url = url + print_server_settings_link.get('href')
    print_server_settings_response = requests.get(print_server_settings_url, headers=headers)

    print_server_settings_soup = BeautifulSoup(print_server_settings_response.content, 'html.parser')
    print_server_link = print_server_settings_soup.find('a', text='Print Server')

    if print_server_link:
        print_server_url = url + print_server_link.get('href')

        print_server_response = requests.get(print_server_url, headers=headers)

        print_server_soup = BeautifulSoup(print_server_response.content, 'html.parser')
        web_admin_link = print_server_soup.find('a', text='Web Admin')

        if web_admin_link:
            web_admin_url = url + '/' + 'server/' + web_admin_link.get('href')
            print(f"LINK = {web_admin_url}")
            webbrowser.open(web_admin_url)
            web_admin_response = requests.get(web_admin_url, headers=headers)
            print(web_admin_response.content)
        else:
            print('Web Admin link not found on Print Server page')
    else:
        print('Print Server link not found on Print Server Settings page')
else:
    print('Print Server Settings link not found')
