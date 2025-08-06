from ..utils import FunctionCalling, FunctionSchema
from . import info, work, notice, program, tour, news


PublikaiFunctions = FunctionCalling(
    schemas=[
        FunctionSchema(
            name="get_center_information",
            description="센터의 연락처(전화번호 등)와 위치 정보를 조회합니다",
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
            name="get_work_information",
            description="센터의 도시재생사업 정보를 조회합니다",
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
            name="get_general_notices",
            description="최신 공지사항을 조회하거나 키워드로 검색합니다",
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
            name="get_program_information",
            description="센터의 시민 참여형 프로그램 정보를 조회합니다 (진행중/진행완료 모두 포함)",
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
            description="센터에서 운영하는 도시재생 투어 정보(코스, 신청 방식)를 조회합니다",
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
        )
    ] + FunctionCalling.DEFAULT.schemas,
    implementations=dict(
        get_center_information=info.get_center_information,
        get_work_information=work.get_work_information,
        get_general_notices=notice.get_general_notices,
        get_program_information=program.get_program_information,
        get_tour_information=tour.get_tour_information,
        get_center_news=news.get_center_news,
        **FunctionCalling.DEFAULT.implementations
    )
)
