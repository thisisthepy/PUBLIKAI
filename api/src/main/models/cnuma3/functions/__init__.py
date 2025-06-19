from ....utils import FunctionCalling, FunctionSchema
from . import graduation, cnu


Cnuma3Functions = FunctionCalling(
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
            description="충남대학교 공지사항을 조회합니다",
            parameters={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "공지사항 소스",
                        "enum": ["대학", "인공지능학과"],
                        "default": "대학"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "최대 결과 수",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 20
                    }
                },
                "required": []
            }
        ),
        FunctionSchema(
            name="get_academic_schedule",
            description="충남대학교 학사일정을 조회합니다",
            parameters={
                "type": "object",
                "properties": {
                    "degree_type": {
                        "type": "string",
                        "description": "학위 유형",
                        "enum": ["학부", "대학원"],
                        "default": "학부"
                    },
                    "semester": {
                        "type": "string",
                        "description": "학기",
                        "enum": ["current", "next"],
                        "default": "current"
                    }
                },
                "required": []
            }
        ),
        FunctionSchema(
            name="get_cafeteria_menu",
            description="충남대학교 교내 식당 식단을 조회합니다",
            parameters={
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "조회할 날짜 (today, tomorrow, YYYY-MM-DD)",
                        "default": "today"
                    },
                    "cafeteria": {
                        "type": "string",
                        "description": "식당명",
                        "enum": ["학생회관", "생활관", "교직원식당"],
                        "default": "학생회관"
                    }
                },
                "required": []
            }
        ),
        FunctionSchema(
            name="get_shuttle_general_time_table",
            description="충남대학교 셔틀버스의 일반적인 타임 테이블 정보를 조회합니다",
            parameters={
                "type": "object",
                "properties": {
                    "route": {
                        "type": "string",
                        "description": "노선",
                        "enum": ["all", "대전역", "유성온천역", "정부청사"],
                        "default": "all"
                    },
                    "time_type": {
                        "type": "string",
                        "description": "시간 유형",
                        "enum": ["current", "weekend", "holiday"],
                        "default": "current"
                    }
                },
                "required": []
            }
        ),
        FunctionSchema(
            name="search_cnu_site",
            description="충남대학교 사이트에서 검색합니다",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "검색 쿼리"
                    },
                    "site": {
                        "type": "string",
                        "description": "검색할 사이트",
                        "enum": ["plus", "ai"],
                        "default": "plus"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "최대 결과 수",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["query"]
            }
        )
    ],
    implementations=dict(
        **FunctionCalling.DEFAULT.implementations,
        get_graduation_requirements=graduation.get_graduation_credits,
        get_all_departments_list=graduation.get_all_departments_list,
        get_cnu_notices=cnu.get_cnu_notices,
        get_academic_schedule=cnu.get_academic_schedule,
        get_cafeteria_menu=cnu.get_cafeteria_menu,
        get_shuttle_general_time_table=cnu.get_shuttle_general_time_table,
        search_cnu_site=cnu.search_cnu_site
    )
)
