import os
import re
import copy
from pathlib import Path
from typing import Tuple

"""
fspr - Full Scissor Pinky/Ring
hspr - Half-Scissor Pinky/Ring

fsg - Full Scissor (Good: Index finger on the bottom row)
wsg - Wide(full) Scissor (Good)
Wsg - Widest(full) Scissor (Good)

fs - Full Scissor (Only Bad)
ws - Wide(full) Scissor (Only Bad) 
Ws - Widest(full) - Scissor (Only Bad)

hsb - Half Scissor (Bad)

sf00 - Same Finger (Finger #, Distance)

ls - Lateral Stretch
lsr - Lateral Stretch (Ring)
LS - Lateral Stretch (Index-Pinky) (5-6u)
lspr - Lateral Stretch (Pinky-Ring)
lspm - Lateral Stretch (Pinky-Middle)

rpm - Roll (Pinky-Middle)
ropr - Roll-Out (Pinky-Ring)
"""

LANGUAGES_LIST = ["en", "ru"]

STD = "std"
ANG = "ang"
ANALYZE_MODE = [STD, ANG]

ALT = "alt"
NOT_FOUND = "NF"
EFFORTS_LIST = [
    ("-3", "-3", 4.0, 1.0),
    ("-2", "-2", 2.0, 3.0),
    ("-1", "-1", 1.0, 6.0),
    ("0", "0", 0.0, None),
    ("1", "1", 0.0, None),
    ("2", "2", 0.0, None),
    ("3", "3", 0.0, None),
    (ALT, ALT, 0.0, None),
    (NOT_FOUND, NOT_FOUND, 0.0, None)
]
"""
EFFORTS_LIST = [
    ("-5", "-5", 4.0, 0.5),
    ("-4", "-4", 2.8, 1.0),
    ("-3", "-3", 2.0, 1.7),
    ("-2", "-2", 1.4, 2.8),
    ("-1", "-1", 1.0, 4.0),
    ("0", "0", 0.0, None),
    ("1", "1", 0.0, None),
    ("2", "2", 0.0, None),
    ("3", "3", 0.0, None),
    ("4", "4", 0.0, None),
    ("5", "5", 0.0, None),
    (ALT, ALT, 0.0, None),
    (NOT_FOUND, NOT_FOUND, 0.0, None)
]
"""
L = "l"
R = "r"
HAND_LIST = [
    ("Left", L, 1.0, 23.0),
    ("Right", R, 1.0, 23.0),
    (ALT, ALT, 0.0, None),
    (NOT_FOUND, NOT_FOUND, 0.0, None)
]
FSPR = "fspr"           # Full Scissor Pinky/Ring
SFB_PREF = "sf"
FING_PTN = "[0-3,6-9]"
PNK_PTN = "[0,9]"
SFB_DIST_PTN = "[0-3]"
SFB_2U_LBL = "SFB(2u)"
BG_TYPES_LIST = [
    ("PRS", f"^{FSPR}$|^hspr$", 3.0, 0.25),           # PRS = FSPR + HSPR
    ("FS(bad)", f"^fs$|^{FSPR}$", 3.0, 0.08),         # Bad Full Scissors - Standart
    ("WS(bad)", "^[Ww]s$", 3.0, 0.10),                # Bad Full Scissors - Wide
    ("HS(bad)", "^hsb$", 1.5, 0.5),                  # Bad Half-Scissors
    ("SFB(P)", f"^{SFB_PREF}{PNK_PTN}{SFB_DIST_PTN}$", 3.0, 0.4),    # SFB on Pinkies
    ("SFB", f"^{SFB_PREF}{FING_PTN}{SFB_DIST_PTN}$", 0.0, 5.6),      # All SFB (with SFB(0u))
    ("SFB(0u)", f"^{SFB_PREF}{FING_PTN}0$", 1.0, None),
    ("SFB(1u)", f"^{SFB_PREF}{FING_PTN}1$", 1.0, 3.1),
    (SFB_2U_LBL, f"^{SFB_PREF}{FING_PTN}2$", 2.0, 0.20), # ?
    ("SFB(3u)", f"^{SFB_PREF}{FING_PTN}3$", 3.0, 0.05),
    ("LSB(IM)", "^ls$", 0.5, 2.5),                   # LSB Index-Middle
    ("LSB(IR)", f"^lsr$", 0.25, 3.5),                # LSB Index-Ring
    ("LSB(IP)", "^LS$", 1.0, 1.0),                   # LSB Index-Pinky
    ("LSB(P)", f"^lspr$|^lspm$", 2.5, 0.25),          # LSB Pinky-Ring + LSB Pinky-Middle
    ("R(P-M)", "^rpm$", 0.5, 2.0),                   # Rolls Pinky-Middle
    ("R(R->P)", "^ropr$", 1.0, 0.5),                 # Roll-out Ring->Pinky
    #("FS(ok)", f"^fsg$", 0.0, None),          # Good (Index on buttom row) Full Scissors
    #("WS(ok)", f"^[Ww]sg$", 0.0, None),        # Good Full Scissors - Wide
]
SORT_BY = "Sort By"

SFB_PER_FINGER_LIST = [
    ("SFB_0", f"^{SFB_PREF}0{SFB_DIST_PTN}$", 1.0, 0.25),
    ("SFB_1", f"^{SFB_PREF}1{SFB_DIST_PTN}$", 1.0, 1.0),
    ("SFB_2", f"^{SFB_PREF}2{SFB_DIST_PTN}$", 1.0, 1.5),
    ("SFB_3", f"^{SFB_PREF}3{SFB_DIST_PTN}$", 1.0, 2.0),
    ("SFB_6", f"^{SFB_PREF}6{SFB_DIST_PTN}$", 1.0, 2.0),
    ("SFB_7", f"^{SFB_PREF}7{SFB_DIST_PTN}$", 1.0, 1.5),
    ("SFB_8", f"^{SFB_PREF}8{SFB_DIST_PTN}$", 1.0, 1.0),
    ("SFB_9", f"^{SFB_PREF}9{SFB_DIST_PTN}$", 1.0, 0.25),
]

#COMPARE TABLE OF LAYOUTS:
COL_W_LAYOUT_NAME = 20      # Layout Name column width
COL_W_TBL = 8               # Other columns width

#FULL REPORT FOR LAYOUT:
COLUMN_WIDTH = 10           # for Bigrams list
COLUMN_COUNT = 10           # for Bigrams list
# Bigram not listed in report if their frequency less then this threshold:
FREQ_MIN = 0.005


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
                top: str = file.readline().strip()
                home: str = file.readline().strip()
                buttom: str = file.readline().strip()
                self.convert_layout_to_inner_view(top, home, buttom)
                #self.left_hand = file.readline().strip()
                #self.right_hand = file.readline().strip()
                self.is_valid = True
            else:
                self.is_valid = False
                print(f"{self.name} - {MODE_ERR}")

    def convert_layout_to_inner_view(self, top: str, home: str, buttom: str) -> None:
        top = top.replace(" ", "")
        if len(top) > 12: top = top[:12]
        #print(top)
        home = home.replace(" ", "")
        if len(home) > 11: home = home[:11]
        buttom = buttom.replace(" ", "")
        if len(buttom) > 10: buttom = buttom[:10]
        self.left_hand = top[:5] + home[:5] + buttom[:5]
        self.right_hand = top[5:] + home[5:] + buttom[5:]

    def get_layout_view(self) -> str:
        top: str = self.left_hand[:5] + self.right_hand[:7]
        home: str = self.left_hand[5:10] + self.right_hand[7:13]
        bottom: str = self.left_hand[10:] + self.right_hand[13:]
        rows = [top, home, bottom]
        view: str = "\n"
        for i, row in enumerate(rows):
            row_spaced: str = ""
            for j, letter in enumerate(row):
                if j == 4:
                    row_spaced += letter + "  " 
                elif j == len(row) - 1:
                    row_spaced += letter
                else:
                    row_spaced += letter + " "
            if i == 2: row_spaced = " " + row_spaced
            view += row_spaced + "\n"
        return view

    def classify(
        self,
        bigrams_list: list[list[str]],
        left_effort: list[list[str]],
        right_effort: list[list[str]],
        left_class: list[list[str]],
        right_class: list[list[str]],
    ) -> list[list[str]]:

        bg_list_classified = copy.deepcopy(bigrams_list)
        for i, row in enumerate(bg_list_classified):
            bigram = row[0].lower()
            simb1 = bigram[0]
            simb2 = bigram[1]
            if (simb1 in self.left_hand) and (simb2 in self.left_hand):
                pos_i = self.left_hand.find(simb1)
                pos_j = self.left_hand.find(simb2)
                bg_list_classified[i].append(left_effort[pos_i][pos_j])
                bg_list_classified[i].append(left_class[pos_i][pos_j])
                bg_list_classified[i].append(L)
            elif (simb1 in self.right_hand) and (simb2 in self.right_hand):
                pos_i = self.right_hand.find(simb1)
                pos_j = self.right_hand.find(simb2)
                bg_list_classified[i].append(right_effort[pos_i][pos_j])
                bg_list_classified[i].append(right_class[pos_i][pos_j])
                bg_list_classified[i].append(R)
            elif (simb1 in self.left_hand) and (simb2 in self.right_hand):
                bg_list_classified[i].append(ALT)
                bg_list_classified[i].append(ALT)
                bg_list_classified[i].append(ALT)
            elif (simb1 in self.right_hand) and (simb2 in self.left_hand):
                bg_list_classified[i].append(ALT)
                bg_list_classified[i].append(ALT)
                bg_list_classified[i].append(ALT)
            else:
                bg_list_classified[i].append(NOT_FOUND)
                bg_list_classified[i].append(NOT_FOUND)
                bg_list_classified[i].append(NOT_FOUND)
        return bg_list_classified

    def get_results_by(
        self,
        mode: str,
        bg_list_classified: list[list[str]],
        range_list: list
    ) -> Tuple[list, dict]:
        res_dict: dict = {}
        layout_name = f"{self.name}({mode})"
        stat_list: list = [layout_name]
        for item in range_list:
            sum = 0.0
            lst: list[list] = []
            lbl = item[0]
            ptn = item[1]
            for bigram in bg_list_classified:
                if range_list is EFFORTS_LIST:
                    if ptn == bigram[2]:
                        sum += float(bigram[1])
                        lst.append(bigram)
                elif (range_list is BG_TYPES_LIST) or (range_list is SFB_PER_FINGER_LIST):
                    x = re.findall(ptn, bigram[3])
                    if x:
                        if x[0] == bigram[3]:
                            sum += float(bigram[1])
                            lst.append(bigram)
                elif range_list is HAND_LIST:
                    if ptn == bigram[4]:
                        sum += float(bigram[1])
                        lst.append(bigram)
            stat_list.append(round(sum, 2))
            if range_list is HAND_LIST:
                if lbl != ALT and lbl != NOT_FOUND:
                    res_dict[lbl] = lst
            else:
                res_dict[lbl] = lst
            #res_dict[lbl] = lst

        return (stat_list, res_dict)

    def append_full_report(
        self,
        #mode: str,
        results_file_path: Path,
        write_mode: str,
        data: tuple[list, dict],
        range_list: list,
        full: bool = True
    ):
        stat_list_original, stat_dict  = data
        stat_list = stat_list_original.copy()
        stat_list.pop(0)
        content_list: list[str] = []
        if full:
            for k, bigrams_list in stat_dict.items():
                sum = 0.0
                i = 0
                line = ""
                bg_list_for_key: list[str] = []
                for bigram in bigrams_list:
                    if float(bigram[1]) >= FREQ_MIN:
                        bigram_freq = bigram[0] + "=" + bigram[1]
                        line += f"{bigram_freq:<{COLUMN_WIDTH}}"
                        i += 1
                    if i == COLUMN_COUNT:
                        bg_list_for_key.append(line)
                        line = ""
                        i = 0
                    sum += float(bigram[1])
                if line != "":
                    bg_list_for_key.append(line)
                sum_str = f"{round(sum, 2):.2f}"
                #sum_str = f"{stat_list[j]:.2f}"
                content_list.append("\n" + str(k) + "=" + sum_str + "%")
                content_list += bg_list_for_key

        layout_stats = ""
        for i, value in enumerate(stat_list):
            red_flag = range_list[i][3]
            param_lbl = range_list[i][0]
            warn = get_warning(value, red_flag, param_lbl)
            layout_stats += f"{warn}{value}".rjust(COL_W_TBL)

        #content_list.insert(0, f"\n{self.name.upper()}({mode})\n")
        l = self.get_layout_view() if full else ""
        content_list.insert(0, l)
        content_list.insert(1, caption(range_list, skip=True))
        content_list.insert(2, layout_stats)

        with open(results_file_path, write_mode, encoding="utf-8") as file:
            for line in content_list:
                file.write(line + "\n")

    def prepend_file(self, file_path: Path, line1: str, line2: str):
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        lines.insert(0, line1 + "\n")
        lines.insert(1, line2 + "\n")

        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)


def read_data(file_path: Path) -> list[list[str]]:
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            data.append(line.split())
    return data

def sort_by_effort(layout_stats: list) -> float:
    order_by = 0.0
    for i, effort in enumerate(EFFORTS_LIST[:abs(int(EFFORTS_LIST[0][1]))], 1):
        order_by +=  effort[2] * layout_stats[i]
    layout_stats.append(order_by)
    return order_by

def sort_by_type(layout_stats: list) -> float:
    order_by = 0.0
    for i, bg_type in enumerate(BG_TYPES_LIST, 1):
        order_by += bg_type[2] * layout_stats[i]
    layout_stats.append(order_by)
    return order_by

def sort_by_alt(layout_stats: list) -> float:
    sort_by = 0.0
    alt = layout_stats[3]
    sort_by = alt * HAND_LIST[2]*[2]
    layout_stats.append(sort_by)
    return sort_by

def sort_by_one_hand_usage(layout_stats: list) -> float:
    sort_by = 0.0
    l = layout_stats[1]
    r = layout_stats[2]
    sort_by = max(l * HAND_LIST[0][2], r * HAND_LIST[1][2])
    layout_stats.append(sort_by)
    return sort_by

def sort_by_sfb(layout_stats: list) -> float:
    sort_by = 0.0
    for i, finger in enumerate(SFB_PER_FINGER_LIST, 1):
        sort_by += finger[2]*layout_stats[i]
    layout_stats.append(sort_by)
    return sort_by

def caption(range_list: list[Tuple], skip: bool = False) -> str:
    k = ""
    lbl = ""
    if not skip:
        k = f"{k:<{COL_W_LAYOUT_NAME}}"
        lbl = "LAYOUT(mode)"
        lbl = f"{lbl:<{COL_W_LAYOUT_NAME}}"
    for item in range_list:
        k += f"{item[2]:>{COL_W_TBL}}"
        lbl += f"{item[0]:>{COL_W_TBL}}"
    if not skip:
        lbl += f"{SORT_BY:>{COL_W_TBL}}"
        caption = k + "\n" + lbl
    else:
        caption = lbl
    return caption

def write_compare_table(
    lang: str, 
    file_path: Path,
    data: list[tuple[list[tuple], list[list]]]
    ):
    all_stats_for_print: list[str] = []
    for range_list, all_stats in data:
        all_stats_for_print.append("\n" + lang)
        all_stats_for_print.append(caption(range_list))
        for lst in all_stats:
            line: str = ""
            for i, value in enumerate(lst):
                if i == 0:
                    line += f"{value:<{COL_W_LAYOUT_NAME}}"
                else:
                    j = i - 1
                    warn = ""
                    if j < len(range_list):
                        red_flag = range_list[j][3]
                        warn = get_warning(value, red_flag, range_list[j][0])
                    line += f"{warn}{value:.2f}".rjust(COL_W_TBL)
            all_stats_for_print.append(line)
    for line in all_stats_for_print:
        print(line)
    with open(file_path, "w", encoding="utf-8") as file:
        for line in all_stats_for_print:
            file.write(line + "\n")
    print("")
    print(f"See this comparison tables in the file: {file_path}")

def get_warning(value: float, red_flag: float, param_lbl: str) -> str:
    warn = ""
    sign = "?" if param_lbl == SFB_2U_LBL else "!"
    if red_flag:
        if value > red_flag:
            ratio = int(value // red_flag)
            warn = sign if ratio < 2 else str(ratio) + sign
    return warn


def main():
    project_path = Path(__file__).resolve().parent
    left_std_efforts: list[list[str]] = read_data(project_path / "left")
    left_std_types: list[list[str]]= read_data(project_path / "left_types")
    left_angle_efforts: list[list[str]]= read_data(project_path / "left_angle")
    left_angle_types: list[list[str]]= read_data(project_path / "left_angle_types")
    right_efforts: list[list[str]]= read_data(project_path / "right")
    right_types: list[list[str]]= read_data(project_path / "right_types")

    res_by_effort: Tuple[list, dict]
    res_by_type: Tuple[list, dict]

    for lang in LANGUAGES_LIST:
        bg_list: list[list[str]] = read_data(project_path / f"{lang}/bigrams")
        results_all_path = project_path / f"{lang}/results_all"
        if not os.path.exists(results_all_path):
            os.makedirs(results_all_path, exist_ok=True)

        res_by_effort_tbl: list[list] = []
        res_by_type_tbl: list[list] = []
        res_by_hand_tbl: list[list] = []
        res_by_finger_tbl: list[list] = []
        for layout_path in (project_path / f"{lang}/layouts").iterdir():
            if not layout_path.is_file():
                continue
            layout = Layout(layout_path)
            if not layout.is_valid:
                continue
            for mode in layout.mode_list:
                left_efforts = left_std_efforts
                left_types = left_std_types
                if mode == ANG:
                    left_efforts = left_angle_efforts
                    left_types = left_angle_types

                bg_list_classified = layout.classify(
                    bg_list, left_efforts, right_efforts, left_types, right_types
                )
                res_by_effort = layout.get_results_by(mode, bg_list_classified, EFFORTS_LIST)
                res_by_effort_tbl.append(res_by_effort[0])

                res_by_type = layout.get_results_by(mode, bg_list_classified, BG_TYPES_LIST)
                res_by_type_tbl.append(res_by_type[0])

                res_by_hand = layout.get_results_by(mode, bg_list_classified, HAND_LIST)
                res_by_hand_tbl.append(res_by_hand[0])

                res_by_finger = layout.get_results_by(mode, bg_list_classified, SFB_PER_FINGER_LIST)
                res_by_finger_tbl.append(res_by_finger[0])
                
                f_path = results_all_path / f"{layout.name}({mode})"
                layout.append_full_report(f_path, "w", res_by_finger, SFB_PER_FINGER_LIST, full=False)
                layout.append_full_report(f_path, "a", res_by_type, BG_TYPES_LIST, full=False)
                layout.append_full_report(f_path, "a", res_by_effort, EFFORTS_LIST, full=False)
                layout.append_full_report(f_path, "a", res_by_hand, HAND_LIST, full=False)
                layout.append_full_report(f_path, "a", res_by_finger, SFB_PER_FINGER_LIST)
                layout.append_full_report(f_path, "a", res_by_type, BG_TYPES_LIST)
                layout.append_full_report(f_path, "a", res_by_effort, EFFORTS_LIST)
                layout.append_full_report(f_path, "a", res_by_hand, HAND_LIST)

        f_path = project_path / f"{lang}/results"
        res_by_effort_tbl.sort(key=sort_by_effort)
        res_by_type_tbl.sort(key=sort_by_type)
        #res_by_hand_tbl.sort(key=sort_by_alt, reverse=True)
        res_by_hand_tbl.sort(key=sort_by_one_hand_usage)
        res_by_finger_tbl.sort(key=sort_by_sfb)
        data = [
            (BG_TYPES_LIST, res_by_type_tbl),
            (EFFORTS_LIST, res_by_effort_tbl),
            (HAND_LIST, res_by_hand_tbl),
            (SFB_PER_FINGER_LIST, res_by_finger_tbl),
        ]
        write_compare_table(lang, f_path, data)
        print(f"Full results for layouts in the folder: {results_all_path}")
        
    print("")

if __name__ == "__main__":
    main()

