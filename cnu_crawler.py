import requests
from bs4 import BeautifulSoup
import urllib3
import csv
import time

# SSL 인증서 경고 메시지 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def scrape_cnu_cs_to_csv():
    # 컴공과 사업단소식 기본 URL
    base_url = "https://computer.cnu.ac.kr/computer/notice/project.do"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
    }

    print("1. 게시판 공지 링크들을 수집합니다...")

    # --- [1단계] 게시판 목록 접속 ---
    response = requests.get(base_url, headers=headers, verify=False)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # HTML 구조에서 제목과 링크가 있는 <a> 태그들 모두 찾기
    notice_links = soup.select('.b-title-box a')

    if not notice_links:
        print("공지사항을 찾을 수 없습니다.")
        return

    print(f"총 {len(notice_links)}개의 공지사항을 찾았습니다. 본문 수집을 시작합니다!\n")

    # 긁어온 데이터를 담을 빈 리스트
    data_list = []

    # --- [2단계] 반복문을 돌며 개별 본문 긁어오기 ---
    for i, link_tag in enumerate(notice_links, 1):
        title = link_tag.text.strip()
        raw_href = link_tag.get('href')

        # 상세 페이지 주소 완성
        detail_url = f"{base_url}{raw_href}"

        print(f"[{i}/{len(notice_links)}] 긁어오는 중: {title[:20]}...")

        # 상세 페이지 접속
        detail_res = requests.get(detail_url, headers=headers, verify=False)
        detail_res.encoding = 'utf-8'
        detail_soup = BeautifulSoup(detail_res.text, 'html.parser')

        # 본문 영역 찾기
        content_area = detail_soup.select_one('.b-content-box') or detail_soup.select_one(
            '.b-con-box') or detail_soup.select_one('#jwxe_main_content')

        clean_text = ""
        if content_area:
            # 불필요한 스크립트, 스타일 날려버리기
            for script_or_style in content_area(["script", "style"]):
                script_or_style.decompose()

            # 텍스트만 추출해서 빈 줄 제거
            raw_text = content_area.get_text(separator='\n')
            clean_text = '\n'.join([line.strip() for line in raw_text.split('\n') if line.strip()])

        # 딕셔너리 형태로 리스트에 차곡차곡 저장
        data_list.append({
            "Title": title,
            "URL": detail_url,
            "Content": clean_text
        })

        time.sleep(1)

    print("\n2. 수집된 데이터를 CSV 파일로 저장합니다...")

    # --- [3단계] CSV 파일로 저장하기 ---
    csv_filename = "cnu_cs_project_notices.csv"

    # 엑셀에서 열 때 한글 깨짐을 막기 위해 'utf-8-sig' 사용
    with open(csv_filename, mode='w', encoding='utf-8-sig', newline='') as f:
        fieldnames = ["Title", "URL", "Content"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()  # 1번째 줄에 헤더(열 이름) 쓰기
        writer.writerows(data_list)  # 2번째 줄부터 데이터 한 번에 쓰기

    print(f"\n작업 완료! 현재 폴더에 [{csv_filename}] 파일 생성")


if __name__ == "__main__":
    scrape_cnu_cs_to_csv()
