## **소양강문화제 QR 스탬프 랠리 시스템: 최종 기술 구현 명세서 (v2.0)**

### **1\. 프로젝트 개요 (Overview)**

* **프로젝트명:** 소양강문화제 QR 스탬프 랠리 시스템  
* **목표:** 소양강문화제 방문객의 체험부스 참여를 디지털 방식으로 유도하고, 데이터를 기반으로 공정한 경품 지급 및 행사 운영 효율화를 달성한다.  
* **최종 기술 스택:**  
  * **프론트엔드:** **React** (Create React App 또는 Vite 기반의 SPA)  
  * **백엔드:** **Django** (Django REST Framework 포함)  
  * **데이터베이스:** **PostgreSQL**

### **2\. 시스템 아키텍처 (System Architecture)**

시스템은 클라이언트(React), 백엔드 서버(Django), 데이터베이스(PostgreSQL)의 3-tier 아키텍처로 구성됩니다.

\+----------------+      (HTTPS)       \+---------------------+      (API)       \+---------------------+  
|                | \<----------------\> |                     | \<--------------\> |                     |  
|  Client        |      (API Call,    |    Backend Server   |   (DB Query)   |    PostgreSQL DB    |  
| (React App on   |   Display Status)  |       (Django)      |                |                     |  
| User's Phone)  |                    |                     |                | (Booths,            |  
|                | \-----------------\> |  \- API Logic (DRF)  | \---------------\> |  Participants,      |  
\+----------------+      (API Call)     |  \- Admin Site       |                |  Stamps tables)     |  
                                       |                     |                |                     |  
\+----------------+                     \+---------------------+                \+---------------------+  
|                |  
|  Admin         |  
| (Django Admin) |  
|                |  
\+----------------+

1. **클라이언트 (Client):** 방문객의 스마트폰 브라우저에서 React로 구현된 SPA(싱글 페이지 애플리케이션)가 실행됩니다.  
2. **백엔드 서버 (Backend Server):** Django를 기반으로 구축됩니다. \*\*Django REST Framework(DRF)\*\*를 사용하여 참여자용 API를 제공하고, \*\*Django의 내장 관리자 사이트(Admin Site)\*\*를 활용하여 운영진에게 강력한 관리 기능을 제공합니다.  
3. **데이터베이스 (Database):** PostgreSQL을 사용하여 모든 데이터를 영구적으로 저장하고 관리합니다.

### **3\. 데이터베이스 스키마 (Database Schema \- PostgreSQL)**

models.py에 정의될 Django 모델의 최종 스키마입니다.

#### **booths \- 체험부스 정보**

| Field Name | Django Field Type | Options & Description |
| :---- | :---- | :---- |
| id | UUIDField | primary\_key=True, default=uuid.uuid4 (부스 고유 ID) |
| name | CharField(max\_length=100) | unique=True, verbose\_name="부스 이름" |
| is\_active | BooleanField | default=True, verbose\_name="활성화 여부" (Soft Delete용) |
| created\_at | DateTimeField | auto\_now\_add=True, verbose\_name="생성 시각" |

#### **participants \- 참여자 정보**

| Field Name | Django Field Type | Options & Description |
| :---- | :---- | :---- |
| id | UUIDField | primary\_key=True, default=uuid.uuid4 (참여자 고유 ID) |
| nickname | CharField(max\_length=50) | unique=True, verbose\_name="닉네임" |
| created\_at | DateTimeField | auto\_now\_add=True, verbose\_name="생성 시각" |

#### **stamps \- 스탬프 획득 기록**

| Field Name | Django Field Type | Options & Description |
| :---- | :---- | :---- |
| id | AutoField | primary\_key=True (기록 순번 ID) |
| participant | ForeignKey | to='participants', on\_delete=models.CASCADE (참여자) |
| booth | ForeignKey | to='booths', on\_delete=models.CASCADE (부스) |
| created\_at | DateTimeField | auto\_now\_add=True, verbose\_name="획득 시각" |
| (Meta) | (UniqueConstraint) | fields=\['participant', 'booth'\] (중복 스캔 방지) |

### **4\. 주요 기능 및 흐름 (Key Features & Flow)**

#### **참여자 흐름 (React SPA)**

1. **QR 스캔:** 체험부스의 QR 코드를 스캔하여 https://\<도메인\>/?boothId=\<부스ID\> 형태의 URL에 접속합니다.  
2. **최초 참여:** localStorage에 참여자 ID가 없으면, 닉네임 입력 화면이 나타납니다. 닉네임 입력 후 참여자 ID가 발급되어 localStorage에 저장됩니다.  
3. **스탬프 획득:** 시스템이 URL의 boothId와 localStorage의 participant\_id를 서버로 전송하여 스탬프를 기록합니다.  
4. **현황 확인:** 화면에 현재까지 모은 스탬프 개수(예: 🔵🔵🔵⚪️⚪️ 3/5)가 실시간으로 표시됩니다.  
5. **미션 완료:** 서로 다른 부스 5개의 스탬프를 모두 모으면, "미션 완료\! 경품 지급처로 가세요" 와 같은 완료 페이지가 나타납니다.

#### **관리자 흐름 (Django Admin Site)**

**별도의 관리자 페이지 개발 없이, Django의 강력한 내장 Admin을 최대한 활용합니다.**

1. **로그인:** 운영진은 /admin URL로 접속하여 사전에 발급된 아이디와 비밀번호로 로그인합니다.  
2. **부스 관리:**  
   * **추가:** \[Booths\] 메뉴에서 'Add booth' 버튼을 눌러 부스 이름만 입력하면 새로운 부스가 즉시 생성됩니다.  
   * **삭제(비활성화):** 부스 목록에서 비활성화할 부스의 '활성화 여부(Is active)' 체크박스를 해제하고 저장합니다.  
   * **QR 코드 확인:** 각 부스의 상세 페이지에서 QR 코드 생성을 위한 URL (https://\<도메인\>/?boothId=\<부스ID\>)을 확인할 수 있습니다.  
3. **참여자 검증:**  
   * \[Participants\] 메뉴의 검색창에서 참여자의 닉네임으로 검색합니다.  
   * 검색된 참여자의 상세 정보에서 스탬프 획득 내역을 직접 확인하여 경품 지급 여부를 결정합니다.  
4. **통계 확인:**  
   * Django Admin에 커스텀 뷰를 추가하여 간단한 대시보드를 만듭니다. 이 페이지에서는 전체 참여자 수, 미션 완료자 수, 부스별 스캔 횟수 순위 등 핵심 지표를 확인할 수 있습니다.

### **5\. API 엔드포인트 명세 (Django REST Framework)**

참여자용 React 앱과 통신하기 위한 API 명세입니다.

* **POST /api/participants/**  
  * **설명:** 신규 참여자 생성.  
  * **Request:** { "nickname": "춘천사는반달곰" }  
  * **Response (201):** { "id": "...", "nickname": "춘천사는반달곰" }  
* **GET /api/participants/\<uuid:id\>/**  
  * **설명:** 특정 참여자의 현재 스탬프 현황 조회.  
  * **Response (200):** { "id": "...", "nickname": "...", "stamps": \[ { "booth\_name": "부스이름1" }, ... \] }  
* **POST /api/stamps/**  
  * **설명:** 스탬프 획득 기록 생성.  
  * **Request:** { "participant\_id": "...", "booth\_id": "..." }  
  * **Response (201):** { "status": "success", "total\_stamps": 3 }  
* **GET /api/admin/stats/**  
  * **설명:** 관리자 대시보드용 통계 데이터 제공.  
  * **Response (200):** { "total\_participants": ..., "total\_completions": ..., "booth\_popularity": \[ ... \] }

### **6\. 프론트엔드 명세 (React)**

* **타입:** 순수 클라이언트 사이드 렌더링(CSR) 기반의 싱글 페이지 애플리케이션(SPA).  
* **개발 도구:** Vite 또는 Create React App 사용.  
* **주요 컴포넌트:**  
  * StampPage.js: 스탬프 현황을 보여주는 메인 페이지.  
  * NicknameForm.js: 최초 사용자에게 닉네임을 입력받는 컴포넌트.  
  * StampBoard.js: 스탬프 획득 상태를 시각적으로 보여주는 UI.  
  * CompletionModal.js: 미션 완료 시 나타나는 축하 및 안내 모달.  
  * AdminDashboard.js: (필요시) Django Admin 내에 삽입하거나 별도 페이지로 구성할 통계 대시보드. /api/admin/stats/ API를 호출하여 데이터를 시각화.

### **7\. 개발 환경 및 배포 (Dev Environment & Deployment)**

* **의존성 (Dependencies):**  
  * **Backend (Django):** django, djangorestframework, psycopg2-binary (PostgreSQL 드라이버), django-cors-headers (CORS 처리), qrcode (QR 생성).  
  * **Frontend (React):** react, react-dom, react-router-dom (라우팅), axios (API 통신).  
* **개발 환경:**  
  * 백엔드: python manage.py runserver 명령어로 Django 개발 서버 실행.  
  * 프론트엔드: npm start (또는 yarn start) 명령어로 React 개발 서버 실행.  
  * django-cors-headers를 설정하여 React 개발 서버(예: localhost:3000)에서의 API 요청을 허용해야 합니다.  
* **배포 전략 (Deployment):**  
  * **Frontend (React):** npm run build로 생성된 정적 파일들을 Vercel, Netlify 등 정적 호스팅 서비스에 배포하여 빠르고 안정적인 서비스를 제공합니다.  
  * **Backend (Django) & DB (PostgreSQL):** Heroku, AWS (Elastic Beanstalk \+ RDS), Google Cloud Platform (App Engine \+ Cloud SQL) 등 Python/Django와 PostgreSQL을 지원하는 관리형 클라우드 서비스를 활용하여 서버 및 데이터베이스를 배포하고 운영합니다.