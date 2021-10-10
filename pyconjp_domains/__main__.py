import argparse
import csv
import os

from pyconjp_domains.core import fetch_talks

WEBSITE_TIMETABLE_FIELDS = [
    "id",
    "title",
    "room",
    "day",
    "start_time",
    "slot_number AS no",
    "elevator_pitch",
    "prior_knowledge AS prerequisite_knowledge",
    "take_away AS audience_takeaway",
    "level AS audience_python_level",
    "track",
    "speaking_language AS lang_of_talk",
    "slide_language AS lang_of_slide",
    "description",
    "duration_min",
    "slide_url",
    "recording_url",
    # 2021は複数人での発表がないため
    "speaker_names AS name",
    "speaker_profiles AS profile",
]


def parse_field_arguments(arguments):
    fields, headers = (), ()
    for argument in arguments:
        splitted = argument.split(" AS ")
        if len(splitted) == 1:
            fields += (argument,)
            headers += (argument,)
        elif len(splitted) == 2:
            fields += (splitted[0],)
            headers += (splitted[1],)
    return fields, headers


def retrieve_talks_in_timetable(output, field_arguments):
    endpoint_id = os.environ["ENDPOINT_ID"]
    url = f"https://sessionize.com/api/v2/{endpoint_id}/view/All"
    talks = fetch_talks(url)

    fields, headers = parse_field_arguments(field_arguments)

    rows = [talk.as_list(fields) for talk in talks.sorted()]

    for row in rows:
        row[3] = row[3].strftime("%m/%d")
        row[4] = row[4].strftime("%H:%M")
        row[5] = None if row[5] == 0 else row[5]
        row[-2] = ", ".join(row[-2])  # スピーカーが2人以上の場合は区切る
        # Noneはjoinできないので、空文字列に変換する
        row[-1] = "\n\n".join(v or "" for v in row[-1])

    with open(output, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows([headers] + rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch talk data from sessionize."
    )
    parser.add_argument("data_type", choices=("timetable",))
    parser.add_argument("output_csv")
    parser.add_argument(
        "--fields", nargs="*", default=WEBSITE_TIMETABLE_FIELDS
    )
    args = parser.parse_args()

    if args.data_type == "timetable":
        retrieve_talks_in_timetable(args.output_csv, args.fields)
