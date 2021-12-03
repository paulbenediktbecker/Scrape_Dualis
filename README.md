# Scrape_Dualis

This is a webscraper for students of the DHBW.

Script based on the work of: [Scrape_Dualis](https://github.com/F-Wer/Scrape_Dualis)

This script will scrape your grades of Dualis and send you a mail, once a change is detected. 

Therefore, it only makes sense to run this on a VPS or similar Server. 

Args: 
  
    index of secret.json file -> for having different scripts running simultanously 
    
    
## secret.json

There has to be a file called secret.json :
```
{
    "1":{
        "passwort_g":"", //password of sender mail
        "recipent": "['test@gmail.com']",
        "sender_email": "testdev@gmail.com",
        "username":"wi12345@lehre.dhbw-stuttgart.de",
        "password":"" //password of dualis 
    },
    "2":{
        "passwort_g":"", //password of sender mail
        "recipent": "['test@gmail.com']",
        "sender_email": "testdev@gmail.com",
        "username":"wi12345@lehre.dhbw-stuttgart.de",
        "password":"" //password of dualis 
    }
}   
```

