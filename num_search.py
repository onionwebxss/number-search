import requests
import re
import json
from datetime import datetime

def print_banner():
    banner = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃Program for searching information     ┃
┃by Russian license plates from        ┃
┃the project owner                     ┃
┃Web Security Intelligentsia - @xss_com┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
"""
    print(banner)

def validate_and_format_phone(phone):
    phone = re.sub(r'\D', '', phone)
    
    if phone.startswith('8') and len(phone) == 11:
        return '7' + phone[1:]
    elif phone.startswith('7') and len(phone) == 11:
        return phone
    elif phone.startswith('9') and len(phone) == 10:
        return '7' + phone
    else:
        return None

def make_api_request(phone):
    url = f"https://api.depsearch.digital/quest={phone}?token=30L5ZJxVhQjNnMynqSYvGND80Gj3Xx7x&lang=ru"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response from API"}

def format_timestamp(timestamp_str):
    if not timestamp_str:
        return "Не указано"
    
    try:
        if 'T' in timestamp_str:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return timestamp_str
    except:
        return timestamp_str

def display_results(data):
    if "error" in data:
        print(f"\nError")
        return
    
    if not data.get("results"):
        print("\nПо данному номеру информация не найдена")
        return
    
    print(f"\n{'='*80}")
    print(f"{'='*80}")
    
    results = data["results"]
    
    for i, result in enumerate(results, 1):
        print("-" * 50)
        
        for key, value in result.items():
            if value is None or value == "":
                continue
                
            formatted_key = key
            formatted_value = str(value)
            
            if any(time_word in key.lower() for time_word in ['время', 'timestamp', 'дата', 'date']):
                formatted_value = format_timestamp(str(value))
            
            if len(formatted_value) > 100:
                formatted_value = formatted_value[:100] + "..."
            
            print(f"{formatted_key}: {formatted_value}")
    
    print(f"\n{'='*80}")
    print(f"{'='*80}")

def main():
    print_banner()
    
    while True:
        phone = input("Send Russian number> ").strip()
        
        if not phone:
            print("Пожалуйста, введите номер телефона")
            continue
        
        formatted_phone = validate_and_format_phone(phone)
        
        if not formatted_phone:
            print("Неверный формат номера. Используйте русский номер в формате: 79998887777, 89998887777 или 9998887777")
            continue
        
        print(f"Поиск информации для номера: +{formatted_phone}")
        print("Запрос к серверу...")
        
        data = make_api_request(formatted_phone)
        display_results(data)
        
        another = input("\nХотите выполнить еще один поиск? (y/n): ").strip().lower()
        if another != 'y':
            print("Bye Bye")
            break

if __name__ == "__main__":
    main()