# PlanKauf
Simplify your centralized company shopping process with Telegram, Google Sheets and Python!

1. Create a Service Account. Go to https://console.cloud.google.com/ with your Google account and click "Create a new project" and name it. Go to the API & Services section. Click ENABLE APIS AND SERVICES. Go to the library(https://console.cloud.google.com/apis/library?). Add Google Drive Api and Google Sheets Api. Go to the Service Accounts section. Create a service account and add the owner role to it. Copy the username, it will be useful to you in the second paragraph. In the service account settings, select the keys section and create a JSON-key. The key will be automatically downloaded to your computer. The key must be in the folder with the main script, or you will need to specify the full path to it.

2. Create a Google Spreadsheet. Name your sheet and fill in the details: Employee A1, Total A2, Smith A3, Smith Reason A4, Pens B1, etc. Copy the spreadsheet ID from your browser's address bar - it should be a long set of characters in the middle of the URL, starting with 1 between forward slashes (/). Grant access to your service account with editor rights by adding its username to the list of users. You will need to set a range of cells in the variable: <"Sheet name"! "A":"Z">, which will depend on the number of names in your table.

3. Create your Telegram Bot. In the application or web version of the Telegram messenger, find the bot by the name @BotFather. Using the shortcut keys press /newbot, come up with a name. Then come up with a name with the prefix Bot. After successfully creating a bot, you will receive a message with your bot token. Copy the token and assign the value to the variable.

4. Installing Python modules. All modules are installed through the pip3 manager by name, except for telebots and apiclient. To install telebots, enter pip3 install pyTelegramBotAPI. It is also necessary to install google-api-python-client.

5. Assign the values from the first three points to the variables. All variables are marked with a comment in the script. Enjoy your use!
