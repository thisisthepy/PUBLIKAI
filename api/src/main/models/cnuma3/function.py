from ...utils import FunctionCalling, FunctionSchema
from . import cnu


Cnuma3Functions = FunctionCalling(
    schemas=FunctionCalling.DEFAULT.schemas + [
        FunctionSchema(
            name="get_graduation_requirements",
            description="충남대학교 졸업요건 정보를 조회합니다",
            parameters={
                "type": "object",
                "properties": {
                    "department": {
                        "type": "string",
                        "description": "학과명 (예: 인공지능학과, 컴퓨터공학과)",
                        "default": "인공지능학과"
                    },
                    "degree_type": {
                        "type": "string",
                        "description": "학위 유형",
                        "enum": ["학사", "석사", "박사"],
                        "default": "학사"
                    }
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
        get_graduation_requirements=cnu.get_graduation_requirements,
        get_cnu_notices=cnu.get_cnu_notices,
        get_academic_schedule=cnu.get_academic_schedule,
        get_cafeteria_menu=cnu.get_cafeteria_menu,
        get_shuttle_general_time_table=cnu.get_shuttle_general_time_table,
        search_cnu_site=cnu.search_cnu_site
    )
)
