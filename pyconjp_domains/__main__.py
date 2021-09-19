import argparse
import csv
import os

from pyconjp_domains.core import fetch_talks


def retrieve_talks_in_timetable(output):
    endpoint_id = os.environ["ENDPOINT_ID"]
    url = f"https://sessionize.com/api/v2/{endpoint_id}/view/All"
    talks = fetch_talks(url)

    fields = [
        "id",
        "title",
        "room",
        "day",
        "start_time",
        "slot_number",
        "elevator_pitch",
        "prior_knowledge",
        "take_away",
        "level",
        "track",
        "speaking_language",
        "slide_language",
        "description",
        "speaker_names",
        "speaker_profiles",
    ]
    rows = [
        talk.as_list(fields)
        for talk in sorted(talks, key=lambda t: (t.day, t.slot_number, t.room))
    ]

    for row in rows:
        row[3] = row[3].strftime("%m/%d")
        row[4] = row[4].strftime("%H:%M")
        row[-2] = ", ".join(row[-2])  # スピーカーが2人以上の場合は区切る
        row[-1] = "\n\n".join(row[-1])

    with open(output, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch talk data from sessionize."
    )
    parser.add_argument("data_type", choices=("timetable",))
    parser.add_argument("output_csv")
    args = parser.parse_args()

    if args.data_type == "timetable":
        retrieve_talks_in_timetable(args.output_csv)
