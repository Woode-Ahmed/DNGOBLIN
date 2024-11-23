import requests
import json
from colorama import Fore, init
from datetime import datetime
import time
import random

init(autoreset=True)

def read_init_data(file_path='data.txt'):
    with open(file_path, 'r') as file:
        return file.read().strip()

def login(intdata):
    url = "https://api.goblinmine.game/graphql"
    payload = {
        "operationName": "login",
        "variables": {
            "input": {
                "initData": intdata
            }
        },
        "query": "mutation login($input: LoginInput!) {\n  login(input: $input) {\n    status\n    token\n    user {\n      id\n      first_name\n    }\n  }\n}"
    }
    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if "data" in data and "login" in data["data"]:
            return data["data"]["login"]["token"], data["data"]["login"]["user"]["first_name"]
    print(Fore.RED + "Login failed.")
    return None, None




def get_bronze_world_balance(token):
    url = "https://api.goblinmine.game/graphql"

    
    payload = json.dumps({
        "operationName": "worlds",
        "variables": {},
        "query": """
        query worlds {
          worlds {
            active
            icon
            income_day
            name
            id
            currency {
              ...CURRENCY_FRAGMENT
              __typename
            }
            __typename
          }
        }

        fragment CURRENCY_FRAGMENT on Currency {
          id
          amount
          coefficient
          icon
          name
          __typename
        }
        """
    })

    # الرؤوس (Headers)
    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    try:
        
        response = requests.post(url, data=payload, headers=headers)

        
        if response.status_code == 200:
            data = response.json()
            worlds = data.get('data', {}).get('worlds', [])

            # المتغير لتخزين رصيد العالم 
            bronze_world_balance = None

            # تصفية العالم البرونزي حسب الاسم
            for world in worlds:
                name = world.get('name', "").lower()  # التأكد من أن الاسم موجود وتحويله إلى أحرف صغيرة
                currency = world.get('currency', {})
                amount = currency.get('amount')

                # إذا كان اسم العالم هو "Bronze world" وكان الرصيد موجودًا
                if name == "bronze world" and amount is not None:
                    bronze_world_balance = int(amount)
                    break  # الخروج بعد العثور على العالم البرونزي

            # إذا لم يتم العثور على الرصيد
            if bronze_world_balance is None:
                print("Bronze world not found or no amount available.")
                return 0  # قيمة افتراضية

            return bronze_world_balance  # إعادة الرصيد إذا تم العثور عليه

        else:
            print(f"Failed to fetch data. Status Code: {response.status_code}")
            print("Response Text:", response.text)
            return 0  # قيمة افتراضية عند فشل الطلب

    except Exception as e:
        print(f"An error occurred: {e}")
        return 0  # قيمة افتراضية عند حدوث خطأ

# مثال على كيفية استدعاء الدالة


# استدعاء الدالة مع التوكن

def welcome_user(name, token):
    
    today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    print(Fore.CYAN + "===============================")
    print(Fore.GREEN + f"Welcome {name}!")
    
    print(Fore.YELLOW + f"Current Date and Time: {today}")
    print(Fore.YELLOW + f"Your access token is: {token}")
    
    print(Fore.CYAN + "===============================")
set = int(input(Fore.BLUE+"Set Your Mine Level Goblin : "))    
#set buy
def buy_mine(token):
    url = "https://api.goblinmine.game/graphql"
    payload = {
        "operationName": "buyMine",
        "variables": {
            "input": {
                "mineId": set
            }
        },
        "query": "mutation buyMine($input: BuyMineInput!) {\n  buyMine(input: $input) {\n    message\n    status\n  }\n}"
    }
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json",
    }

    # إرسال الطلب
    response = requests.post(url, json=payload, headers=headers)

    # معالجة الاستجابة
    try:
        data = response.json()
        if "data" in data and data["data"].get("buyMine") is not None:
            message = data["data"]["buyMine"]["message"]
            print(Fore.GREEN + f"BuyMine message: {message}")
        else:
            error_message = data.get("errors", [{"message": "Unknown error"}])[0]["message"]
            print(Fore.RED + f"Don Buy Mine")
    except ValueError:
        print(Fore.RED + "Error: Failed to parse JSON response.")
        print(Fore.RED + f"Response: {response.text}")






def CatchWork(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "mineAndMiners",
        "variables": {
            "mineId": set
        },
        "query": "query mineAndMiners($mineId: Int!) {\n  mine(mineId: $mineId) {\n    ...MINE_FRAGMENT\n    __typename\n  }\n  miners(mineId: $mineId) {\n    ...MINERS_FRAGMENT\n    __typename\n  }\n}\n\nfragment MINE_FRAGMENT on MineFool {\n  deposit_day\n  goblin_image\n  id\n  image\n  income_per_day\n  level\n  miner_amount\n  name\n  price\n  user_miners_count\n  volume\n  userMine {\n    auto\n    cart_level\n    deposit_day\n    deposit_day_default\n    extracted_amount\n    extracted_percent\n    id\n    income_hour\n    next_volume\n    updateIn\n    volume\n    updated_at\n    total_day\n    __typename\n  }\n  currency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  miningCurrency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  __typename\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}\n\nfragment MINERS_FRAGMENT on Miners {\n  available\n  id\n  level\n  name\n  price\n  currency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  minerLevel {\n    available\n    disabled\n    existInventoryLevel\n    id\n    image\n    income_hour\n    level\n    name\n    price\n    inventoryLevel {\n      level\n      name\n      __typename\n    }\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        # استخراج بيانات miners
        miners = data.get('data', {}).get('miners', [])
        
        # استخراج العناصر التي يكون فيها available = False داخل minerLevel
        unavailable_miners = []
        for miner in miners:
            miner_levels = miner.get('minerLevel', [])
            for level in miner_levels:
                if level.get('available') == False:
                    unavailable_miners.append(level)

        # كتابة IDs الخاصة بالـ miners غير المتاحين إلى ملف
        with open('firstbuy.txt', 'w') as file:
            for miner in unavailable_miners:
                file.write(f"{miner.get('id')}\n")

        print(f"تم استخراج وكتابة {len(unavailable_miners)} من miners غير المتاحين إلى الملف firstbuy.txt.txt'")

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response")
    except KeyError:
        print("Unexpected data structure in response")




def get_user_mine_id(token):
    url = "https://api.goblinmine.game/graphql"
    
    payload = json.dumps({
        "operationName": "minesAndCheckTasksCompleted",
        "variables": {
            "worldId": 1
        },
        "query": "query minesAndCheckTasksCompleted($worldId: Int!) {\n  mines(worldId: $worldId) {\n    ...MINE_FRAGMENT\n    __typename\n  }\n  check_tasks_completed(worldId: $worldId)\n}\n\nfragment MINE_FRAGMENT on MineFool {\n  deposit_day\n  goblin_image\n  id\n  image\n  income_per_day\n  level\n  miner_amount\n  name\n  price\n  user_miners_count\n  volume\n  userMine {\n    auto\n    cart_level\n    deposit_day\n    deposit_day_default\n    extracted_amount\n    extracted_percent\n    id\n    income_hour\n    next_volume\n    updateIn\n    volume\n    updated_at\n    total_day\n    __typename\n  }\n  currency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  miningCurrency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  __typename\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    response = requests.post(url, data=payload, headers=headers)
    re = response.json()
    #print(f"wha i do :{re}")
   

    user_mine_id = None
    for mine in re['data']['mines']:
        if mine['name'] == f"Шахта {set}" and 'userMine' in mine:
            user_mine_id = mine['userMine']['id']
            break

    if user_mine_id:
        return int(user_mine_id)
    else:
        return None

def get_cart_id_by_price(token):
    user_mine_id = get_user_mine_id(token)
    if user_mine_id is None:
        print("Error: userMine ID not found, cannot proceed.")
        return

    url = "https://api.goblinmine.game/graphql"
    
    # يجب استبدال 'set' بقيمة رقمية صحيحة
    mine_id = 1  # على سبيل المثال، قم بتحديث هذا حسب الحاجة

    payload = json.dumps({
      "operationName": "carts",
      "variables": {
        "mineId": mine_id,
        "userMineId": user_mine_id
      },
      "query": "query carts($mineId: Int!, $userMineId: Int!) {\n  carts(mineId: $mineId, userMineId: $userMineId) {\n    auto\n    available\n    id\n    image\n    level\n    name\n    price\n    volume\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    miningCurrency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code != 200:
        print(f"Error: Request failed with status code {response.status_code}")
        print("Response content:", response.text)
        return

    re = response.json()
    if 'data' not in re or 'carts' not in re['data']:
        print("Error: 'data' or 'carts' key is missing in the response.")
        print("Response content:", re)
        return

    # استخراج "id" حيث تكون "available" هي False
    unavailable_carts = [cart['id'] for cart in re['data']['carts'] if not cart['available']]
    
    # حفظ القيم في ملف cartid.txt
    with open("cartid.txt", "w") as file:
        for cart_id in unavailable_carts:
            file.write(f"{cart_id}\n")
    print("IDs with 'available' as False have been saved to cartid.txt.")

# استدعاء الدالة


def update_cart_status(token):
    url = "https://api.goblinmine.game/graphql"

    # قراءة قيم id من الملف الخارجي
    try:
        with open("cartid.txt", "r") as file:
            cart_ids = [int(line.strip()) for line in file if line.strip().isdigit()]
    except FileNotFoundError:
        print("Error: cartid.txt file not found.")
        return

    for cart_id in cart_ids:
        # إعداد البيانات مع تحديد ID المطلوب
        payload = json.dumps({
          "operationName": "updateCart",
          "variables": {
            "id": cart_id
          },
          "query": "mutation updateCart($id: Int!) {\n  updateCart(id: $id) {\n    volume\n    status\n    message\n    __typename\n  }\n}"
        })

        headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

        # إرسال الطلب
        response = requests.post(url, data=payload, headers=headers)
        response_data = response.json()

        # استخراج status من الاستجابة
        status = response_data.get('data', {}).get('updateCart', {}).get('status')
        print(f"Cart ID {cart_id}: Status - {status if status is not None else 'Status not found'}")
        time.sleep(5)

# استدعاء الدالة مع إدخال رمز التوكن


# استدعاء الدالة مع معرف الـ Cart المطلوب



def mine_and_miners(token):
    url = "https://api.goblinmine.game/graphql"
    
    # تجهيز البيانات للطلب
    payload = {
        "operationName": "mineAndMiners",
        "variables": {
            "mineId": set
        },
        "query": """
            query mineAndMiners($mineId: Int!) {
              mine(mineId: $mineId) {
                ...MINE_FRAGMENT
                __typename
              }
              miners(mineId: $mineId) {
                ...MINERS_FRAGMENT
                __typename
              }
            }

            fragment MINE_FRAGMENT on MineFool {
              deposit_day
              goblin_image
              id
              image
              income_per_day
              level
              miner_amount
              name
              price
              user_miners_count
              volume
              userMine {
                auto
                cart_level
                deposit_day
                deposit_day_default
                extracted_amount
                extracted_percent
                id
                income_hour
                next_volume
                updateIn
                volume
                updated_at
                total_day
                __typename
              }
              currency {
                ...CURRENCY_FRAGMENT
                __typename
              }
              miningCurrency {
                ...CURRENCY_FRAGMENT
                __typename
              }
              __typename
            }

            fragment CURRENCY_FRAGMENT on Currency {
              id
              amount
              coefficient
              icon
              name
              __typename
            }

            fragment MINERS_FRAGMENT on Miners {
              available
              id
              level
              name
              price
              currency {
                ...CURRENCY_FRAGMENT
                __typename
              }
              minerLevel {
                available
                disabled
                existInventoryLevel
                id
                image
                income_hour
                level
                name
                price
                inventoryLevel {
                  level
                  name
                  __typename
                }
                currency {
                  ...CURRENCY_FRAGMENT
                  __typename
                }
                __typename
              }
              __typename
            }
        """
    }

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام json=payload
    response = requests.post(url, json=payload, headers=headers)

    # طباعة الاستجابة إذا كانت تحتوي على "message"
    if response.status_code == 200:
        try:
            response_data = response.json()
            # استخراج بيانات mine
            mine_data = response_data.get("data", {}).get("mine", {})
            if mine_data:
                # استخراج قيمة user_miners_count
                user_miners_count = mine_data.get("user_miners_count", "Not Found")
                print(Fore.GREEN + f"user_miners_count: {user_miners_count}")   
                print(Fore.CYAN+ f"Acc Blance is: {get_bronze_world_balance(token)}")
                if user_miners_count == 45:
                	print(Fore.YELLOW+f"Your Miner Is Full {user_miners_count} Change To next set..")
                	target = int(input(Fore.YELLOW+ "How many Gather Gold claim:  "))
                	while True:                		          		                		                		
                		bl = get_bronze_world_balance(token)
                		print(Fore.CYAN+ f"Acc Blance is: {bl}")
                		pickup_mine(token)
                		fetch_mines_and_check_tasks2(token) 
                		print(Fore.LIGHTBLACK_EX+ 'Watting 60 s...')
                		if target == bl:
                			print(Fore.GREEN+ f"Your Target is done your Blance is : {bl} Go Buy Next Set ")
                			break
                		time.sleep(60)
                	
                	
                
                #elif bl >= 20000:
#                	target_price = 20000
#                	cart_id = get_cart_id_by_price(token,target_price)                
#                	print(Fore.GREEN+ f"Now Buy Cart: {cart_id}")
#                	update_cart_status(token,cart_id)
#                elif bl >= 50000:
#                	target_price = 20000
#                	cart_id = get_cart_id_by_price(token,target_price)                
#                	print(Fore.GREEN+ f"Now Buy Cart: {cart_id}")
#                	update_cart_status(token,cart_id)                   	               	                	                	
            else:
                print(Fore.RED + "No mine data found in the response.")

        except json.JSONDecodeError:
            print(Fore.RED + "Failed to decode the response as JSON.")
    else:
        print(Fore.RED + f"Request failed with status code: {response.status_code}")
        print(Fore.YELLOW + f"Response content: {response.text}")
    

# solt buy
def buy_miner(token):
    url = "https://api.goblinmine.game/graphql"
    payload = {
        "operationName": "buyMiner",
        "variables": {
            "input": {
                "minerId": set
            }
        },
        "query": "mutation buyMiner($input: BuyMinerInput!) {\n  buyMiner(input: $input) {\n    message\n    status\n  }\n}"
    }
    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # التحقق من وجود البيانات اللازمة قبل الوصول إليها
        if data.get("data") and data["data"].get("buyMiner"):
            message = data["data"]["buyMiner"]["message"]
            if message == "Exists":
                print(Fore.GREEN + "You alrady Buying it")
            else:
                print(Fore.GREEN + f"Buy Done {message}")
        else:
            print(Fore.RED + "Error: Unexpected response format during buyMiner.")
    else:
        print(Fore.RED + "Failed to send buyMiner request.")
#worker buy
def read_miner_level_id(file_path, index):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            if index < len(lines):
                return lines[index].strip()  # إرجاع القيمة عند الفهرس المحدد
            else:
                return None  # إذا كانت هناك قيم أكثر
    except FileNotFoundError:
        print(f"الملف {file_path} غير موجود.")
        return None
        
def get_inventory(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "inventory",
        "variables": {
            "mineId": set
        },
        "query": "query inventory($mineId: Int!) {\n  inventory(mineId: $mineId) {\n    disabled\n    id\n    image\n    income_hour\n    level\n    name\n    price\n    inventory_income_hour\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # تحقق من حالة الاستجابة
    if response.status_code == 200:
        data = response.json()  # تحويل الاستجابة إلى JSON
        inventory = data.get("data", {}).get("inventory", [])  # استخراج قائمة الأدوات من الاستجابة

        # البحث عن "Pickaxe" وحفظ القيم في متغيرات
        for item in inventory:
            if item.get("name") == "Pickaxe":
                # تخزين القيم في متغيرات
                pickaxe_id = item["id"]
                pickaxe_name = item["name"]
                

                # طباعة القيم
                print(f"Pickaxe ID: {pickaxe_id}")
                print(f"Pickaxe Name: {pickaxe_name}")
                
                
                # يمكنك استخدام المتغيرات لاحقاً في مكان آخر في الكود
                return  pickaxe_id# إذا كنت ترغب في التوقف بعد العثور عليها
        else:
            print("Pickaxe not found in inventory.")
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)
def get_Jack(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "inventory",
        "variables": {
            "mineId": set
        },
        "query": "query inventory($mineId: Int!) {\n  inventory(mineId: $mineId) {\n    disabled\n    id\n    image\n    income_hour\n    level\n    name\n    price\n    inventory_income_hour\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # تحقق من حالة الاستجابة
    if response.status_code == 200:
        data = response.json()  # تحويل الاستجابة إلى JSON
        inventory = data.get("data", {}).get("inventory", [])  # استخراج قائمة الأدوات من الاستجابة

        # البحث عن "Pickaxe" وحفظ القيم في متغيرات
        for item in inventory:
            if item.get("name") == "Jackhammer":
                # تخزين القيم في متغيرات
                Jackhammerid = item["id"]
                Jackhammer = item["name"]
                

                # طباعة القيم
                print(f"Jackhammer ID: {Jackhammerid}")
                print(f"Jackhammerid Name: {Jackhammer}")
                
                
                # يمكنك استخدام المتغيرات لاحقاً في مكان آخر في الكود
                return  Jackhammerid 
        else:
            print("Pickaxe not found in inventory.")
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)
        
 #Foremansid       
def get_Foremans(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "inventory",
        "variables": {
            "mineId": set
        },
        "query": "query inventory($mineId: Int!) {\n  inventory(mineId: $mineId) {\n    disabled\n    id\n    image\n    income_hour\n    level\n    name\n    price\n    inventory_income_hour\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # تحقق من حالة الاستجابة
    if response.status_code == 200:
        data = response.json()  # تحويل الاستجابة إلى JSON
        inventory = data.get("data", {}).get("inventory", [])  # استخراج قائمة الأدوات من الاستجابة

        # البحث عن "Pickaxe" وحفظ القيم في متغيرات
        for item in inventory:
            if item.get("name") == "Foreman's helmet":
                # تخزين القيم في متغيرات
                Foremansid = item["id"]
                Foremanss = item["name"]
                

                # طباعة القيم
                print(f"Foremans ID: {Foremansid}")
                print(f"Foremans Name: {Foremanss}")
                
                
                # يمكنك استخدام المتغيرات لاحقاً في مكان آخر في الكود
                return  Foremansid 
        else:
            print("Pickaxe not found in inventory.")
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)        
 #formeans
def Foremans(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "buyInventory",
        "variables": {
            "id": get_Foremans(token)
        },
        "query": "mutation buyInventory($id: Int!) {\n  buyInventory(id: $id) {\n    message\n    volume\n    status\n    __typename\n  }\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # طباعة الاستجابة
    if response.status_code == 200:
        print("Response:", response.text)
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)
        
                      
def Pickaxe(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "buyInventory",
        "variables": {
            "id": get_inventory(token)
        },
        "query": "mutation buyInventory($id: Int!) {\n  buyInventory(id: $id) {\n    message\n    volume\n    status\n    __typename\n  }\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # طباعة الاستجابة
    if response.status_code == 200:
        print("Response:", response.text)
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)
        

       
def get_ForemansFoldet(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "inventory",
        "variables": {
            "mineId": set
        },
        "query": "query inventory($mineId: Int!) {\n  inventory(mineId: $mineId) {\n    disabled\n    id\n    image\n    income_hour\n    level\n    name\n    price\n    inventory_income_hour\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # تحقق من حالة الاستجابة
    if response.status_code == 200:
        data = response.json()  # تحويل الاستجابة إلى JSON
        inventory = data.get("data", {}).get("inventory", [])  # استخراج قائمة الأدوات من الاستجابة

        # البحث عن "Pickaxe" وحفظ القيم في متغيرات
        for item in inventory:
            if item.get("name") == "Foreman's folder":
                # تخزين القيم في متغيرات
                Foremansfolderid = item["id"]
                Foremanss = item["name"]
                

                # طباعة القيم
                print(f"Foremans folderid ID: {Foremansfolderid}")
                print(f"Foremans folder Name: {Foremanss}")
                
                
                # يمكنك استخدام المتغيرات لاحقاً في مكان آخر في الكود
                return  Foremansfolderid 
        else:
            print("Pickaxe not found in inventory.")
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)        
 #formeans
def ForemansFolder(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "buyInventory",
        "variables": {
            "id": get_ForemansFoldet(token)
        },
        "query": "mutation buyInventory($id: Int!) {\n  buyInventory(id: $id) {\n    message\n    volume\n    status\n    __typename\n  }\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # طباعة الاستجابة
    if response.status_code == 200:
        print("Response:", response.text)
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)              
                     
def get_Directors(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "inventory",
        "variables": {
            "mineId": set
        },
        "query": "query inventory($mineId: Int!) {\n  inventory(mineId: $mineId) {\n    disabled\n    id\n    image\n    income_hour\n    level\n    name\n    price\n    inventory_income_hour\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # تحقق من حالة الاستجابة
    if response.status_code == 200:
        data = response.json()  # تحويل الاستجابة إلى JSON
        inventory = data.get("data", {}).get("inventory", [])  # استخراج قائمة الأدوات من الاستجابة

        # البحث عن "Pickaxe" وحفظ القيم في متغيرات
        for item in inventory:
            if item.get("name") == "Director's briefcase":
                # تخزين القيم في متغيرات
                Director = item["id"]
                Foremanss = item["name"]
                

                # طباعة القيم
                print(f"Foremansfolderid ID: {Director}")
                print(f"Foremans Name: {Foremanss}")
                
                
                # يمكنك استخدام المتغيرات لاحقاً في مكان آخر في الكود
                return  Director 
        else:
            print("Pickaxe not found in inventory.")
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)        
 #formeans
def Directorsbriefcase(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "buyInventory",
        "variables": {
            "id": get_Directors(token)
        },
        "query": "mutation buyInventory($id: Int!) {\n  buyInventory(id: $id) {\n    message\n    volume\n    status\n    __typename\n  }\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # طباعة الاستجابة
    if response.status_code == 200:
        print("Response:", response.text)
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)                                          
                                   
def get_badge(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "inventory",
        "variables": {
            "mineId": set
        },
        "query": "query inventory($mineId: Int!) {\n  inventory(mineId: $mineId) {\n    disabled\n    id\n    image\n    income_hour\n    level\n    name\n    price\n    inventory_income_hour\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # تحقق من حالة الاستجابة
    if response.status_code == 200:
        data = response.json()  # تحويل الاستجابة إلى JSON
        inventory = data.get("data", {}).get("inventory", [])  # استخراج قائمة الأدوات من الاستجابة

        # البحث عن "Pickaxe" وحفظ القيم في متغيرات
        for item in inventory:
            if item.get("name") == "Director's badge":
                # تخزين القيم في متغيرات
                badgee = item["id"]
                Foremanss = item["name"]
                

                # طباعة القيم
                print(f"Foremansfolderid ID: {badgee}")
                print(f"Foremans Name: {Foremanss}")
                
                
                # يمكنك استخدام المتغيرات لاحقاً في مكان آخر في الكود
                return  badgee
        else:
            print("Pickaxe not found in inventory.")
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)        
 #formeans
def badge(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "buyInventory",
        "variables": {
            "id": get_badge(token)
        },
        "query": "mutation buyInventory($id: Int!) {\n  buyInventory(id: $id) {\n    message\n    volume\n    status\n    __typename\n  }\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # طباعة الاستجابة
    if response.status_code == 200:
        print("Response:", response.text)
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)                                           

                                                        
def get_tnt(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "inventory",
        "variables": {
            "mineId": set
        },
        "query": "query inventory($mineId: Int!) {\n  inventory(mineId: $mineId) {\n    disabled\n    id\n    image\n    income_hour\n    level\n    name\n    price\n    inventory_income_hour\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # تحقق من حالة الاستجابة
    if response.status_code == 200:
        data = response.json()  # تحويل الاستجابة إلى JSON
        inventory = data.get("data", {}).get("inventory", [])  # استخراج قائمة الأدوات من الاستجابة

        # البحث عن "Pickaxe" وحفظ القيم في متغيرات
        for item in inventory:
            if item.get("name") == "Small TNT":
                # تخزين القيم في متغيرات
                tnt = item["id"]
                Foremanss = item["name"]
                

                # طباعة القيم
                print(f"Foremansfolderid ID: {tnt}")
                print(f"Foremans Name: {Foremanss}")
                
                
                # يمكنك استخدام المتغيرات لاحقاً في مكان آخر في الكود
                return  tnt
        else:
            print("Pickaxe not found in inventory.")
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)        
 #formeans
def SmallTNT(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "buyInventory",
        "variables": {
            "id": get_tnt(token)
        },
        "query": "mutation buyInventory($id: Int!) {\n  buyInventory(id: $id) {\n    message\n    volume\n    status\n    __typename\n  }\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # طباعة الاستجابة
    if response.status_code == 200:
        print("Response:", response.text)
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)                                                     
def get_TNT(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "inventory",
        "variables": {
            "mineId": set
        },
        "query": "query inventory($mineId: Int!) {\n  inventory(mineId: $mineId) {\n    disabled\n    id\n    image\n    income_hour\n    level\n    name\n    price\n    inventory_income_hour\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # تحقق من حالة الاستجابة
    if response.status_code == 200:
        data = response.json()  # تحويل الاستجابة إلى JSON
        inventory = data.get("data", {}).get("inventory", [])  # استخراج قائمة الأدوات من الاستجابة

        # البحث عن "Pickaxe" وحفظ القيم في متغيرات
        for item in inventory:
            if item.get("name") == "TNT":
                # تخزين القيم في متغيرات
                TNTt = item["id"]
                Foremanss = item["name"]
                

                # طباعة القيم
                print(f"Foremansfolderid ID: {TNTt}")
                print(f"Foremans Name: {Foremanss}")
                
                
                # يمكنك استخدام المتغيرات لاحقاً في مكان آخر في الكود
                return  TNTt
        else:
            print("Pickaxe not found in inventory.")
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)        
 #formeans
def TNT(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "buyInventory",
        "variables": {
            "id": get_TNT(token)
        },
        "query": "mutation buyInventory($id: Int!) {\n  buyInventory(id: $id) {\n    message\n    volume\n    status\n    __typename\n  }\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # طباعة الاستجابة
    if response.status_code == 200:
        print("Response:", response.text)
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)                                                        
def Jackhammer(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "buyInventory",
        "variables": {
            "id": get_Jack(token)
        },
        "query": "mutation buyInventory($id: Int!) {\n  buyInventory(id: $id) {\n    message\n    volume\n    status\n    __typename\n  }\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام requests.post
    response = requests.post(url, data=payload, headers=headers)

    # طباعة الاستجابة
    if response.status_code == 200:
        print("Response:", response.text)
    else:
        print(f"Error occurred: {response.status_code}")
        print(response.text)
# دالة لشراء مستوى المعدن
user_mine_ids = []  # قائمة لتخزين جميع معرفات userMine
ids = []  # قائمة لتخزين جميع المعرفات

def fetch_mines_and_check_tasks2(token):
    global user_mine_ids, ids  # تحديد المتغيرات كعالمية

    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "minesAndCheckTasksCompleted",
        "variables": {
            "worldId": 1
        },
        "query": """
        query minesAndCheckTasksCompleted($worldId: Int!) {
          mines(worldId: $worldId) {
            ...MINE_FRAGMENT
            __typename
          }
          check_tasks_completed(worldId: $worldId)
        }

        fragment MINE_FRAGMENT on MineFool {
          deposit_day
          goblin_image
          id
          image
          income_per_day
          level
          miner_amount
          name
          price
          user_miners_count
          volume
          userMine {
            auto
            cart_level
            deposit_day
            deposit_day_default
            extracted_amount
            extracted_percent
            id
            income_hour
            next_volume
            updateIn
            volume
            updated_at
            total_day
            __typename
          }
          currency {
            ...CURRENCY_FRAGMENT
            __typename
          }
          miningCurrency {
            ...CURRENCY_FRAGMENT
            __typename
          }
          __typename
        }

        fragment CURRENCY_FRAGMENT on Currency {
          id
          amount
          coefficient
          icon
          name
          __typename
        }
        """
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    try:
        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            
            if "data" in data and "mines" in data["data"]:
                mines = data["data"]["mines"]
                
                for mine in mines:
                    user_mine = mine.get("userMine")
                    if user_mine:
                        # استخراج القيم المطلوبة
                        deposit_day_default = user_mine.get("deposit_day_default")
                        total_day = user_mine.get("total_day")
                        user_mine_id = user_mine.get("id")  # استخراج userMine ID
                        
                        # تحقق إذا كانت deposit_day_default تساوي total_day
                        if deposit_day_default == total_day:
                            ids.append(mine.get("id"))  # إضافة معرف mine إلى القائمة
                            user_mine_ids.append(user_mine_id)  # إضافة userMine ID إلى القائمة
                            print(Fore.GREEN + f"Condition met! User Mine ID: {user_mine_id}")
                            time.sleep(30)
                            process_upgrade(token)
                        else:
                            print(Fore.YELLOW + f"Condition not met for Mine ID: {mine.get('id')}")
                            
                            print(Fore.CYAN + f"Deposit Day Default: {deposit_day_default}")
                            print(Fore.CYAN + f"Total Day: {total_day}")
            
            else:
                print(Fore.RED + "No mines data found in the response.")
        else:
            print(Fore.RED + f"Failed to fetch data. Status code: {response.status_code}")
    
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")
        return None

def buy_miner_level(token, file_path, index):
    url = "https://api.goblinmine.game/graphql"

    # جلب minerLevelId من الملف
    miner_level_id = read_miner_level_id(file_path, index)
    if miner_level_id is None:
        print("لا توجد قيم لقراءة minerLevelId أو تم الوصول إلى النهاية.")
        return None

    # تجهيز البيانات للطلب
    payload = {
        "operationName": "buyMinerLevel",
        "variables": {
            "input": {
                "minerLevelId": int(miner_level_id)
            }
        },
        "query": "mutation buyMinerLevel($input: BuyMinerLevelInput!) {\n  buyMinerLevel(input: $input) {\n    balance\n    message\n    status\n    __typename\n  }\n}"
    }
    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب باستخدام json=payload
    response = requests.post(url, json=payload, headers=headers)

    # التحقق من الاستجابة
    if response.status_code == 400:
        print(f"حدث خطأ في الطلب: {response.status_code}")
        print(f"محتوى الاستجابة: {response.text}")
        return None

    if response.status_code == 200:
        try:
            # تحويل الاستجابة إلى JSON
            response_data = response.json()

            # التحقق من وجود البيانات المطلوبة
            data = response_data.get("data", {})
            if not data:
                print("لا توجد بيانات في الاستجابة.")
                return None

            buy_miner_level = data.get("buyMinerLevel", {})
            if not buy_miner_level:
                print("لا توجد بيانات buyMinerLevel في الاستجابة.")
                return None

            # استخراج الرسالة
            message = buy_miner_level.get("message", "Message not found")
            print(Fore.GREEN + f"Worker Id Try : [{miner_level_id}] Status : {message}")
            

            # استدعاء المهام بناءً على الرسالة
            fetch_mines_and_check_tasks2(token)
            if "Jackhammer" in message or "JACKHAMMER" in message:
                print(Fore.GREEN + "UPGRADE Jackhammer Done")
                Jackhammer(token)
            elif "Pickaxe" in message:
                print(Fore.GREEN + "Done UPGRADE Pickaxe")
                Pickaxe(token)
            elif "Foreman's helmet" in message:
                print(Fore.GREEN + "Done UPGRADE Foreman's helmet")
                Foremans(token)
            elif "Foreman's folder" in message:
                print(Fore.GREEN + "Done UPGRADE ForemansFolder")
                ForemansFolder(token)
                time.sleep(30)
                SmallTNT(token)
                time.sleep(30)
                TNT(token)
            elif "Director's briefcase" in message:
                print(Fore.GREEN + "Done UPGRADE Director's briefcase")
                Directorsbriefcase(token)
                time.sleep(30)
                SmallTNT(token)
                time.sleep(30)
                TNT(token)
            elif "Director's badge" in message:
                print(Fore.GREEN + "Done UPGRADE Director's badge")
                badge(token)
                time.sleep(30)
                SmallTNT(token)
                time.sleep(30)
                TNT(token)

        except json.JSONDecodeError:
            print("فشل في تحويل الاستجابة إلى JSON.")
    else:
        print(f"حدث خطأ غير معروف في الطلب: {response.status_code}")
        print(f"محتوى الاستجابة: {response.text}")

    return miner_level_id


def fetch_and_save_upgrade_ids(token):
    url = "https://api.goblinmine.game/graphql"
    payload = json.dumps({
        "operationName": "mineAndUpgradeMine",
        "variables": {
            "mineId": set
        },
        "query": "query mineAndUpgradeMine($mineId: Int!) {\n  mine(mineId: $mineId) {\n    ...MINE_FRAGMENT\n    __typename\n  }\n  upgradeMine(mineId: $mineId) {\n    ...UPGRADE_MINE_FRAGMENT\n    __typename\n  }\n}\n\nfragment MINE_FRAGMENT on MineFool {\n  deposit_day\n  goblin_image\n  id\n  image\n  income_per_day\n  level\n  miner_amount\n  name\n  price\n  user_miners_count\n  volume\n  userMine {\n    auto\n    cart_level\n    deposit_day\n    deposit_day_default\n    extracted_amount\n    extracted_percent\n    id\n    income_hour\n    next_volume\n    updateIn\n    volume\n    updated_at\n    total_day\n    __typename\n  }\n  currency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  miningCurrency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  __typename\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}\n\nfragment UPGRADE_MINE_FRAGMENT on upgradeMine {\n  id\n  image\n  level\n  name\n  price\n  disabled\n  deposit_day\n  currency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  need_inventory {\n    level\n    name\n    __typename\n  }\n  __typename\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب والحصول على الاستجابة
    response = requests.post(url, data=payload, headers=headers)
    data = response.json()

    # استخراج قيم 'id' التي تكون 'disabled' فيها False
    ids_with_disabled_false = [
        item['id'] for item in data.get("data", {}).get("upgradeMine", [])
        if item.get("disabled") is False
    ]

    # حفظ القيم في ملف
    with open("upgrademine.txt", "w") as file:
        for id_value in ids_with_disabled_false:
            file.write(f"{id_value}\n")

    print("تم حفظ IDs بنجاح في ملف upgrademine.txt")





def process_upgrade(token):
    
    try:
        # تحميل الـ IDs من الملف
        with open('upgrademine.txt', 'r') as file:
            upgrade_ids = [line.strip() for line in file.readlines()]

        # إذا كانت القائمة فارغة
        if not upgrade_ids:
            print(Fore.RED + "لا يوجد أي IDs للمعالجة.")
            return

        # تحميل الموضع الحالي من ملف آخر
        try:
            with open('last_position.txt', 'r') as pos_file:
                current_position = int(pos_file.read().strip())
        except FileNotFoundError:
            current_position = 0  # إذا لم يكن الملف موجودًا، ابدأ من البداية

        # التحقق من الموضع الحالي
        if current_position >= len(upgrade_ids):
            print(Fore.YELLOW + "تم الوصول إلى نهاية قائمة IDs. سيتم البدء من جديد.")
            current_position = 0

        # الحصول على ID الحالي
        upgrade_id = upgrade_ids[current_position]

        # تحديث الموضع وحفظه
        next_position = current_position + 1
        with open('last_position.txt', 'w') as pos_file:
            pos_file.write(str(next_position))

        # إعداد البيانات لإرسالها
        url = "https://api.goblinmine.game/graphql"
        payload = json.dumps({
            "operationName": "buyUpgradeMine",
            "variables": {
                "id": int(upgrade_id)  # تحويل الـ ID إلى int
            },
            "query": "mutation buyUpgradeMine($id: Int!) {\n  buyUpgradeMine(id: $id) {\n    message\n    status\n    volume\n    __typename\n  }\n}"
        })

        headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

        # إرسال الطلب
        response = requests.post(url, data=payload, headers=headers)

        # التحقق من حالة الاستجابة
        if response.status_code == 200:
            try:
                # تحويل الاستجابة إلى JSON
                response_data = response.json()
                upgrade_data = response_data.get("data", {}).get("buyUpgradeMine", {})

                # التحقق من وجود البيانات المطلوبة
                if not upgrade_data:
                    print(Fore.YELLOW + "لم يتم العثور على بيانات الترقية في الاستجابة.")
                    return

                # استخراج التفاصيل
                message = upgrade_data.get("message", "لم يتم العثور على الرسالة.")
                status = upgrade_data.get("status", "غير معروف")
                

                # طباعة النتائج
                print(Fore.GREEN + f"Upgrade ID: {upgrade_id}")
                print(Fore.GREEN + f"Status: {status}")
                print(Fore.CYAN + f"Message: {message}")
                time.sleep(60)
                

            except json.JSONDecodeError:
                print(Fore.RED + "فشل في تحويل الاستجابة إلى JSON.")
        else:
            print(Fore.RED + f"حدث خطأ: {response.status_code}")
            print(Fore.YELLOW + f"تفاصيل الخطأ: {response.text}")

    except FileNotFoundError:
        print(Fore.RED + "الملف 'upgrademine.txt' غير موجود.")
    except ValueError as ve:
        print(Fore.RED + f"خطأ في تحويل ID إلى رقم: {ve}")
    except Exception as e:
        print(Fore.RED + f"حدث خطأ غير متوقع: {e}")

# دالة رئيسية لاستدعاء الدالة مع الـ token
# متغير خارجي لحفظ الحالة
current_index = 0
user_mineids = []  # قائمة لتخزين معرفات user_mineid

def fetch_mines_and_check_tasks(token):
    global current_index, user_mineids

    url = "https://api.goblinmine.game/graphql"
    payload = json.dumps({
        "operationName": "minesAndCheckTasksCompleted",
        "variables": {
            "worldId": 1
        },
        "query": """
        query minesAndCheckTasksCompleted($worldId: Int!) {
          mines(worldId: $worldId) {
            ...MINE_FRAGMENT
            __typename
          }
          check_tasks_completed(worldId: $worldId)
        }

        fragment MINE_FRAGMENT on MineFool {
          deposit_day
          goblin_image
          id
          image
          income_per_day
          level
          miner_amount
          name
          price
          user_miners_count
          volume
          userMine {
            auto
            cart_level
            deposit_day
            deposit_day_default
            extracted_amount
            extracted_percent
            id
            income_hour
            next_volume
            updateIn
            volume
            updated_at
            total_day
            __typename
          }
          currency {
            ...CURRENCY_FRAGMENT
            __typename
          }
          miningCurrency {
            ...CURRENCY_FRAGMENT
            __typename
          }
          __typename
        }

        fragment CURRENCY_FRAGMENT on Currency {
          id
          amount
          coefficient
          icon
          name
          __typename
        }
        """
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    try:
        # إذا كانت القائمة فارغة، استرجع البيانات واملأ القائمة
        if not user_mineids:
            response = requests.post(url, data=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "mines" in data["data"]:
                    mines = data["data"]["mines"]
                    for mine in mines:
                        user_mine = mine.get("userMine")
                        if user_mine:                            
                            user_mineids.append(user_mine.get("id"))                           
                else:
                    print("No mines found.")
            else:
                print("Request failed with status code:", response.status_code)
                print("Response content:", response.text)

        # طباعة المعرف الحالي في القائمة
        if user_mineids:
            print(Fore.GREEN + f"Current user_mine ID: {user_mineids[current_index]}")

            # تحديث المؤشر للمرة القادمة
            current_index = (current_index + 1) % len(user_mineids)  # العودة للبداية بعد الوصول للنهاية

    except Exception as e:
        print(f"An error occurred: {e}")
        


def pickup_mine(token):
    # استدعاء الدالة لجلب المعرّف وتنفيذ المهام المطلوبة في الدالة fetch_mines_and_check_tasks
    fetch_mines_and_check_tasks(token)
    
    # تحقق من وجود معرفات في القائمة قبل تنفيذ المهمة
    if user_mineids:
        mine_id = user_mineids[current_index]  # استخدام المعرّف الحالي

        url = "https://api.goblinmine.game/graphql"
        payload = json.dumps({
            "operationName": "pickUp",
            "variables": {
                "input": {
                    "mineId": mine_id,
                    "worldId": set
                }
            },
            "query": "mutation pickUp($input: PickUpMineInput!) {\n  pickUp(input: $input) {\n    total\n    __typename\n  }\n}"
        })

        headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

        response = requests.post(url, data=payload, headers=headers)

        if response.status_code == 200:
            print(Fore.GREEN + f"Claiming Done for mine ID: {mine_id}")
        else:
            print(Fore.RED + "Error Claiming")
    else:
        print("No user mine IDs available to pick up.")

def fetch_task_ids(token):
    url = "https://api.goblinmine.game/graphql"
    
    payload = json.dumps({
        "operationName": "dailyBonusAndTasks",
        "variables": {
            "worldId": 1
        },
        "query": "query dailyBonusAndTasks($worldId: Int!) {\n  dailyBonus {\n    ...DAILY_BONUS_FRAGMENT\n    __typename\n  }\n  tasks(worldId: $worldId) {\n    ...TASK_FRAGMENT\n    __typename\n  }\n}\n\nfragment DAILY_BONUS_FRAGMENT on DailyBonus {\n  amount\n  available\n  day\n  is_done\n  currency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  __typename\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}\n\nfragment TASK_FRAGMENT on Task {\n  amount\n  id\n  image\n  status\n  title\n  url\n  currency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  __typename\n}"
    })
    
    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}
    
    # إرسال الطلب
    response = requests.post(url, data=payload, headers=headers)
    re = response.json()
    
    # استخراج وحفظ task IDs في ملف نصي
    if "data" in re and "tasks" in re["data"]:
        task_ids = [task["id"] for task in re["data"]["tasks"]]
        
        # كتابة task IDs فقط في ملف نصي
        with open("taskId.txt", "w") as file:
            for task_id in task_ids:
                file.write(f"{task_id}\n")
        
        print("تم حفظ task IDs في الملف taskId.txt.")
    else:
        print("لم يتم العثور على بيانات المهام في الاستجابة.")

# استدعاء الدالة


def check_all_task_statuses(token,file_path="taskId.txt"):
    # قراءة جميع taskId من الملف
    try:
        with open(file_path, "r") as file:
            task_ids = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("الملف taskId.txt غير موجود.")
        return

    # إعدادات الطلب
    url = "https://api.goblinmine.game/graphql"
    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # تكرار الطلب لكل taskId
    for task_id in task_ids:
        payload = json.dumps({
            "operationName": "checkTask",
            "variables": {
                "taskId": int(task_id)
            },
            "query": "mutation checkTask($taskId: Int!) {\n  checkTask(taskId: $taskId) {\n    message\n    status\n    __typename\n  }\n}"
        })

        # إرسال الطلب وجلب الاستجابة
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            status = response_data.get("data", {}).get("checkTask", {}).get("status", "Status not found")
            print(f"Task ID: {task_id}, Status: {status}")
            time.sleep(10)
        else:
            print(f"Error with Task ID {task_id}: Status Code {response.status_code}")

# استدعاء الدالة للتحقق من جميع Task IDs

def give_bonus(token):
    url = "https://api.goblinmine.game/graphql"
    payload = json.dumps({
        "operationName": "giveBonus",
        "variables": {},
        "query": "mutation giveBonus {\n  giveBonus {\n    message\n    status\n    volume\n    __typename\n  }\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    # إرسال الطلب وجلب الاستجابة
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        # استخراج `message` من الاستجابة
        message = response_data.get("data", {}).get("giveBonus", {}).get("message", "No message found")
        print(Fore.LIGHTRED_EX+f"Status Of Bouns : {message}")
    else:
        print("Failed to fetch data. Status code:", response.status_code)

#solt save 
def extract_and_save_miner_ids(token):
    url = "https://api.goblinmine.game/graphql"

    payload = json.dumps({
        "operationName": "mineAndMiners",
        "variables": {
            "mineId": set
        },
        "query": "query mineAndMiners($mineId: Int!) {\n  mine(mineId: $mineId) {\n    ...MINE_FRAGMENT\n    __typename\n  }\n  miners(mineId: $mineId) {\n    ...MINERS_FRAGMENT\n    __typename\n  }\n}\n\nfragment MINE_FRAGMENT on MineFool {\n  deposit_day\n  goblin_image\n  id\n  image\n  income_per_day\n  level\n  miner_amount\n  name\n  price\n  user_miners_count\n  volume\n  userMine {\n    auto\n    cart_level\n    deposit_day\n    deposit_day_default\n    extracted_amount\n    extracted_percent\n    id\n    income_hour\n    next_volume\n    updateIn\n    volume\n    updated_at\n    total_day\n    __typename\n  }\n  currency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  miningCurrency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  __typename\n}\n\nfragment CURRENCY_FRAGMENT on Currency {\n  id\n  amount\n  coefficient\n  icon\n  name\n  __typename\n}\n\nfragment MINERS_FRAGMENT on Miners {\n  available\n  id\n  level\n  name\n  price\n  currency {\n    ...CURRENCY_FRAGMENT\n    __typename\n  }\n  minerLevel {\n    available\n    disabled\n    existInventoryLevel\n    id\n    image\n    income_hour\n    level\n    name\n    price\n    inventoryLevel {\n      level\n      name\n      __typename\n    }\n    currency {\n      ...CURRENCY_FRAGMENT\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"
    })

    headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

    response = requests.post(url, data=payload, headers=headers)

    # جلب الاستجابة
    re = response.json()

    # استخراج الأيدي التي تحتوي على قيمة 'False' في 'available'
    miners = re.get('data', {}).get('miners', [])

    # فتح الملف 'soltid.txt' لكتابة الأيدي المستخرجة
    with open('soltid.txt', 'w') as file:
        for miner in miners:
            available = miner.get('available')
            if available == False:  # إذا كانت القيمة False
                miner_id = miner.get('id')  # استخراج ID المعدن
                file.write(f"{miner_id}\n")  # كتابة الـ ID في الملف

    print("تم إضافة الأيدي إلى الملف soltid.txt")
       

# استدعاء الدالة مع إدخال التوكن

#solt
def buy_miners_from_file(token):
    url = "https://api.goblinmine.game/graphql"
    
    # فتح الملف soltid.txt لقراءة الأيدي
    with open('soltid.txt', 'r') as file:
        miner_ids = file.readlines()

    # استدعاء لكل id بالترتيب
    for miner_id in miner_ids:
        miner_id = miner_id.strip()  # إزالة الفراغات الزائدة

        payload = json.dumps({
            "operationName": "buyMiner",
            "variables": {
                "input": {
                    "minerId": int(miner_id)  # التأكد من تحويله إلى عدد صحيح
                }
            },
            "query": "mutation buyMiner($input: BuyMinerInput!) {\n  buyMiner(input: $input) {\n    message\n    status\n    __typename\n  }\n}"
        })

        headers = {
  'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
  'Content-Type': "application/json",
  'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
  'app-b': "7246500f-89c5-4178-bdc3-d265b960b294",
  'accept-language': "en",
  'sec-ch-ua-mobile': "?1",
  'authorization': f"Bearer {token}",
  'sec-ch-ua-platform': "\"Android\"",
  'origin': "https://game.goblinmine.game",
  'sec-fetch-site': "same-site",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://game.goblinmine.game/"
}

        # إرسال الطلب
        response = requests.post(url, data=payload, headers=headers)
        result = response.json()

        # استخراج الحالة (status) من الاستجابة
        status = result.get('data', {}).get('buyMiner', {}).get('status', 'No status found')
        if "ok" in status:
        	print(Fore.LIGHTBLUE_EX+f"Miner Solt:  {miner_id} | Status: {status}")
        elif "fail" in status:
        	print(Fore.RED+f"You Buying Done Solt Number : {miner_id}")
        time.sleep(10)

def main():
    index = 0
    file_path = "firstbuy.txt"
    
    init_data = read_init_data()
    token, name = login(init_data)
    
    if token and name:        
        welcome_user(name, token)
        get_cart_id_by_price(token)            
        CatchWork(token)     
        give_bonus(token)
        buy_mine(token)  
        extract_and_save_miner_ids(token)
        buy_miners_from_file(token)
        fetch_and_save_upgrade_ids(token)
        fetch_task_ids(token)
        check_all_task_statuses(token)
        bl = get_bronze_world_balance(token)
        if bl >= 30000:
            print(Fore.GREEN + "Now Buy Cart")
            update_cart_status(token)
           
        while True:                       
            print(Fore.CYAN + "\nStarting new cycle of operations...\n")              
            
            if set == set:
                get_user_mine_id(token) 
                time.sleep(10)
                mine_and_miners(token)
                time.sleep(10)
                buy_miner(token)           
                time.sleep(30)
                pickup_mine(token)
                
                miner_level_id = buy_miner_level(token, file_path, index) 
                if miner_level_id is None:
                    CatchWork(token) 
                    print(Fore.YELLOW + "miner_level_id is None, continuing to next cycle...")
                    
                    index = 0
                    miner_level_id = buy_miner_level(token, file_path, index)
                else:
                    index += 1
                    print(Fore.CYAN + "Waiting for the next cycle...")

                       		 
            		 
             # انتظار 30 ثانية قبل تكرار الدورة

if __name__ == "__main__":
    main()
