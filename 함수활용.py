import func

def main():
    print("==========================")
    print("| 1. 멜론 차트 TOP 100곡  |")
    print("| 2. 멜론 차트 TOP 50곡   |")
    print("| 3. 멜론 차트 TOP 10곡   |")
    print("| 4. 멜론 원하는 차트     |")
    print("| 5. 멜론 차트 AI 추천곡  |")
    print("==========================")

    n = input("[원하는 번호를 입력하세요]: ")
    print(f"당신이 입력한 번호는? {n}")

    match n:
        case "1":
            func.m100("멜론 TOP 100곡")
        case "2":
            func.m50("멜론 TOP 50곡")
        case "3":
            func.m10("멜론 10곡")
        case "4":
            count = int(input("몇 곡을 출력할까요? (예: 5): "))
            func.m000("멜론 원하는 차트", count)
        case "5":
            func.m_random("멜론 차트 AI 추천곡")
        case _:
            print("올바른 번호를 입력하세요 (1~5)")

if __name__ == "__main__":
    main()
