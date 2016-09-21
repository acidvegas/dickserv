# dickserv
A bot with many useful commands &amp; features for the Internet Relay Chat (IRC) protocol.

###### Note
This is just the source code to and IRC bot that I have ran on some IRC networks, and is used as a reference.
Changes *may* need to be made in order for someone to run this on their own channel/network.

###### Requirments
 - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

###### Config
Browse to the */core/* folder and edit the *config.py* file.

###### Commands
| Command | Description |
| --- | --- |
| @help | Information about the commands. |
| .ascii delete \<name> | Delete the \<name> ASCII art file. |
| .ascii list | A list of all the ASCII art files. |
| .ascii random | Display a random ASCII art file. |
| .ascii rename \<old> \<new> | Rename the \<old> ASCII art file to \<new>. |
| .ascii \<name> | Display the <name> ASCII art file. |
| .btc | Bitcoin rate in USD. |
| .date | Get the current date and time. |
| .define \<word> | Get the definition of <word>. |
| .dickserv | Information about the bot. |
| .filter enable | Enable word filters. (+G) |
| .filter disable | Disable word filters. (-G) |
| .flood enable | Enable channel message flooding. (-f) |
| .flood disable | Disable channel message flooding. (+f) |
| .geoip \<ip> | Geographical location information about \<ip>. |
| .imdb \<query> | Search IMDb and return the 1st result for <search>. |
| .isup \<url> | Check if \<url> is up or not. |
| .ltc | Litecoin rate in USD. |
| .r \<subreddit> | Read top posts from <subreddit> |
| .remind \<time> \<text> | Remind yourself about \<text> in \<time>. |
| .resolve \<ip/url> | Resolve a <ip/url> to a hostname or IP address. |
| .steam \<query> | Search \<query on the Steam store. |
| .talent | RIP DITTLE DIP DIP DIP DIP IT\'S YA BIRTHDAY!!1@11! |
| .tpb \<query> | Searc \<query on ThePirateBay. |
| .ud \<word> | Get the urban dictionary definition of \<word>. |
| .uptime | Get the amount of time DickServ has been running. |
| .wolfram \<ask> | Get the results of <query> from WolframAlpha. |
| .yt \<query> | Search \<query> on YouTube. |

##### ToDo
- Add a google / quote / tweet command.
- Security measures against command floods.
