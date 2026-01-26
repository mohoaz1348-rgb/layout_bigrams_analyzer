import os
import copy
from pathlib import Path
from typing import Tuple

LANGUAGES_LIST = ["en", "ru"]
ANALYZE_MODE = ["std", "ang"]
ALT = "alt"
NOT_FOUND = "not_found"
RANGE_LIST = ["-3", "-2", "-1", "0", "1", "2", "3", ALT, NOT_FOUND]
COLUMN_WIDTH = 10
COLUMN_COUNT = 10
FREQ_MIN = 0.005


def caption() -> str:
    caption = "LAYOUT(mode)"
    caption = f"{caption:<{COLUMN_WIDTH*2}}"
    for effort in RANGE_LIST:
        caption += f"{effort:<{COLUMN_WIDTH}}"
    return caption

def read_data(file_name: str) -> list[list[str]]:
    data = []
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            data.append(line.split())
    return data

def print_results_list(lang: str, all_stats: list[Tuple[float, str]]):
    all_stats.insert(0, (0, "\n" + lang))
    all_stats.insert(1, (0, caption()))
    for line in all_stats:
        print(line[1])
    with open(f"./{lang}/results", "w", encoding="utf-8") as file:
        for line in all_stats:
            file.write(line[1] + "\n")


class Layout:
    def __init__(self, path_to_layout: Path) -> None:
        self.name = path_to_layout.name
        self.mode_list: list[str] = []
        self.left_hand = ""
        self.right_hand = ""
        self.is_valid = False
        MODE_ERR = "Analyze Mode for this layout doesn't set in layout file"

        with open(path_to_layout, "r", encoding="utf-8") as file:
            first_line_list = file.readline().split()
            for mode in first_line_list:
                if mode not in ANALYZE_MODE:
                    first_line_list.remove(mode)
            if len(first_line_list) > 0:
                self.mode_list = first_line_list
                self.left_hand = file.readline().strip()
                self.right_hand = file.readline().strip()
                self.is_valid = True
            else:
                self.is_valid = False
                print(f"{self.name} - {MODE_ERR}")

    def analyze(
        self,
        bigrams_list: list[list[str]],
        left_effort: list[list[str]],
        right_effort: list[list[str]],
    ) -> list[list[str]]:

        bigrams_list_analyzed = copy.deepcopy(bigrams_list)
        for i, row in enumerate(bigrams_list_analyzed):
            bigram = row[0].lower()
            simb1 = bigram[0]
            simb2 = bigram[1]
            if (simb1 in self.left_hand) and (simb2 in self.left_hand):
                pos_i = self.left_hand.find(simb1)
                pos_j = self.left_hand.find(simb2)
                bigrams_list_analyzed[i].append(left_effort[pos_i][pos_j])
            elif (simb1 in self.right_hand) and (simb2 in self.right_hand):
                pos_i = self.right_hand.find(simb1)
                pos_j = self.right_hand.find(simb2)
                bigrams_list_analyzed[i].append(right_effort[pos_i][pos_j])
            elif (simb1 in self.left_hand) and (simb2 in self.right_hand):
                bigrams_list_analyzed[i].append(ALT)
            elif (simb1 in self.right_hand) and (simb2 in self.left_hand):
                bigrams_list_analyzed[i].append(ALT)
            else:
                bigrams_list_analyzed[i].append(NOT_FOUND)
        return bigrams_list_analyzed

    def write_results(
        self,
        mode: str,
        bigrams_list_analyzed: list[list[str]],
        results_file_path: Path,
    ) -> Tuple[float, str]:

        with open(results_file_path, "w", encoding="utf-8") as results_file:

            results_file.write("\n")
            results_file.write(f"{self.name.upper()}({mode})\n")

            stat_list: list[str] = []
            sort_by = 0.000
            for effort in RANGE_LIST:
                sum = 0.000
                i = 0
                line = ""
                # print(effort + "(" + self.name + ")")
                results_file.write(effort + "\n")
                for bigram in bigrams_list_analyzed:
                    if bigram[2] == effort:
                        if float(bigram[1]) >= FREQ_MIN:
                            bigram_freq = bigram[0] + "=" + bigram[1]
                            line += f"{bigram_freq:<{COLUMN_WIDTH}}"
                            i += 1
                        if i == COLUMN_COUNT:
                            # print(bigrams_string)
                            results_file.write(line + "\n")
                            line = ""
                            i = 0
                        sum += float(bigram[1])
                if line != "":
                    results_file.write(line + "\n")
                results_file.write("\n")
                if effort == RANGE_LIST[0]:
                    sort_by = sum
                stat_list.append(str(round(sum, 3)))

        layout_stats = f"{self.name}({mode})"
        layout_stats = f"{layout_stats:<{COLUMN_WIDTH*2}}"
        for value in stat_list:
            layout_stats += f"{value:<{COLUMN_WIDTH}}"
        self.prepend_file(results_file_path, caption(), layout_stats)
        return (sort_by, layout_stats)

    def prepend_file(self, file_path: Path, line1: str, line2: str):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        lines.insert(0, line1 + "\n")
        lines.insert(1, line2 + "\n")

        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)


def main():
    left_std_efforts: list[list[str]] = read_data("left")
    left_angle_efforts: list[list[str]]= read_data("left_angle")
    right_efforts: list[list[str]]= read_data("right")

    for lang in LANGUAGES_LIST:
        bigrams_list: list[list[str]] = read_data(f"./{lang}/bigrams")
        results_all_dir = f"./{lang}/results_all/"
        if not os.path.exists(results_all_dir):
            os.makedirs(results_all_dir, exist_ok=True)

        results_list: list[Tuple[float, str]] = []
        for layout_path in Path(f"./{lang}/layouts/").iterdir():
            if not layout_path.is_file():
                continue
            layout = Layout(layout_path)
            if not layout.is_valid:
                continue
            for mode in layout.mode_list:
                left_efforts = left_std_efforts
                if mode == ANALYZE_MODE[1]:
                    left_efforts = left_angle_efforts

                bigrams_list_analized = layout.analyze(
                    bigrams_list, left_efforts, right_efforts
                )
                results: Tuple[float, str] = layout.write_results(
                    mode,
                    bigrams_list_analized,
                    Path(f"{results_all_dir}{layout.name}({mode})"),
                )
                if len(results_list) == 0:
                    results_list.append(results)
                else:
                    for i, result in enumerate(results_list):
                        if results[0] < result[0]:
                            results_list.insert(i, results)
                            break
                        if i == len(results_list) - 1:
                            results_list.append(results)
                            break

        print_results_list(lang, results_list)

if __name__ == "__main__":
    main()

