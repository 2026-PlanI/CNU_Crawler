import csv
import json
import requests
import time


def generate_metadata_from_ollama(title: str, content: str) -> str:
    """Ollama API를 호출하여 본문에서 메타데이터를 JSON 형태로 추출합니다."""

    ollama_url = "http://localhost:11434/api/generate"
    model_name = "llama3"

    prompt = f"""
당신은 대학교 학사 및 공지사항 데이터를 분류하는 AI 도우미입니다.
주어진 공지의 제목과 본문을 읽고, RAG 시스템의 검색 필터로 사용할 수 있도록 아래 JSON 형식으로만 정확히 출력하세요. 
설명이나 인사말은 절대 추가하지 마세요.

[JSON 출력 형식]
{{
    "target_major": "관련 학과 (언급이 없으면 '전체')",
    "activity_type": "유형 (공모전, 인턴십, 특강, 일반공지 중 택 1)",
    "summary": "이 공지의 핵심 내용을 학생이 읽기 좋게 1줄로 요약"
}}

[공고 정보]
제목: {title}
본문: {content[:1000]}  # 너무 긴 본문은 LLM 토큰을 위해 자름

[JSON 결과]:
"""

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "format": "json"  # JSON 형태로만 대답하도록 강제
    }

    try:
        response = requests.post(ollama_url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "{}").strip()
    except Exception as e:
        print(f"Ollama 통신 에러: {e}")
        return "{}"


def process_csv_with_llm():
    input_csv = "cnu_cs_project_notices.csv"
    output_csv = "cnu_cs_notices_with_metadata.csv"

    print(f"[{input_csv}] 파일을 읽어 LLM 분석을 시작합니다...\n")

    try:
        with open(input_csv, mode='r', encoding='utf-8-sig') as infile, \
                open(output_csv, mode='w', encoding='utf-8-sig', newline='') as outfile:

            reader = csv.DictReader(infile)

            # 기존 필드에 'Metadata' 필드를 추가해서 새 CSV 저장
            fieldnames = reader.fieldnames + ["Metadata"]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for i, row in enumerate(reader, 1):
                title = row['Title']
                content = row['Content']

                print(f"[{i}] LLM 분석 중: {title[:25]}...")

                # LLM에게 메타데이터 추출 요청
                metadata_json_str = generate_metadata_from_ollama(title, content)

                # 원본 데이터에 LLM 결과 추가
                row['Metadata'] = metadata_json_str

                # 새로운 CSV에 쓰기
                writer.writerow(row)

                # LLM 서버 과부하 방지 (로컬 GPU 성능에 따라 조절)
                time.sleep(0.5)

        print(f"[{output_csv}] 파일이 생성되었습니다.")

    except FileNotFoundError:
        print(f"에러: [{input_csv}] 파일이 없습니다. 크롤링 코드를 먼저 실행해 주세요.")


if __name__ == "__main__":
    process_csv_with_llm()
