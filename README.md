# 🏛️ 퍼블리카이 (PUBLIKAI)

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Astro-FF5D01?style=for-the-badge&logo=astro" alt="Astro"/>
</div>
<br><br>
<div align="center">
  <h3>🌟 정보 접근성 향상 및 민원 응대 부담 해소용 대시보드 통합형 공공기관 챗봇 시스템</h3>
  <p>공공기관의 시민 서비스 향상과 업무 효율성 증대를 위한 AI 기반 통합 솔루션입니다.</p>
  
  ### 📹 데모 영상
  > **📁 [`res/demo.mp4`](https://github.com/thisisthepy/PUBLIKAI/raw/refs/heads/develop/res/demo.mp4)
</div>

---

## 🎯 프로젝트 배경

이 프로젝트는 **툴콜링 최적화를 위한 [Gemstone AI](https://github.com/thisisthepy/Gemstone) 레포지토리**를 fork하여 구현되었습니다. 

### 🏛️ 천안시 도시재생지원센터 챗봇 시스템 Design Thinking 프로젝트

**대시보드 AI Agent를 만드는 AI Agent 시스템**을 구상하였으나, 시간 제약으로 인해 완전한 구현에는 도달하지 못했습니다.

#### 📊 문제 정의 (Define)
- **POV 1**: 바쁜 직장인 시민들이 도시재생사업 정보에 쉽고 빠르게 접근하고 싶어하지만, 정보가 분산되어 있고 실시간 문의가 어려운 상황
- **POV 2**: 도시재생지원센터 직원들이 전문적인 기획업무에 집중하고 싶어하지만, 반복적인 민원 응답으로 핵심 업무 시간이 부족한 상황

#### 💡 핵심 해결 과제 (HMW)
- 시민들이 24시간 언제든지 필요한 정보를 얻을 수 있게 하기
- 반복적인 민원 응답을 자동화하기
- 시민과 기관 간의 양방향 소통을 활성화하기

#### 🏗️ 최종 솔루션
**"정보 접근성 향상 및 민원 응대 부담 해소용 대시보드 통합형 공공기관 챗봇 시스템"**

### 📋 대시보드 구성 계획
**기본 섹션 (7개)**
- Main 랜딩 페이지: 기관 간단 소개
- Introduction 페이지: 기관 소개, 진행하는 행사 목록 및 일정
- 시민 참여형 페이지: 민원 접수, 행사 참여 신청
- 월별 기관 실적 분석: 월간 성과 지표 및 트렌드
- 년도별 기관 실적 분석: 연간 성과 비교 및 분석
- 사례 소개: 성공 사례 및 Before/After
- 기타 자료 목록: 다운로드 가능한 문서 및 자료

**추가 확장 섹션 (5개)**
- 실시간 현황 모니터링: 진행 중인 사업 현황 맵
- 시민 소통 허브: 의견 수렴 및 투표 시스템, Q&A 게시판 (챗봇 연동)

---

## ✨ 주요 기능

- �️ **공공기관 특화** - 민원, 사업정보, 공지사항 등 공공기관 업무에 특화된 AI 챗봇
- 🎯 **맞춤형 응답** - 기관별 맞춤형 정보 제공 및 민원 안내
- 📊 **통합 대시보드** - 실시간 모니터링 및 관리 기능
- 💾 **로컬 AI 처리** - 개인정보 보호를 위한 온디바이스 AI 모델 지원
- 🔄 **실시간 통신** - WebSocket 기반 실시간 채팅
- 🌐 **웹 기반 인터페이스** - 별도 설치 없이 웹 브라우저에서 바로 사용

## 🛠️ 기술 스택

### 🖥️ 백엔드 (AI 모델 서버)
- **FastAPI** - 고성능 웹 API 프레임워크
- **Transformers & PyTorch** - 트랜스포머 모델 서빙 (INT4/INT8 양자화)
- **Llama-cpp-python** - GGUF 모델 서빙
- **BitsAndBytes** - 메모리 효율적인 모델 양자화

### 🌐 프론트엔드 (관리 대시보드)
- **Astro** - 정적 사이트 생성기
- **Tailwind CSS** - 유틸리티 우선 CSS 프레임워크
- **Flowbite** - Tailwind CSS 컴포넌트 라이브러리

### 🔒 개인정보 보호 고려사항
- **외부 AI API 사용 제한**: 개인정보 이슈로 인해 외부 인공지능 API 사용 불가
- **채팅 기록 비저장**: 사용자와의 채팅 내역 저장하지 않음

## 🤖 지원 모델
- **KT Mi:dm 2.0 Base** (11.5B 4bitQ Instruct) - 한국어 특화 대화형 AI 모델

### ⚡ 성능 최적화 및 제약사항
- **하드웨어 제약**: 낮은 공공기관 PC 사양으로 인한 로컬 LLM 추론 한계 => 온디바이스로 서빙은 불가능
- **배포 해결방안**: Hugging Face Space Pro 요금제 활용 (Sleep 모드 지원, 고정 요금)

## � 주요 기능 모듈

### 📋 공공기관 특화 기능
- **사업정보 조회** (`api/functions/business.py`) - 지원사업, 보조금 정보
- **공지사항 안내** (`api/functions/notice.py`) - 최신 공지사항 및 정책 변경사항
- **민원 안내** (`api/functions/info.py`) - 민원 접수 절차 및 문의사항
- **프로그램 정보** (`api/functions/program.py`) - 교육, 행사 프로그램 안내
- **관광정보** (`api/functions/tour.py`) - 지역 관광 정보 제공
- **뉴스 브리핑** (`api/functions/news.py`) - 기관 관련 뉴스 요약

### 🛠️ 유틸리티 기능
- **날씨 정보** (`api/utils/weather.py`) - 실시간 기상 정보
- **환율 정보** (`api/utils/currency.py`) - 실시간 환율 조회
- **일정 관리** (`api/utils/calendar.py`) - 공공기관 일정 안내
- **계산기** (`api/utils/calculator.py`) - 각종 계산 기능
- **웹 검색** (`api/utils/web_search.py`) - 실시간 정보 검색

## 📖 API 사용 예시

```json
{
  "role": "user",
  "content": "대전시 창업지원 사업에 대해 알려주세요"
}
```

**응답 예시:**
```json
{
  "role": "assistant", 
  "content": "대전시에서 제공하는 창업지원 사업을 안내해드리겠습니다.\n\n� **주요 창업지원 사업**\n- 청년창업지원센터 운영\n- 스타트업 보육 프로그램\n- 창업자금 융자 지원\n- 멘토링 및 컨설팅 서비스\n\n� **신청 방법**\n1. 대전시 홈페이지 접속\n2. 창업지원 메뉴 선택\n3. 온라인 신청서 작성\n4. 필요 서류 첨부\n\n자세한 내용은 대전시청 경제진흥과(☎ 042-270-xxxx)로 문의해주세요."
}
```

## 🏗️ 시스템 아키텍처

퍼블리카이는 **공공기관 홈페이지에 쉽게 통합 가능한 형태**로 설계되었으며, 개인정보 보호와 관리 편의성을 고려한 모듈형 아키텍처를 기반으로 합니다:

```
📁 PUBLIKAI/
├── 🎯 api/                  # AI 모델 서버 및 API
│   ├── models/             # AI 모델 관리
│   ├── functions/          # 공공기관 특화 기능
│   ├── utils/              # 유틸리티 기능
│   └── settings.py         # 시스템 설정
├── 📊 dashboard/           # 관리자 대시보드
│   ├── components/         # UI 컴포넌트
│   ├── modules/            # 기능 모듈
│   ├── pages/              # 페이지 라우팅
│   └── services/           # 데이터 서비스
├── 📄 data/                # 샘플 데이터 및 문서 (JSON 형태)
│   └── pdf/               # 벡터 DB 임베딩용 PDF 문서
└── 🚀 app.py               # 메인 애플리케이션
```

### � 데이터 파이프라인 설계
- **데이터 처리**: 기관에서 모든 데이터 가공 및 분석을 담당하고, 대시보드는 분석 완료된 결과만 표시
- **데이터 저장**: DB 대신 **JSON 형태로 데이터 관리**하여 기관에서 쉽게 관리 가능
- **GitHub Template 제공**: 코드 clone 없이 GitHub에서 직접 데이터 수정 가능
- **벡터 DB 자동화**: PDF 문서를 data/pdf 폴더에 저장하면 시작 시 자동으로 임베딩 진행

### 🔄 데이터 플로우
1. **사용자 입력** → 웹 인터페이스 또는 API
2. **요청 처리** → FastAPI 라우터
3. **AI 모델 추론** → 로컬 또는 클라우드 모델
4. **기능 실행** → 공공기관 특화 함수 호출
5. **응답 반환** → 구조화된 JSON 응답

### 🌐 배포 전략
**Hugging Face Space (ZeroGPU) 활용**
- **문제**: 기존 공공기관 PC 사양으로는 LLM 추론 불가능
- **해결**: HF Space Pro 요금제 사용
  - 사용하지 않을 때 자동 Sleep 모드
  - 고정 월 요금제로 비용 효율성 확보
  - GPU 서버 대비 안정적인 서비스 운영

## 🚀 설치 및 실행

### 📋 필요 조건
- **Python 3.12+**
- **Git**
- **Node.js 18+** (대시보드 사용 시)
- **CUDA 호환 GPU** (선택사항, GPU 가속용)

### 🔧 설치 방법

#### 1️⃣ 저장소 복제
```bash
git clone https://github.com/thisisthepy/PUBLIKAI.git
cd PUBLIKAI
```

#### 2️⃣ Python 의존성 설치
```bash
uv sync
```

### � 실행 방법

#### 메인 AI 챗봇 서버 실행
```bash
npm run build
python app.py
```

#### 대시보드 개발 서버 실행
```bash
npm install
npm run dev
```

### 🏛️ 기관별 커스터마이징
`api/system.py`에서 시스템 프롬프트 및 환영 메시지 수정:
```python
system_prompt = """
당신은 [기관명]의 AI 어시스턴트입니다.
시민들의 문의사항에 친절하고 정확하게 답변해주세요.
"""

welcome_message = """
안녕하세요! [기관명] AI 어시스턴트입니다. 
무엇을 도와드릴까요?
"""
```

---


## 🏗️ 프로젝트 현황 및 향후 계획

### ✅ 완성된 기능
- 기본 AI 챗봇 시스템 (Tool Calling 지원)
- 공공기관 특화 기능 모듈 (민원, 사업정보, 공지사항 등)

### 🚧 미완성 및 개선 필요 사항
- **대시보드 유지보수용 AI Agent 시스템**: 시간 제약으로 완전한 구현 미완료
- **LoRA 기반 2Bit 모델 최적화**: Tool Calling 능력 복구를 위한 RULER Training 필요

### 🎯 향후 개발 계획
1. **AI Agent 시스템 완성**: AI 챗봇 대시보드를 자동으로 생성하는 Meta-AI Agent 구현
2. **모델 최적화**: KT Intelligence와 협력하여 경량화 모델 Tool Calling 능력 개선
3. **확장 기능 개발**: 실시간 현황 모니터링 및 시민 참여 기능
4. **GitHub Template 완성**: 다른 공공기관이 쉽게 사용할 수 있는 템플릿 제공

## 🤝 기여하기

퍼블리카이 프로젝트에 기여해주셔서 감사합니다!

### 🐛 버그 리포트
- [이슈 트래커](https://github.com/thisisthepy/PUBLIKAI/issues) 사용
- 재현 가능한 상세한 설명 제공
- 플랫폼 및 버전 정보 포함

### 💡 기능 제안
- 기존 [기능 요청](https://github.com/thisisthepy/PUBLIKAI/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement) 확인
- 명확한 사용 사례와 함께 새로운 아이디어 제안
- 구현 복잡도 고려

### 🔧 개발 기여
1. 저장소 포크
2. 기능 브랜치 생성 (`git checkout -b feature/AmazingFeature`)
3. 변경사항 커밋 (`git commit -m 'Add some AmazingFeature'`)
4. 브랜치에 푸시 (`git push origin feature/AmazingFeature`)
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE.md) 파일을 참조하세요.

## 🙏 감사의 말

- **[Gemstone AI](https://github.com/thisisthepy/Gemstone)** - 툴콜링 최적화 기반 코드 제공
- **Hugging Face** - Transformers 라이브러리 및 Space 플랫폼 제공
- **Llama.cpp** - 효율적인 로컬 모델 서빙
- **FastAPI** - 고성능 웹 프레임워크
- **Astro & Flowbite** - 현대적인 웹 인터페이스
- **KT Intelligence** - Mi:dm 2.0 모델 제공
- **천안시 도시재생지원센터** - 실제 사용 사례 및 요구사항 제공

---

<div align="center">
  <p><strong>�️ 공공기관의 디지털 혁신을 함께 만들어갑니다!</strong></p>
  <p>
    <a href="https://github.com/thisisthepy/PUBLIKAI/issues">🐛 버그 신고</a> |
    <a href="https://github.com/thisisthepy/PUBLIKAI/discussions">💬 토론 참여</a> |
    <a href="https://github.com/thisisthepy/PUBLIKAI">⭐ GitHub 스타</a>
  </p>
</div>
