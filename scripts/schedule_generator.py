#!/usr/bin/env python3
"""
Schedule Generator for ASTR 201
Reads data/schedule.yml and generates computed dates.

Usage:
    # In a Quarto document with {python}:
    from scripts.schedule_generator import generate_schedule, format_schedule_table
    schedule = generate_schedule()
    print(format_schedule_table(schedule))

    # Or run standalone:
    python scripts/schedule_generator.py
"""

import yaml
from datetime import datetime, timedelta
from pathlib import Path


def _coerce_date(value) -> datetime:
    """Return a datetime for YYYY-MM-DD strings or date/datetime objects."""
    if isinstance(value, datetime):
        return value
    # yaml.safe_load may return datetime.date for ISO dates
    if hasattr(value, "year") and hasattr(value, "month") and hasattr(value, "day"):
        return datetime(value.year, value.month, value.day)
    return datetime.strptime(str(value), "%Y-%m-%d")


def load_schedule_data(path: str = "data/schedule.yml") -> dict:
    """Load schedule configuration from YAML."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def get_lecture_dates(semester_start: str, days: list[str], num_lectures: int,
                      breaks: list[dict] = None) -> list[datetime]:
    """
    Generate lecture dates given semester start and lecture days.

    Args:
        semester_start: ISO date string (e.g., "2026-01-20")
        days: List of day names (e.g., ["Tue", "Thu"])
        num_lectures: Total number of lectures to generate
        breaks: List of break periods to skip

    Returns:
        List of datetime objects for each lecture
    """
    day_map = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}
    lecture_days = [day_map[d] for d in days]

    start = _coerce_date(semester_start)

    # Build list of break dates
    break_dates = set()
    if breaks:
        for brk in breaks:
            brk_start = _coerce_date(brk["date"])
            for i in range(brk.get("duration", 1)):
                break_dates.add(brk_start + timedelta(days=i))

    dates = []
    current = start
    while len(dates) < num_lectures:
        if current.weekday() in lecture_days and current not in break_dates:
            dates.append(current)
        current += timedelta(days=1)

    return dates


def generate_schedule(config_path: str = "data/schedule.yml") -> list[dict]:
    """
    Generate full schedule with computed dates.

    Returns list of dicts with: week, date, topic, reading, type
    """
    config = load_schedule_data(config_path)

    # Count total lectures
    total_lectures = sum(
        len(m["lectures"]) for m in config["modules"]
    )

    # Generate dates
    dates = get_lecture_dates(
        config["semester_start"],
        config["days"],
        total_lectures,
        config.get("breaks", [])
    )

    # Build schedule
    schedule = []
    date_idx = 0
    start_date = _coerce_date(config["semester_start"])

    for module in config["modules"]:
        for lecture in module["lectures"]:
            if date_idx < len(dates):
                lecture_date = dates[date_idx]
                # Calculate week number
                week_num = ((lecture_date - start_date).days // 7) + 1

                schedule.append({
                    "week": week_num,
                    "date": lecture_date,
                    "module": module["name"],
                    "topic": lecture["title"],
                    "reading": lecture.get("reading", ""),
                    "type": "exam" if "MIDTERM" in lecture["title"] or "EXAM" in lecture["title"].upper() else "lecture"
                })
                date_idx += 1

    # Add homework due dates (Tuesday) and optional grade memo due dates (following Friday)
    hw_schedule = []
    for hw in config.get("homework", []):
        # Homework due Tuesday of given week
        week_start = start_date + timedelta(weeks=hw["week"] - 1)
        # Find Tuesday of that week
        days_to_tuesday = (1 - week_start.weekday()) % 7
        if week_start.weekday() == 1:
            due_date = week_start
        else:
            due_date = week_start + timedelta(days=days_to_tuesday)
        grade_memo_due = None
        if hw.get("grade_memo", True):
            grade_memo_due = due_date + timedelta(days=3)  # following Friday

        hw_schedule.append({
            "week": hw["week"],
            "date": due_date,
            "grade_memo_due": grade_memo_due,
            "title": hw["title"],
            "type": "homework"
        })

    return schedule, hw_schedule


def format_schedule_table(schedule: list[dict], include_reading: bool = True) -> str:
    """Format schedule as Markdown table."""
    if include_reading:
        lines = ["| Week | Date | Topic | Reading |", "|:--:|:--|:--|:--|"]
        for entry in schedule:
            date_str = entry["date"].strftime("%a %b %d")
            reading = entry.get("reading", "")
            if entry["type"] == "exam":
                lines.append(f"| {entry['week']} | **{date_str}** | **{entry['topic']}** | |")
            else:
                lines.append(f"| {entry['week']} | {date_str} | {entry['topic']} | {reading} |")
    else:
        lines = ["| Week | Date | Topic |", "|:--:|:--|:--|"]
        for entry in schedule:
            date_str = entry["date"].strftime("%a %b %d")
            if entry["type"] == "exam":
                lines.append(f"| {entry['week']} | **{date_str}** | **{entry['topic']}** |")
            else:
                lines.append(f"| {entry['week']} | {date_str} | {entry['topic']} |")

    return "\n".join(lines)


def format_homework_table(hw_schedule: list[dict]) -> str:
    """Format homework schedule as Markdown table."""
    lines = ["| Week | Due Date | Grade Memo Due | Assignment |", "|:--:|:--|:--|:--|"]
    for hw in hw_schedule:
        due_date_str = hw["date"].strftime("%a %b %d")
        memo_date_str = hw["grade_memo_due"].strftime("%a %b %d") if hw["grade_memo_due"] else "—"
        lines.append(f"| {hw['week']} | {due_date_str} | {memo_date_str} | {hw['title']} |")
    return "\n".join(lines)


def get_week_dates(week_num: int, config_path: str = "data/schedule.yml") -> tuple[datetime, datetime]:
    """Get start and end dates for a given week number."""
    config = load_schedule_data(config_path)
    start = _coerce_date(config["semester_start"])
    week_start = start + timedelta(weeks=week_num - 1)
    # Adjust to Monday
    week_start = week_start - timedelta(days=week_start.weekday())
    week_end = week_start + timedelta(days=6)
    return week_start, week_end


if __name__ == "__main__":
    # Test the generator
    import os
    os.chdir(Path(__file__).parent.parent)

    schedule, hw_schedule = generate_schedule()

    print("# Lecture Schedule\n")
    print(format_schedule_table(schedule))
    print("\n# Homework Schedule\n")
    print(format_homework_table(hw_schedule))
