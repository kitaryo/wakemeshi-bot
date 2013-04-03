wakemeshi_bot
=============

和敬飯botは、男子寮「和敬塾」の食堂メニューをスクレイピングしてTwitterで呟くツールです。

cron.yaml
- periodic notification
- periodic process of mentions
- periodic scraping of menus

/notification
-> invokes notification.py; tweets next menu

/menu
-> invokes menu.py; scrapes menus from wakeijuku site

/mention
-> invokes mention.py; processes mentions
