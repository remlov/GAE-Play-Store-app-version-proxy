Synopsis
==
Easy to deploy Android version proxy for Google App Engine.

Motivation
--
Google doesn't provide a simple way nor API to check your Android version within the application. Although a slew of Android libraries exist to faciliate this, there isn't a simple server side proxy implentation to use in conjunciton with aforementioned libraries.

Installation
--
Modify <b>app.yaml</b> and change <b>application</b> name to your own matching the application you created in the GAE Console, change <b>play_store_url</b> to your own Android Application Store URL. Deploy via command line or use the GoogleAppEngineLauncher.

API Reference
--
Your version proxy server should return something similar as the following:
```json
{
    content: "What's New:</p><br><li>First Play store release.</li>",
    version_code: 8
}
```
In the included Android sample I used the Android library [WVersionManager](https://github.com/winsontan520/Android-WVersionManager). In you MainActivity of your Android app do something like the following:
```java
@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);

    WVersionManager versionManager = new WVersionManager(this);
    versionManager.setVersionContentUrl("http://myGaeProxyUrl.appspot.com");
    versionManager.checkVersion();
}
```
Where <b>myGaeProxyUrl</b> will point to your deployed proxy server.
Caveat
--
As [WVersionManager](https://github.com/winsontan520/Android-WVersionManager) and other Android libraries generally use the <b>versionCode</b> and not the <b>versionName</b> and the only available metadata to scrape of the Play Store is the <b>versionName</b> I use the semantic versioning paradigm and use the PATCH value and match it to the <b>versionCode</b> eg:
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.remlov.androidversionproxyexample"
    android:versionCode="1"
    android:versionName="1.0.1">
```
Questions
--
<b>Question</b>: Why use a proxy at all instead of having the Android app do the Play Store url scraping?

<b>Answer</b>: If you have a slew of users using your application and Google decides to change the layout of the Play Store and/or change the tag used to search and find the <b>versionName</b>, your users will be out of luck to get an in app update notification. If you use a proxy, you can just update your proxy server to mitigate such an issue.
License
--

* MIT License