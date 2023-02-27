from dataclasses import dataclass
from typing import Dict, List

from image_link_mapping import IMAGE_LINKS

@dataclass
class SurveyResponse:
    calibrations: List[Dict[str, bool]]
    generated: List[Dict[str, bool]]
    max_climbed: int

    def __init__(self, qualtrics_resp):
        self.calibrations = []
        self.generated = []
        self.max_climbed = int(qualtrics_resp['Q6'].split()[0][1:])
        for i in range(30):
            question = f'{i + 1}_Q10'
            link = IMAGE_LINKS[i]
            true_grade = int(link.split('_')[0][1:])
            is_calibration = 'calibrate' in link
            guessed_grade = int(qualtrics_resp[question].split()[0][1:])
            correct = true_grade - 1 <= guessed_grade <= true_grade + 1
            if is_calibration:
                add_to = self.calibrations
            else:
                add_to = self.generated
            add_to.append({true_grade: correct})

