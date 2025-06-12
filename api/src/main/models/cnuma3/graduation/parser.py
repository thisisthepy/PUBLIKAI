import logging
from typing import Dict, List, Optional

class GraduationRequirementParser:
    """
    다중 연도별 포맷을 지원하는 파서
    """
    def __init__(self):
        self.COLLEGES = ["인문대학", "사회과학대학", "자연과학대학", "공과대학", "경상대학", "농업생명과학대학", "약학대학", "의과대학", "생활과학대학", "예술대학", "수의과대학", "사범대학", "간호대학", "생명시스템과학대학", "자유전공학부", "지식융합학부", "국가안보융합학부", "창의융합대학"]
        self.CATEGORIES = ["단수전공자", "복수전공자", "부전공자", "교직단수전공자", "교직복수전공자", "심화단수전공자", "심화복수전공자", "심화부전공자", "복수전공제한", "제한"]

    def _calculate_sum(self, value_string: str) -> str:
        total = 0
        parts = value_string.split()
        for part in parts:
            try:
                total += int(part)
            except (ValueError, TypeError):
                continue
        return str(total)

    def _parse_2025_credits(self, tokens: List[str]) -> Optional[Dict[str, str]]:
        # 2025년도 형식 파싱 로직
        if len(tokens) >= 11:
            parsed = {
                "교양기초": tokens[0], "교양균형": self._calculate_sum(f"{tokens[1]} {tokens[2]} {tokens[3]}"),
                "교양소양": self._calculate_sum(f"{tokens[4]} {tokens[5]} {tokens[6]}"), "교양소계": tokens[7],
                "전공기초": tokens[-6] if len(tokens) >= 14 else tokens[-5] if len(tokens) == 13 else tokens[-4] if len(tokens) == 12 else "-",
                "전공핵심": tokens[-5] if len(tokens) >= 14 else tokens[-4] if len(tokens) == 13 else tokens[-3] if len(tokens) == 12 else "-",
                "전공심화": tokens[-4] if len(tokens) >= 14 else tokens[-3] if len(tokens) == 13 else tokens[-2] if len(tokens) == 12 else tokens[-4],
                "전공소계": tokens[-3] if len(tokens) >= 14 else tokens[-2] if len(tokens) == 13 else tokens[-1] if len(tokens) == 12 else tokens[-3],
                "일반선택": tokens[-2], "졸업학점": tokens[-1]
            }
            return parsed
        return None

    def _parse_pre_2025_credits(self, tokens: List[str]) -> Optional[Dict[str, str]]:
        # 2025학년도 이전 형식 파싱 로직
        parsed = {}
        if len(tokens) == 11:
            parsed = {"교양기초": tokens[0], "교양균형": self._calculate_sum(f"{tokens[1]} {tokens[2]}"), "교양소양": self._calculate_sum(tokens[3]), "교양소계": tokens[4], "전공기초": tokens[5], "전공핵심": tokens[6], "전공심화": tokens[7], "전공소계": tokens[8], "일반선택": tokens[9], "졸업학점": tokens[10]}
        elif len(tokens) == 10:
            parsed = {"교양기초": tokens[0], "교양균형": self._calculate_sum(f"{tokens[1]} {tokens[2]}"), "교양소양": self._calculate_sum(tokens[3]), "교양소계": tokens[4], "전공기초": tokens[5], "전공핵심": tokens[6], "전공심화": tokens[7], "전공소계": tokens[8], "일반선택": tokens[9], "졸업학점": tokens[9]}
        else:
            return None
        
        return parsed

    def parse_from_markdown(self, file_path: str, year: int) -> Dict[str, List[Dict[str, str]]]:
        # ... (이전 답변의 parse_from_markdown 메소드 내용 전체를 여기에 복사)
        structured_data = {}
        current_college = None
        last_department = None
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except FileNotFoundError:
            logging.error(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
            return {}
        for line in lines:
            clean_line = line.replace('　', ' ').replace('–', '-').strip()
            if not clean_line or clean_line.startswith(('#', '`', '*', '◦', '※')): continue
            tokens = clean_line.split()
            if not tokens: continue
            category_index = -1
            for i, token in enumerate(tokens):
                if token in self.CATEGORIES or (i > 0 and tokens[i-1] + " " + token == "복수전공 제한"):
                    if token == "제한" and i > 0 and tokens[i-1] == "복수전공": category_index = i
                    elif token != "제한": category_index = i
            if category_index == -1: continue
            text_tokens = tokens[:category_index + 1]
            credit_tokens = tokens[category_index + 1:]
            if text_tokens[0] in self.COLLEGES:
                current_college = text_tokens[0]
            if not current_college: continue
            college_name = current_college
            start_of_dept_index = 1 if text_tokens[0] == college_name else 0
            if text_tokens[-2:] == ['복수전공', '제한']:
                department = " ".join(text_tokens[start_of_dept_index:-2])
                category = "복수전공 제한"
            else:
                department = " ".join(text_tokens[start_of_dept_index:-1])
                category = text_tokens[-1]
            if not department and last_department:
                department = last_department
            elif department:
                last_department = department
            if year == 2025:
                parsed_credits = self._parse_2025_credits(credit_tokens)
            else:
                parsed_credits = self._parse_pre_2025_credits(credit_tokens)
            if parsed_credits:
                final_row = {"입학년도": str(year), "대학명": college_name, "학과명": department, "구분": category, **parsed_credits}
                if college_name not in structured_data:
                    structured_data[college_name] = []
                structured_data[college_name].append(final_row)
        return structured_data