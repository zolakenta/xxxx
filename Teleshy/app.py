from colorama import *
from datetime import datetime
from pyrogram import Client
from pyrogram.errors import (
    FloodWait,
    BadRequest,
    PhoneNumberBanned,
    PhoneNumberInvalid,
    PhoneCodeExpired,
    PhoneCodeHashEmpty,
    PhoneCodeInvalid,
    PasswordHashInvalid,
    SessionPasswordNeeded,
    Unauthorized,
    AuthKeyUnregistered,
    UserDeactivated
)
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
from telethon.sync import TelegramClient
from telethon.errors import (
    PhoneNumberBannedError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)
from urllib.parse import unquote
import asyncio
import os
import re
import sys

class Teleshy:
    def __init__(self):
        self.api_id = 25121246
        self.api_hash = 'ef0474010e5db79d4112fe7e2cdc8c65'

    def print_timestamp(self, message):
        print(
            f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{message}",
            flush=True
        )

    async def create_telegram_session_pyrogram(self, phone_number: str):
        self.print_timestamp(
            f"{Fore.WHITE + Style.BRIGHT}[ 📱 ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}[ {phone_number} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.BLUE + Style.BRIGHT}[ Creating Session With Pyrogram ]{Style.RESET_ALL}"
        )
        client = Client(
            name=f'sessions/pyrogram/{phone_number}',
            api_id=self.api_id,
            api_hash=self.api_hash
        )
        try:
            if not client.is_connected:
                await client.connect()

            try:
                phone_code_hash = await client.send_code(phone_number=phone_number)
            except PhoneNumberBanned:
                return self.print_timestamp(
                    f"{Fore.CYAN + Style.BRIGHT}[ {phone_number} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}[ Is Banned From Telegram And Cannot Be Used ]{Style.RESET_ALL}"
                )
            except PhoneNumberInvalid:
                return self.print_timestamp(
                    f"{Fore.CYAN + Style.BRIGHT}[ {phone_number} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}[ Is Invalid ]{Style.RESET_ALL}"
                )
            max_attempts = 3
            attempts = 0
            while attempts < max_attempts:
                try:
                    phone_code = input(
                        f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[ 📥 ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}[ Please Enter The Code You Received ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    ).strip()
                    await client.sign_in(
                        phone_number=phone_number,
                        phone_code_hash=phone_code_hash.phone_code_hash,
                        phone_code=phone_code
                    )
                    break
                except PhoneCodeExpired:
                    return self.print_timestamp(
                        f"{Fore.CYAN + Style.BRIGHT}[ {phone_number} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ The Confirmation Code Has Expired ]{Style.RESET_ALL}"
                    )
                except PhoneCodeHashEmpty:
                    return self.print_timestamp(
                        f"{Fore.CYAN + Style.BRIGHT}[ {phone_number} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ The Phone Code Hash Is Missing ]{Style.RESET_ALL}"
                    )
                except PhoneCodeInvalid:
                    attempts += 1
                    if attempts < max_attempts:
                        self.print_timestamp(
                            f"{Fore.CYAN + Style.BRIGHT}[ {phone_number} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}[ The Phone Code Entered Was Invalid. Attempt {attempts} Of {max_attempts} ]{Style.RESET_ALL}"
                        )
                    else:
                        return self.print_timestamp(
                            f"{Fore.CYAN + Style.BRIGHT}[ {phone_number} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT}[ The Phone Code Entered Was Invalid. Maximum Attempts Reached. ]{Style.RESET_ALL}"
                        )
                except SessionPasswordNeeded:
                    max_password_attempts = 3
                    password_attempts = 0
                    while password_attempts < max_password_attempts:
                        try:
                            password = input(
                                f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}[ 👀 ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT}[ Enter Password ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            ).strip()
                            await client.check_password(password=password)
                            break
                        except PasswordHashInvalid:
                            password_attempts += 1
                            if password_attempts < max_password_attempts:
                                self.print_timestamp(
                                    f"{Fore.CYAN + Style.BRIGHT}[ {phone_number} ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}[ The Two-step Verification Password Is Invalid. Attempt {password_attempts} Of {max_password_attempts} ]{Style.RESET_ALL}"
                                )
                            else:
                                return self.print_timestamp(
                                    f"{Fore.CYAN + Style.BRIGHT}[ {phone_number} ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}[ The Two-step Verification Password Is Invalid. Maximum Attempts Reached. ]{Style.RESET_ALL}"
                                )
                    me = await client.get_me()
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ ✅ ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}[ Hello {me.first_name}! Your Session Saved As sessions/pyrogram/{phone_number}.session ]{Style.RESET_ALL}"
                    )

                    if client.is_connected:
                        return await client.disconnect()
        except FloodWait as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ FloodWait While Creating Session With Pyrogram: A wait of {str(e.value)} seconds is required (caused by \"auth.SendCode\") ]{Style.RESET_ALL}")
        except BadRequest as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Bad Request While Creating Session With Pyrogram: {str(e)} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Unexpected Error While Creating Session With Pyrogram: {str(e)} ]{Style.RESET_ALL}")

    async def create_telegram_session_telethon(self, phone: str):
        self.print_timestamp(
            f"{Fore.WHITE + Style.BRIGHT}[ 📱 ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}[ {phone} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.BLUE + Style.BRIGHT}[ Creating Session With Telethon ]{Style.RESET_ALL}"
        )

        client = TelegramClient(
            session=f"sessions/telethon/{phone}",
            api_id=self.api_id,
            api_hash=self.api_hash
        )

        try:
            await client.connect()

            try:
                await client.send_code_request(phone=phone)
            except PhoneNumberBannedError:
                return self.print_timestamp(
                    f"{Fore.CYAN + Style.BRIGHT}[ {phone} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}[ Has Been Banned From Telegram And Cannot Be Used Anymore ]{Style.RESET_ALL}"
                )
            except PhoneNumberInvalidError:
                return self.print_timestamp(
                    f"{Fore.CYAN + Style.BRIGHT}[ {phone} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}[ Is Invalid ]{Style.RESET_ALL}"
                )
            max_attempts = 3
            attempts = 0
            while attempts < max_attempts:
                try:
                    code = input(
                        f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[ 📥 ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}[ Please Enter The Code You Received ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    ).strip()
                    await client.sign_in(phone=phone, code=code, password=None)
                    break
                except PhoneCodeInvalidError:
                    attempts += 1
                    if attempts < max_attempts:
                        self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ The Phone Code Entered Was Invalid. Please Try Again. Attempt {attempts} Of {max_attempts} ]{Style.RESET_ALL}")
                    else:
                        return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ The Phone Code Entered Was Invalid. Maximum Attempts Reached. ]{Style.RESET_ALL}")
                except SessionPasswordNeededError:
                    max_password_attempts = 3
                    password_attempts = 0
                    while password_attempts < max_password_attempts:
                        try:
                            password = input(
                                f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT}[ 👀 ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                f"{Fore.YELLOW + Style.BRIGHT}[ Enter Password ]{Style.RESET_ALL}"
                                f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            ).strip()
                            await client.sign_in(password=password)
                            break
                        except PasswordHashInvalidError:
                            password_attempts += 1
                            if password_attempts < max_password_attempts:
                                self.print_timestamp(
                                    f"{Fore.CYAN + Style.BRIGHT}[ {phone} ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}[ The Two-step Verification Password Is Invalid. Attempt {password_attempts} Of {max_password_attempts} ]{Style.RESET_ALL}"
                                )
                            else:
                                return self.print_timestamp(
                                    f"{Fore.CYAN + Style.BRIGHT}[ {phone} ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.RED + Style.BRIGHT}[ The Two-step Verification Password Is Invalid. Maximum Attempts Reached. ]{Style.RESET_ALL}"
                                )
                    me = await client.get_me()
                    self.print_timestamp(
                        f"{Fore.WHITE + Style.BRIGHT}[ ✅ ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT}[ Hello {me.first_name}! Your Session Saved As sessions/telethon/{phone}.session ]{Style.RESET_ALL}"
                    )

                    return await client.disconnect()
        except Exception as e:
            return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Unexpected Error While Creating Session With Telethon: {str(e)} ]{Style.RESET_ALL}")

    async def generate_queries(self, session: str, referral_url: str, file_name_queries: str):
        try:
            bot_username = re.search(r"https://t.me/(\w+)/", referral_url).group(1)
            short_name = re.search(r"t.me/\w+/(\w+)\?", referral_url).group(1)
            referral = re.search(r"startapp=([^&]+)", referral_url).group(1)

            client = Client(
                name=f'sessions/test/{session}',
                api_id=self.api_id,
                api_hash=self.api_hash
            )

            if not client.is_connected:
                try:
                    await client.connect()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered) as e:
                    raise e

            while True:
                try:
                    peer = await client.resolve_peer(bot_username)
                    break
                except FloodWait as e:
                    self.print_timestamp(
                        f"{Fore.CYAN + Style.BRIGHT}[ {session} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}[ FloodWait {str(e.value)} Seconds While Generating Query With Pyrogram ]{Style.RESET_ALL}"
                    )
                    await asyncio.sleep(e.value + 3)

            web_view = await client.invoke(RequestAppWebView(
                peer=peer,
                app=InputBotAppShortName(bot_id=peer, short_name=short_name),
                platform='ios',
                write_allowed=True,
                start_param=referral
            ))

            auth_url = web_view.url
            query = unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

            if not os.path.exists(f'{file_name_queries}.txt'):
                open(f'{file_name_queries}.txt', 'w').close()

            with open(f'{file_name_queries}.txt', 'a') as file:
                file.write(f'{query}\n')

            if client.is_connected:
                await client.disconnect()

            return self.print_timestamp(f"{Fore.GREEN + Style.BRIGHT}[ Successfully Generate Query For {session} ]{Style.RESET_ALL}")
        except Exception as e:
            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {session} Unexpected Error While Generating Query With Pyrogram: {str(e)} ]{Style.RESET_ALL}")

    async def main(self):
        while True:
            try:
                self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ 1. Create Telegram Session (Pyrogram & Telethon) ]{Style.RESET_ALL}")
                self.print_timestamp(f"{Fore.CYAN + Style.BRIGHT}[ 2. Generate Query ]{Style.RESET_ALL}")
                choice = input(
                    f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Select Number ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                ).strip()
                if choice == "1":
                    phone_numbers = [line.strip() for line in open('phone_numbers.txt') if line.strip()]
                    if not phone_numbers:
                        return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ No Phone Numbers Available! Please Fill The File With Number Phone Of Your Telegram. ]{Style.RESET_ALL}")

                    for phone_number in phone_numbers:
                        await self.create_telegram_session_pyrogram(phone_number=phone_number)
                        await self.create_telegram_session_telethon(phone=phone_number)
                elif choice == "2":
                    sessions = [file.replace('.session', '') for file in os.listdir('sessions/test/') if file.endswith('.session')]
                    if not sessions:
                        return self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ No Session Files Found In The Folder! Please Make Sure There Are '*.session' Files In The Folder. ]{Style.RESET_ALL}")

                    file_name_queries = input(
                        f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT}[ File Name Queries (Without '.txt') ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    ).strip()

                    while True:
                        referral_url = input(
                            f"{Fore.BLUE + Style.BRIGHT}[ {datetime.now().astimezone().strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.YELLOW + Style.BRIGHT}[ Referral URL (e.g https://t.me/major/start?startapp=6094625904) ]{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        ).strip()
                        if re.match(r"https://t.me/\w+/\w+\?startapp=[^&]+", referral_url):
                            break
                        else:
                            self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Invalid URL Format! Please Enter A Valid URL ]{Style.RESET_ALL}")

                    tasks = []
                    for session in sessions:
                        tasks.append(self.generate_queries(session=session, referral_url=referral_url, file_name_queries=file_name_queries))

                    await asyncio.gather(*tasks)
                else:
                    self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ Invalid Choice! Please Enter 1 Or 2 ]{Style.RESET_ALL}")
            except Exception as e:
                self.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        init(autoreset=True)
        teleshy = Teleshy()
        asyncio.run(teleshy.main())
    except Exception as e:
        teleshy.print_timestamp(f"{Fore.RED + Style.BRIGHT}[ {str(e)} ]{Style.RESET_ALL}")
    except KeyboardInterrupt:
        sys.exit(0)