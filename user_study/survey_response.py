from dataclasses import dataclass
from typing import List, Tuple

from image_link_mapping import IMAGE_LINKS

GRADE_ALLOWANCE = 3

@dataclass
class GradeResponse:
    actual: int
    predicted: int

    def is_correct(self):
        return self.actual - GRADE_ALLOWANCE <= self.predicted <= self.actual + GRADE_ALLOWANCE

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
        return self.max_climbed + GRADE_ALLOWANCE

    def correct_list(self, ls: GradeResponses):
        return [c for c in ls if c.is_correct()]
    
    def incorrect_list(self, ls: GradeResponses):
        return [c for c in ls if not c.is_correct()]

    def correct_calibrations(self):
        return self.correct_list(self.calibrations)

    def correct_generated(self):
        return self.correct_list(self.generated)

    def perc_calibration_correct(self):
        return len(self.correct_calibrations()) / len(self.calibrations)

    def perc_generated_correct(self):
        return len(self.correct_generated()) / len(self.generated)

    def perc_gradeable(self, ls):
        top = self.max_gradeable()
        valid = [c for c in ls if c.actual <= top]
        correct = self.correct_list(valid)
        return len(correct) / len(valid)

    def perc_calibrated_gradeable(self):
        return self.perc_gradeable(self.calibrations)

    def perc_generated_gradeable(self):
        return self.perc_gradeable(self.generated)

    def num_pred_higher(self):
        return len([p for p in self.incorrect_generated() if p.predicted < p.actual])

    def num_pred_lower(self):
        return len([p for p in self.incorrect_generated() if p.predicted > p.actual])
