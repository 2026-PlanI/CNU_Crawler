import requests
from bs4 import BeautifulSoup
import urllib3

# SSL 인증서 경고 메시지 숨기기
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_cnu_html():
    # 충남대학교 메인 공지사항 (사업단 소식) URL 예시
    # 원하는 홈페이지로 변경하시면 됩니다.
    url = "https://computer.cnu.ac.kr/computer/notice/project.do"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        print(f"[{url}] 에 접속 시도 중...")
        response = requests.get(url, headers=headers, verify=False)
        response.encoding = 'utf-8'
        response.raise_for_status()

        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        print("\n--- 사이트 기본 정보 ---")
        print(f"페이지 제목: {soup.title.text if soup.title else '제목 없음'}")

        # 전체 HTML을 눈으로 보기 편하게 파일로 저장
        file_name = "cnu_notice_test.html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(soup.prettify())

    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    check_cnu_html()
