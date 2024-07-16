import os
import time
import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

# ASCII art
ascii_art = r"""
 ______     ______     ______   ______     __  __     ______     ______     __  __    
/\  ___\   /\  __ \   /\  ___\ /\  __ \   /\ \_\ \   /\  __ \   /\  __ \   /\ \/ /    
\ \___  \  \ \ \/\ \  \ \  __\ \ \  __ \  \ \  __ \  \ \ \/\ \  \ \ \/\ \  \ \  _"-.  
 \/\_____\  \ \_____\  \ \_\    \ \_\ \_\  \ \_\ \_\  \ \_____\  \ \_____\  \ \_\ \_\ 
  \/_____/   \/_____/   \/_/     \/_/\/_/   \/_/\/_/   \/_____/   \/_____/   \/_/\/_/ 
                                                                                      
"""

# Function to clear console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main menu function
def main_menu():
    console = Console()
    clear_screen()

    console.print(ascii_art)

    # Display purple box for main menu
    console.print(Panel.fit(
        "[purple][1] Webhook Spammer.[/purple]\n"
        "[purple][2] Webhook Deleter.[/purple]\n"
        "[purple][3] Exit.[/purple]"
    ))

    choice = Prompt.ask("[blue]Enter your choice >>[/blue]")

    if choice == "1":
        webhook_spammer()
    elif choice == "2":
        webhook_deleter()
    elif choice == "3":
        console.print("[bold green]Exiting...[/bold green]")
        return
    else:
        console.print("[bold red]Invalid choice. Please enter 1, 2, or 3.[/bold red]")
        main_menu()

# Function to handle webhook spamming
def webhook_spammer():
    console = Console()
    clear_screen()

    console.print(ascii_art)

    console.print(Panel.fit(
        "[purple][1] Webhook Spammer.[/purple]"
    ))

    webhook_url = Prompt.ask("[blue][Webhook] >>[/blue]")
    message = Prompt.ask("[blue][Message] >>[/blue]")
    delay = float(Prompt.ask("[blue][Delay] >>[/blue]"))
    num_messages = int(Prompt.ask("[blue][Number of Messages] >>[/blue]"))

    start_spammer = Prompt.ask("[blue][Start spammer?] (y/n) >>[/blue]")

    if start_spammer.lower() == "y":
        console.print("[bold green]Starting spammer...[/bold green]")
        for message_count in range(1, num_messages + 1):
            response = requests.post(webhook_url, json={"content": message})
            if response.status_code == 204:
                console.print(f"[bold green]#{message_count} Successful[/bold green] Message -> {message} to webhook -> {webhook_url}")
            elif response.status_code == 429:
                retry_after = response.json().get("retry_after", 1) / 1000
                console.print(f"[yellow]Rate limited[/yellow] Cooling down... trying again in {retry_after}s.")
                time.sleep(retry_after)
                continue
            else:
                console.print(f"[bold red]Failed[/bold red] to send message to webhook -> {webhook_url}")
                break
            time.sleep(delay)
    else:
        console.print("[bold yellow]Spammer not started.[/bold yellow]")

    input("Press Enter to return to main menu...")
    main_menu()

# Function to handle webhook deletion
def webhook_deleter():
    console = Console()
    clear_screen()

    console.print(ascii_art)

    console.print(Panel.fit(
        "[purple][2] Webhook Deleter.[/purple]"
    ))

    webhook_url = Prompt.ask("[blue][Webhook] >>[/blue]")
    delete_confirmation = Prompt.ask("[blue][Delete webhook?] (y/n) >>[/blue]")

    if delete_confirmation.lower() == "y":
        response = requests.delete(webhook_url)
        if response.status_code == 204:
            console.print(f"[bold green]Successfully[/bold green] deleted webhook -> {webhook_url}")
        else:
            console.print(f"[bold red]Failed[/bold red] to delete webhook -> {webhook_url}")
    else:
        console.print("[bold yellow]Webhook not deleted.[/bold yellow]")

    input("Press Enter to return to main menu...")
    main_menu()

# Main entry point of the script
if __name__ == "__main__":
    main_menu()
