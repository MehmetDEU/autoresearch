"""Participation scoring, survey Q1 credit, and EAP presentation credit."""

from __future__ import annotations

# EAP presentation (Q4): confirmed presenters who may have left the box unchecked.
# Value = number of presentations (2 → full 20 participation cap).
PRESENTATION_CREDIT: dict[str, int] = {
    "220907002": 2,  # İdil Ezgi Atış — presented twice
    "220907017": 1,  # Okan İşkol
    "220907025": 1,  # Eren Doğan
    "220907026": 1,  # Sudem Güler
    "220907044": 1,  # Şevval Ağca
    "230907034": 1,  # Beyzanur İnce
    "230907035": 1,  # Eren Özdemir
    "230907039": 1,  # Enes Parlaktaş
    "230907046": 1,  # Ayşe Gül Tanriverdi
    "230907059": 1,  # Çağatay Duman
    "230907064": 1,  # Beril Şuheda Sakarya
    "230907069": 1,  # Işıl Yıldız Özbek
    "230907070": 1,  # Emir Edremitli
    "230907092": 1,  # Şeyma Ayşe Efendioğlu
    "230907095": 1,  # Zeynep Zülal Kahriman
    "230907100": 1,  # Ceylin Yılmazsönmez
    "240907025": 1,  # İrem Demiröz
}

PRESENTATION_CREDIT_IDS = frozenset(PRESENTATION_CREDIT)

# Students confirmed on Soner Polat survey but may have left Q1 unchecked on exam.
SURVEY_Q1_CREDIT_IDS = frozenset(
    {
        "220907059",  # Kübra Azra Hoşgör
        "220907067",  # Kübra Yerli
        "220907036",  # Elif Nur Dolak
        "220907002",  # İdil Ezgi Atış
        "230907069",  # Işıl Yıldız Özbek
        "230907046",  # Ayşe Gül Tanriverdi
        "230907100",  # Ceylin Yılmazsönmez
        "220907025",  # Eren Doğan
        "220907042",  # Fatmanur Emir
        "230907076",  # Mukaddes Karavil
        "230907058",  # Şevval Ceren Topdemir
    }
)


def yes_val(value: object) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    return text in ("yes", "y", "true", "checked", "evet", "1")


def parse_checklist(checklist: dict | None) -> dict:
    if not checklist:
        return {"q1": False, "q2": False, "q3": False, "q4": False, "times": None}

    flat = {str(key).lower(): value for key, value in checklist.items()}

    def read_yes(keys: tuple[str, ...]) -> bool:
        for key in keys:
            if key not in flat:
                continue
            value = flat[key]
            if key in ("q4_participated", "eap_presentation", "eap_presentations", "q4"):
                if isinstance(value, bool):
                    return value
                text = str(value).strip().lower()
                if text in ("did_not_participate", "no", "false", "unchecked"):
                    return False
                if text in ("participated", "yes", "true", "i participated"):
                    return True
            return yes_val(value)
        return False

    def read_times() -> int | None:
        for key in ("times", "q4_times", "eap_times", "presentation_times"):
            if key not in flat or flat[key] is None:
                continue
            value = flat[key]
            if isinstance(value, (int, float)):
                return int(value)
            text = str(value).strip().lower()
            if text in ("2", "two", "twice"):
                return 2
            if text in ("1", "one", "once"):
                return 1
            try:
                return int(text)
            except ValueError:
                continue
        return None

    return {
        "q1": read_yes(("q1", "q1_questionnaire", "questionnaire")),
        "q2": read_yes(("q2", "q2_ai_workshops", "ai_workshops")),
        "q3": read_yes(("q3", "q3_ai_symposium", "ai_symposium")),
        "q4": read_yes(("q4_participated", "eap_presentation", "eap_presentations", "q4")),
        "times": read_times(),
    }


def calc_participation(
    checklist: dict | None,
    *,
    force_q1: bool = False,
    force_q4: bool = False,
    presentation_times: int | None = None,
) -> int:
    parsed = parse_checklist(checklist)
    q1, q2, q3, q4 = parsed["q1"], parsed["q2"], parsed["q3"], parsed["q4"]
    if force_q1:
        q1 = True
    if force_q4:
        q4 = True

    times = presentation_times if presentation_times is not None else parsed["times"]
    if times == 2:
        return 20

    yes_count = sum([q1, q2, q3])
    part = 10 if yes_count >= 2 else (5 if yes_count == 1 else 0)
    if q4:
        part += 10
    return min(part, 20)


def apply_participation_credits(row: dict) -> tuple[float, str]:
    """Recalculate participation with survey Q1 and EAP presentation overrides."""
    sid = row.get("idnumber", "")
    checklist = row.get("checklist")
    force_q1 = sid in SURVEY_Q1_CREDIT_IDS
    pres_times = PRESENTATION_CREDIT.get(sid)
    force_q4 = pres_times is not None

    baseline = calc_participation(checklist)
    with_q1 = calc_participation(checklist, force_q1=True) if force_q1 else baseline
    without_pres = calc_participation(
        checklist,
        force_q1=force_q1,
        force_q4=False,
        presentation_times=None,
    )
    new = float(
        calc_participation(
            checklist,
            force_q1=force_q1,
            force_q4=force_q4,
            presentation_times=pres_times,
        )
    )

    notes: list[str] = []
    existing = row.get("notes") or ""
    if force_q1 and with_q1 > baseline and "Soner Polat" not in existing:
        notes.append(f"Soner Polat anketi Q1 kredisi (+{with_q1 - baseline:.0f} katılım).")
    if force_q4 and new > without_pres and "EAP sunumu" not in existing:
        if pres_times == 2:
            notes.append("EAP sunumu 2× kredisi (katılım üst sınır 20).")
        else:
            notes.append(f"EAP sunumu katılım kredisi (+{new - without_pres:.0f} katılım).")

    return new, (" " + " ".join(notes)) if notes else ""


def apply_survey_q1_credit(row: dict) -> tuple[float, str]:
    """Backward-compatible wrapper."""
    return apply_participation_credits(row)
