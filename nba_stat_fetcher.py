#Requirements: requests, rich, prompt_toolkit
#Usage: python nba_stat_fetcher.py


import requests
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

console = Console()

# Function to fetch and process NBA stats
def fetch_nba_stats(season="2024-25", stat_category="PTS"):
    url = f"https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season={season}&SeasonType=Regular%20Season&StatCategory={stat_category}"
    
    console.print("\n[bold green]Fetching NBA stats...[/bold green]")
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Fetching data...", total=100)
        
        response = requests.get(url)
        for _ in range(10):
            progress.update(task, advance=10)
        
        if response.status_code != 200:
            console.print("[bold red]Error fetching data. Please try again later.[/bold red]")
            return None, None
    
    data = response.json()
    return data["resultSet"]["headers"], data["resultSet"]["rowSet"]

# Function to search for a player's stats based on partial name match
def search_player_stats(player_query, stats_data):
    player_query = player_query.lower()
    for row in stats_data:
        full_name = row[2].lower()
        if player_query in full_name:
            return row
    return None

# Function to print stats in a formatted table
def display_player_stats(player_stats, headers):
    table = Table(title=f"🏀 Player Stats: {player_stats[2]}", show_header=True, header_style="bold magenta")
    
    key_stats = ["TEAM", "GP", "PTS", "AST", "REB", "STL", "BLK", "FG_PCT", "FT_PCT", "3P_PCT"]
    stat_display_names = {
        "TEAM": "Team", "GP": "Games Played", "PTS": "Points Per Game",
        "AST": "Assists Per Game", "REB": "Rebounds Per Game", "STL": "Steals Per Game",
        "BLK": "Blocks Per Game", "FG_PCT": "Field Goal %", "FT_PCT": "Free Throw %", "3P_PCT": "Three-Point %"
    }
    
    table.add_column("Stat", style="bold cyan")
    table.add_column("Value", style="bold yellow")
    
    for stat in key_stats:
        if stat in headers:
            index = headers.index(stat)
            table.add_row(stat_display_names[stat], str(player_stats[index]))
    
    console.print(table)

# Function to search players with tab completion
def search_players(headers, stats_data):
    player_names = [row[2] for row in stats_data]
    player_completer = WordCompleter(player_names, ignore_case=True)
    
    while True:
        player_query = prompt("Enter player's name (or part of it) to search (type 'quit' to exit): ", completer=player_completer).strip()
        
        if player_query.lower() == "quit":
            return  

        player_stats = search_player_stats(player_query, stats_data)
        
        if player_stats:
            display_player_stats(player_stats, headers)
        else:
            console.print(f"[bold red]❌ No player found with '{player_query}'. Try again![/bold red]")

# Main Menu
def main_menu():
    console.print("\n[bold cyan]NBA Stats Explorer[/bold cyan] 🏀", style="bold underline")
    
    while True:
        headers, stats_data = fetch_nba_stats()
        if headers and stats_data:
            search_players(headers, stats_data)
        else:
            console.print("[bold red]Could not fetch NBA data. Exiting...[/bold red]")
            break  # Exit the loop if data fetching fails

        console.print("[bold red]Exiting NBA Stats Explorer...[/bold red]")
        break


if __name__ == "__main__":
    main_menu()
