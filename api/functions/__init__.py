from ..utils import FunctionCalling, FunctionSchema
from . import info, business, notice, program, tour, news


PublikaiFunctions = FunctionCalling(
    schemas=[
        FunctionSchema(
            name="get_center_information",
            description="센터의 전화번호와 위치 정보 등 기본 사항을 조회합니다",
            parameters={
                "type": "object",
                "properties": {
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
            name="get_business_information",
            description="센터에서 진행중인 도시재생사업의 현황, 추진 단계, 예산 정보를 조회합니다 (진행중/진행완료 모두 포함) | 키워드: 사업현황, 추진상황, 계획, 예산",
            parameters={
                "type": "object",
                "properties": {
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
            name="get_center_notices",
            description="센터의 최신 공지사항을 조회하거나 키워드로 검색합니다",
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "검색 키워드 (검색 쿼리가 없으면 최신 공지사항을 조회합니다)",
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
            name="get_upcoming_programs",
            description="다가오는 시민들이 참여형 교육, 워크샵, 체험 프로그램의 일정과 신청 방법을 조회합니다 | 키워드: 프로그램, 교육, 참여, 워크샵",
            parameters={
                "type": "object",
                "properties": {
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
            name="get_program_history",
            description="센터에서 진행한 프로그램들의 이력들을 조회합니다 (진행중/진행완료 모두 포함) | 키워드: 프로그램, 교육, 참여, 워크샵",
            parameters={
                "type": "object",
                "properties": {
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
            name="get_tour_information",
            description="센터에서 운영하는 `도시재생 투어 정보`(코스, 신청 방식)를 조회합니다",
            parameters={
                "type": "object",
                "properties": {
                },
                "required": []
            }
        ),
        FunctionSchema(
            name="get_center_news",
            description="센터의 도시재생 관련 발간물 및 뉴스를 조회합니다",
            parameters={
                "type": "object",
                "properties": {
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
            name="navigate_to_dashboard",
            description="현재 유저가 보고 있는 대시보드 페이지를 이동시킵니다",
            parameters={
                "type": "object",
                "properties": {
                    "section": {
                        "type": "string",
                        "description": "이동할 대시보드 섹션 이름 (예: '#welcome', '#introduction', '#participation', '#monthly', '#yearly')"
                    }
                },
                "required": ["section"]
            }
        )
    ] + FunctionCalling.DEFAULT.schemas,
    implementations=dict(
        get_center_information=info.get_center_information,
        get_business_information=business.get_business_information,
        get_center_notices=notice.get_center_notices,
        get_upcoming_programs=program.get_upcoming_programs,
        get_program_history=program.get_program_history,
        get_tour_information=tour.get_tour_information,
        get_center_news=news.get_center_news,
        navigate_to_dashboard=lambda section: None,
        **FunctionCalling.DEFAULT.implementations
    )
)
