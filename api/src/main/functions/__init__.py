from ..utils import FunctionCalling, FunctionSchema
from . import grad, calendar, cafeteria, shuttle, notice


PublikaiFunctions = FunctionCalling(
    schemas=FunctionCalling.DEFAULT.schemas + [
        FunctionSchema(
            name="get_graduation_requirements",
            description="미리 수집된 충남대학교 학과별 졸업 요건을 조회합니다 (수집 데이터는 2025년 입학자 기준이며, 자세한 요건은 충남대학교 홈페이지 대학생활 > 교육과정안내 > 졸업이수학점 (https://plus.cnu.ac.kr/html/kr/sub05/sub05_051202.html)를 참고하는 것이 좋습니다.)",
            parameters={
                "type": "object",
                "properties": {
                    "department_name": {
                        "type": "string",
                        "description": "학과명 (예: 인공지능학과, 컴퓨터공학과)",
                        "default": "인공지능학과"
                    }
                },
                "required": ["department_name"]
            }
        ),
        FunctionSchema(
            name="get_all_departments_list",
            description="졸업 요건을 조회하려 하는데, 학과 목록이 필요한 경우에 사용할 수 있습니다 (2025년 입학자 기준)",
            parameters={
                "type": "object",
                "properties": {
                },
                "required": []
            }
        ),
        FunctionSchema(
            name="get_cnu_notices",
            description="충남대학교 최신 공지사항을 조회하거나 검색합니다",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "검색 쿼리 (검색 쿼리가 없으면 최신 공지사항을 조회합니다)",
                        "default": ""
                    },
                    "retry": {
                        "type": "integer",
                        "description": "홈페이지 조회 실패시 재시도 횟수",
                        "default": 3
                    }
                },
                "required": []
            }
        ),
        FunctionSchema(
            name="get_cnu_ai_notices",
            description="충남대학교 인공지능학과의 최신 공지사항을 조회하거나 검색합니다",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "검색 쿼리 (검색 쿼리가 없으면 최신 공지사항을 조회합니다)",
                        "default": ""
                    },
                    "retry": {
                        "type": "integer",
                        "description": "홈페이지 조회 실패시 재시도 횟수",
                        "default": 3
                    }
                },
                "required": []
            }
        ),
        FunctionSchema(
            name="get_academic_schedule",
            description="미리 수집된 충남대학교 2025년 학사일정을 조회합니다 (2025년 2월 1일 기준)",
            parameters={
                "type": "object",
                "properties": {
                    "degree_type": {
                        "type": "string",
                        "description": "학위 유형",
                        "enum": ["학부", "일반대학원"],
                        "default": "학부"
                    }
                },
                "required": []
            }
        ),
        FunctionSchema(
            name="fetch_academic_schedule_from_web",
            description="충남대학교의 최신 학사일정을 홈페이지로부터 가져옵니다 (2025년 이외 학사 일정이나, 최신화된 학사 일정이 있는지 확인하기 위함)",
            parameters={
                "type": "object",
                "properties": {
                    "year": {
                        "type": "integer",
                        "description": "조회할 연도 (예: 2025)"
                    },
                    "degree_type": {
                        "type": "string",
                        "description": "학위 유형",
                        "enum": ["학부", "일반대학원"],
                        "default": "학부"
                    },
                    "retry": {
                        "type": "integer",
                        "description": "홈페이지 조회 실패시 재시도 횟수",
                        "default": 3
                    }
                },
                "required": ["year"]
            }
        ),
        FunctionSchema(
            name="get_cafeteria_menu",
            description="충남대학교 교내 식당 식단을 조회합니다 (실시간 조회)",
            parameters={
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "조회할 날짜 (YYYY.MM.DD)"
                    },
                    "retry": {
                        "type": "integer",
                        "description": "홈페이지 조회 실패시 재시도 횟수",
                        "default": 3
                    }
                },
                "required": ["date"]
            }
        ),
        FunctionSchema(
            name="get_dorm_cafeteria_menu",
            description="일주일(월요일~일요일) 치의 충남대학교 학생생활관 식당 식단을 조회합니다 (실시간 조회)",
            parameters={
                "type": "object",
                "properties": {
                    "week": {
                        "type": "integer",
                        "description": "조회할 주차를 지정하는 페이지 번호입니다. 1=이번 주, 2=지난 주, 3=2주 전... 순서로 조회됩니다. 기본값은 1입니다.",
                        "default": 1
                    },
                    "retry": {
                        "type": "integer",
                        "description": "홈페이지 조회 실패시 재시도 횟수",
                        "default": 3
                    }
                },
                "required": []
            }
        ),
        FunctionSchema(
            name="get_shuttle_general_time_table",
            description="미리 수집된 충남대학교 셔틀버스의 일반적인 타임 테이블 정보를 조회합니다 (2025년 5월 기준)",
            parameters={
                "type": "object",
                "properties": {
                },
                "required": []
            }
        ),
        FunctionSchema(
            name="fetch_shuttle_bus_time_table_from_web",
            description="충남대학교 셔틀버스의 최신 운영 시간표를 홈페이지로부터 가져옵니다 (2025년 5월 이후 변경 사항이 있는지 확인하기 위함)",
            parameters={
                "type": "object",
                "properties": {
                    "url": {
                        "url": "string",
                        "description": "시간표 조회에 사용할 홈페이지 URL",
                        "default": "https://plus.cnu.ac.kr/html/kr/sub05/sub05_050403.html"
                    },
                    "retry": {
                        "type": "integer",
                        "description": "홈페이지 조회 실패시 재시도 횟수",
                        "default": 3
                    }
                },
                "required": []
            }
        )
    ],
    implementations=dict(
        **FunctionCalling.DEFAULT.implementations,
        get_graduation_requirements=grad.get_graduation_credits,
        get_all_departments_list=grad.get_all_departments_list,
        get_cnu_notices=notice.get_cnu_notices,
        get_cnu_ai_notices=notice.get_cnu_ai_notices,
        get_academic_schedule=calendar.get_academic_schedule,
        fetch_academic_schedule_from_web=calendar.fetch_academic_schedule_from_web,
        get_cafeteria_menu=cafeteria.get_cafeteria_menu,
        get_dorm_cafeteria_menu=cafeteria.get_dorm_cafeteria_menu,
        get_shuttle_general_time_table=shuttle.get_shuttle_general_time_table,
        fetch_shuttle_bus_time_table_from_web=shuttle.fetch_shuttle_bus_time_table_from_web
    )
)
