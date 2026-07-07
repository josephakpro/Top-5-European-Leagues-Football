import os
import random
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def create_driver():
    """Creates a freshly configured Chrome driver instance."""
    chrome_options = Options()
    # Unique User-Agent to disguise automation
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
    chrome_options.add_argument("--window-size=1280,800")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"]
    )
    chrome_options.add_experimental_option("useAutomationExtension", False)

    return webdriver.Chrome(options=chrome_options)


def scrape_single_metric(league_id, season_id, stat_key):
    """Opens a fresh browser window, fetches a single stat metric, and closes it securely."""
    url = f"https://www.fotmob.com/leagues/{league_id}/stats/season/{season_id}/teams/{stat_key}"
    print(f"\n[Scraping] Launching clean session for: {stat_key}")

    driver = None
    rows_collected = []

    try:
        driver = create_driver()
        driver.get(url)

        # Wait for the main table links to load completely
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'a[href^="/teams/"]')
            )
        )

        # Human Behavior Simulation: Gently scroll down slightly to trigger lazy-loaded text
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(random.uniform(2.0, 3.5))

        # Parse source HTML layout
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Select all individual team data links
        team_links = soup.find_all(
            "a", href=lambda href: href and href.startswith("/teams/")
        )

        for link in team_links:
            try:
                # 1. Parse Rank
                rank_span = link.find("span", class_=re.compile(r"-Rank"))
                if not rank_span:
                    continue  # Skip any non-table row links matching /teams/
                rank = int(rank_span.text.strip())

                # 2. Parse Team Name
                name_span = link.find(
                    "span", class_=re.compile(r"-TeamOrPlayerName")
                )
                team_name = name_span.text.strip() if name_span else "Unknown"

                # 3. Parse Sub-Stat (Total Value) - Safe Fallback check
                substat_span = link.find("span", class_=re.compile(r"-SubStat"))
                sub_value = None
                if substat_span:
                    sub_text = substat_span.get_text()
                    digits = "".join(filter(str.isdigit, sub_text))
                    sub_value = int(digits) if digits else 0

                # 4. Parse Main Stat Value (Percentage or Average)
                stat_span = link.find("span", class_=re.compile(r"-StatValue"))
                stat_value_text = (
                    stat_span.text.strip().replace("%", "") if stat_span else "0"
                )
                stat_value = float(stat_value_text)

                # Assemble dynamic record entry
                record = {"Rank": rank, "Team Name": team_name}

                # Only include total column if a sub-stat row component exists on the page
                if sub_value is not None:
                    record[f"{stat_key}_Total"] = sub_value

                record[f"{stat_key}_Value"] = stat_value
                rows_collected.append(record)

            except Exception:
                continue

        print(f"[Success] Successfully pulled data for {len(rows_collected)} teams.")

    except Exception as e:
        print(f"[Blocked/Error] Could not pull metric '{stat_key}': {e}")

    finally:
        if driver:
            driver.quit()  # Kill process entirely to purge tracking tokens and clear RAM

    return rows_collected


# =====================================================================
# PIPELINE CONFIGURATION & EXECUTION
# =====================================================================

LEAGUE = "87"  # LaLiga
SEASON = "27233"  # 2023/2024 Season

# Test array with the items you provided
STATS_TO_SCRAPE = [
    #Standard
    "goals_team_match",
    "goals_conceded_team_match",
    "possession_percentage_team",
    "clean_sheet_team", 
    #Attack
    "ontarget_scoring_att_team",
    "expected_goals_team", 
    "_xg_diff_team", 
    "ontarget_scoring_att_team", 
    "big_chance_team",
    "big_chance_missed_team", 
    "accurate_pass_team", 
    "accurate_long_balls_team", 
    "accurate_cross_team", 
    "penalty_won_team", 
    "touches_in_opp_box_team", 
    "corner_taken_team", 
    "_set_piece_goals_team", 
    #Defense
    "expected_goals_conceded_team", 
    "interception_team", 
    "total_tackle_team", 
    "effective_clearance_team", 
    "poss_won_att_3rd_team", 
    "_set_piece_goals_conceded_team", 
    "penalty_conceded_team" , 
    "saves_team",
    #Discipline
    #"fk_foul_lost_team", 
    #"total_yel_card_team", 
    #"total_red_card_team"
]

os.makedirs("fotmob_data", exist_ok=True)
all_metric_dfs = []

print("Starting automated statistical scraping run...")

for current_stat in STATS_TO_SCRAPE:
    records = scrape_single_metric(LEAGUE, SEASON, current_stat)

    if records:
        df_metric = pd.DataFrame(records)
        df_metric.drop(columns=["Rank"], inplace=True, errors="ignore")

        # Export individual file backup
        df_metric.to_csv(f"fotmob_data/{current_stat}.csv", index=False)
        all_metric_dfs.append(df_metric)

    # Cooldown timer to prevent rate-limiting triggers across separate windows
    time.sleep(random.uniform(3.0, 5.0))

# Combine all individual results together into a single tabular sheet
if all_metric_dfs:
    print("\n[Merging] Combining all successful data sheets on 'Team Name'...")
    master_df = all_metric_dfs[0]

    for single_df in all_metric_dfs[1:]:
        master_df = pd.merge(master_df, single_df, on="Team Name", how="outer")

    master_df.to_csv("fotmob_data/master_team_stats.csv", index=False)
    print("\n" + "=" * 50)
    print("      ALL OPERATIONS COMPLETE SUCCESSFULY")
    print("=" * 50)
    print(master_df.head(5))
else:
    print("\nPipeline finished, but zero metrics were successfully gathered.")
    
    master_df.to_csv("laliga_teams_stats_2526.csv", index=False)
