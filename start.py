import Overlord
import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler
from discord import LoginFailure, ClientException, DiscordException
from time import sleep

# Set up a log for when the bot restarts incase user is away and the bot completely dies
logger = logging.getLogger('Overlord-start.py')
logger.setLevel(logging.DEBUG)
fh = TimedRotatingFileHandler(filename='Overlord-StartErrors.log', when='d', interval=1, backupCount=5, encoding='utf-8',)
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s > %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Run the bot and set up auto-restart
run = True
while run:
    try:
        loop = asyncio.get_event_loop()
        bot = Overlord.Bot()
        # Start bot
        loop.run_until_complete(bot.start())
    except Overlord.MissingConfigFile as e:
        # Missing Config File
        logger.critical("Config File Missing: {}".format(e))
        logger.info("A config file has been made for you (Overlord/config.json). Please fill it out and restart the bot")
        run = False
    except (LoginFailure, Overlord.LoginError) as e:
        # LogIn Fails
        loop.run_until_complete(bot.logout())
        logger.critical("Login Failed: {}".format(e))
        run = False
    except (ClientException, DiscordException):
        # Discord disconnected the bot
        loop.run_until_complete(bot.logout())
        logger.error("Disconnected will try to reconnect: {}".format(e))
        run = True
        sleep(20)
    except SystemExit as e:
        # System Exit
        loop.close()
        logger.critical("System Exit: {}".format(e))
        run = False
    except Exception as e:
        # Any Unknown Exception
        logger.critical("Unknown Exception: {}".format(e))
        run = False
    finally:
        if run == False:
            loop.close()