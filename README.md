# BerkshireQuotesGoogle

A Google Assistant app which gives quotes by Warren Buffett and Charlie Munger. This is written based on the Alexa skill I wrote for the same purpose (https://github.com/vishalbala-nps/BerkshireQuotes.git)

## Setup Instructions:
### Cloning the project
Start by cloning the repository on to your local machine with the following command:
```bash
git clone https://github.com/vishalbala-nps/BerkshireQuotesGoogle.git
```
### Setup Dialogflow

* Go to dialogflow.cloud.google.com and login with your Google Account Credentials. Then, click on "Create Agent" and set the language to "English - en" and set your Timezone as well

* Then, Click on the settings button and select "Export and Import". Then, in this screen, click on "Restore from ZIP" and select the BerkshireQuotes.zip file in this repostitory. This zip file contains the intents, entities required for this project

* Then, in the sidebar, click on "Integrations" and under Google Assistant, click on "Intergration Settings"

* Type "openskill" in Explicit Inovocation and type "startskill" and "startskillwithAuthor" in Implicit Invocation and click Close. Click on Fulfilment and keep this page open as we need to configure AWS DynamoDB and Google Cloud App Engine

### Setup in AWS
NOTE: If you have already set up DynamoDB Tables for the Berkshire Quotes Alexa Skill, you can skip creation of Authors and Quotes table and move on to creating AWS Users

#### Setup DynamoDB Tables
* Now, we need to setup Amazon DynamoDB Tables. Make sure you are logged in to your AWS Account. Go to: https://eu-west-1.console.aws.amazon.com/dynamodb/home/ Then, click on "Create table"

##### Setup Authors table
* Now, for name of table, enter "Authors" and type "AuthorId" as Primary Key and select it as Number. Now click on Create.

* Now, after the table has been created, click on "Items" and click on "Create Item"

* Here, on the text box which says "value", enter the Author ID. Which in this case is 1

* Then click on the plus sign and select Insert. Under this, select "String" and in Field, enter it as "AuthorName". Now, enter an author's name under value. In this case, Warren Buffett. After this, select Save

* Do this for all other Authors. Do note that the "AuthorId" MUST be unique

##### Setup Quotes table
* Now, for name of table, enter "Quotes" and type "QuoteID" as Primary Key and select it as Number. Now click on Create.

* Now, after the table has been created, click on "Items" and click on "Create Item"

* Here, on the text box which says "value", enter the Quote ID. Which in this case is 1

* Then click on the plus sign and select Insert. Under this, select "Number" and in Field, enter it as "AuthorID". Now, enter the author's id from the previous table

* Now, again click on the plus sign and select Insert. Under this, select "String" and in Field, enter it as "Quote". Now, enter a Quote from that author. After this, select Save

* Do this for all other Quotes. Do note that the "QuoteID" MUST be unique

##### Create AWS User
A User needs to be created in AWS with permissons to access DynamoDB. This user credentials will be used by our Web Service
* Now, make sure you are logged in to AWS. If you are logged in, go to: https://console.aws.amazon.com/iam/home

* Click on Users on the sidebar and click on Add User

* Specify a name for the User and for Access Type, click on Programmatic Access and click on "Next: Permissons"

* Then, select "Attach existing policies directly" and add the "AWSLambdaDynamoDBExecutionRole" and "AmazonDynamoDBFullAccess" permissons and click on "Next: Tags". We can ignore this step. So, click on "Next: Review" and click on "Create User"

* Now, click on "Download .csv" and keep this file safe as we need this file later on

### Google Cloud Platform configuration

#### Setup Google Cloud App engine

* Login into your Google Cloud Console and make sure billing is enabled. Click on the project drop down and select "New Project" and give your project a name 

* Now, make sure you have gcloud installed on your Local Machine and configured with this project and your account. If not, follow the instructions to install and setup at https://cloud.google.com/sdk/docs/quickstarts If you have gcloud already installed but, configured with a different project or account, type `gcloud init` and follow the instructions

* After gcloud is installed, create a new App on Google App Engine by typing the following command

```bash
gcloud app create
```

Follow the instructions in this screen and set the server to "us-central". Set a name for your app and make a note of the app's URL (mostly: <YOUR_PROJECT_ID>.appspot.com)

* Now, go back to our Dialogflow console and in Fulfilment, enable Webhook and enter our engine's URL and click Save

#### Deploy our Project

* Now, in your local machine, enter inside the "AppEngine" folder of this repository and open the main.py file. Enter the Access Key and secret from the AWS Credentials downloaded in the CSV File earlier and save it.

* After that, we need to deploy our project by following the command:

```bash
gcloud app deploy
```

Follow the instructions given in this command to deploy the project

### Testing our App and invocation names

* Go to our Dialogflow console and on the sidebar, click on "Integrations" and under Google Assistant, click on "Intergration Settings"

* Then, in this screen click on Test to test our app. Type "talk to my test app" in the test area and make sure everything is working

* You can also tell "Talk to my Test App" on any Google Assistant based device linked to the Dialogflow account

#### Invocation Names

If you want, instead of using "Talk to my Test App" to call our App, we can create a more specific invocation name. To do so, follow the steps:

* Go to our Dialogflow console and on the sidebar, click on "Integrations" and under Google Assistant, click on "Intergration Settings"

* Then, in this screen click on Test. This will navigate you to the Actions on Google console.

* Click on "Develop" and under Display name, enter your invocation name and click Save. If you want, you can alter the assistant's voice as well.

