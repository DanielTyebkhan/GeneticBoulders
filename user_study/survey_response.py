from dataclasses import dataclass
from typing import List, Tuple

from image_link_mapping import IMAGE_LINKS


@dataclass
class GradeResponse:
    actual: int
    predicted: int

    def is_correct(self):
        return self.actual - 1 <= self.predicted <= self.actual + 1

GradeResponses = List[GradeResponse]

@dataclass
class SurveyResponse:
    calibrations: GradeResponses
    generated: GradeResponses
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
            if is_calibration:
                add_to = self.calibrations
            else:
                add_to = self.generated
            add_to.append(GradeResponse(true_grade, guessed_grade))

    def max_gradeable(self):
        return self.max_climbed + 1

    def correct_list(self, ls: GradeResponses):
        return [c for c in ls if c.is_correct()]

    def correct_calibrations(self):
        return self.correct_list(self.calibrations)

    def correct_generated(self):
        return self.correct_list(self.generated)

    def perc_gradeable(self, ls: GradeResponses):
        top = self.max_gradeable()
        valid = [c for c in ls if c.actual <= top]
        correct = self.correct_list(valid)
        return len(correct) / len(valid)

    def perc_calibrated_gradeable(self):
        return self.perc_gradeable(self.calibrations)

    def perc_generated_gradeable(self):
        return self.perc_gradeable(self.generated)

    def num_pred_higher(self):
        return []
