# dickserv
A bot with many useful commands &amp; features for the Internet Relay Chat (IRC) protocol.

###### Requirments
 - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

###### Config
Browse to the */core/* folder and edit your *config.py* file.

**Note:** The key, password, nickserv, and operserv configs can be set to None (No quotations) to disbale it.

###### Commands
| Command | Description |
| --- | --- |
| @help | Information about the commands. |
| .ascii list | A list of all the ASCII art files. |
| .ascii \<name> | Display the <name> ASCII art file. |
| .btc | Bitcoin rate in USD. |
| .date | Get the current date and time. |
| .define \<word> | Get the definition of <word>. |
| .dickserv | Information about the bot. |
| .fml | Random \'FuckMyLife\' story. |
| .g \<query> | Search <query> on Google. |
| .imdb \<query> | Search IMDb and return the 1st result for <search>. |
| .isgd \<url> | Shorten <url> to an IsGd URL. |
| .isup \<url> | Check if <url> is up or not. |
| .ltc | Litecoin rate in USD. |
| .reddit \<subreddit> | Read top posts from <subreddit> |
| .resolve \<ip/url> | Resolve a <ip/url> to a hostname or IP address.
| .talent | RIP DITTLE DIP DIP DIP DIP IT\'S YA BIRTHDAY!!1@11! |
| .tinyurl \<url> | Shorten <url> to a TinyURL URL. |
| .todo | Read all the To DO entries for your nick. |
| .todo add \<string> | Add a new To Do entry. |
| .todo del \<number> | Delete the <number> To Do entry. |
| .ud \<word> | Get the urban dictionary definition of <word>. |
| .uptime | Get the amount of time DickServ has been running. |
| .wolfram \<ask> | Get the results of <query> from WolframAlpha. |
| .yt \<query> | Search <query> on YouTube. |

##### ToDo
- Fix google command.
- Use sqlite3 databases for todo managment. (Max of 3 entrees per-nick, 15 todo's max.)
- Add admin only commands via PM that checks for a certain user@host mask. (ignore, say, act, etc...)
- Baisc channel management to replace ChanServ.
