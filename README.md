## ComiCalender

### Abstract
This application update release day of comics on Google Calendar automatically.

### How to deploy
This application uses Google Cloud Function, Scheduler and Pub/Sub.  
Scheduler invoke Cloud Function using Pub/Sub. Details are [here](https://cloud.google.com/scheduler/docs/tut-pub-sub).  
LINE_ACCESS_TOKEN and GOOGLE_DALENDAR_ID have to be set as environment variable.