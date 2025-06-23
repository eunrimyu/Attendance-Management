import sys
import pygame
from datetime import datetime

def start():
    pygame.init()
    screen_width = 1200
    screen_height = 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("출결 시스템")

    # 상명대 이미지
    img_smu = pygame.image.load("img/smu.jpg") #802x680
    img_smu_width = img_smu.get_rect().size[0]
    img_smu_height = img_smu.get_rect().size[1]
    smu_width = img_smu_width/3
    smu_height = img_smu_height/3
    smu = pygame.transform.scale(img_smu, (smu_width,smu_height))

    # 현재 날짜
    current_date = datetime.now().date()

    # 입력 상자
    box_height = 30
    
    input_class = ""
    input_class_box_rect = pygame.Rect((screen_width - smu_width)/2, (screen_height)/2 + 17, smu_width, box_height)
    active_input_class_box = False

    input_name = ""
    input_name_box_rect = pygame.Rect((screen_width - smu_width)/2, (screen_height)/2 + 45, smu_width, box_height)
    active_input_name_box = False

    input_starttime = ""
    input_starttime_box_rect = pygame.Rect((screen_width - smu_width)/2, (screen_height)/2 + 73, smu_width/2 + 2, box_height)
    active_input_starttime_box = False

    input_endtime = ""
    input_endtime_box_rect = pygame.Rect((screen_width)/2-1, (screen_height)/2 + 73, smu_width/2 + 1, box_height)
    active_input_endtime_box = False

    # 버튼
    start_button_rect = pygame.Rect((screen_width - smu_width)/2, (screen_height)/2 + 101, smu_width, box_height)

    waiting_for_start = True
    
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 마우스 클릭
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if start_button_rect.collidepoint(x, y):
                    print(input_class)
                    print(input_name)
                    print(input_starttime)
                    print(input_endtime)
                    # datetime 객체를 비교
                    if start_datetime < end_datetime:
                        print("시작 시간은 종료 시간보다 이전입니다.")
                    elif start_datetime == end_datetime:
                        print("시작 시간과 종료 시간이 동일합니다.")
                    else:
                        print("입력한 시간이 유효합니다.")
                    waiting_for_start = False
                elif input_class_box_rect.collidepoint(x, y):
                    active_input_class_box = not active_input_class_box
                    active_input_name_box = False
                    active_input_starttime_box = False
                    active_input_endtime_box = False
                elif input_name_box_rect.collidepoint(x, y):
                    active_input_name_box = not active_input_name_box
                    active_input_class_box = False
                    active_input_starttime_box = False
                    active_input_endtime_box = False
                elif input_starttime_box_rect.collidepoint(x, y):
                    active_input_starttime_box = not active_input_starttime_box
                    active_input_name_box = False
                    active_input_class_box = False
                    active_input_endtime_box = False
                elif input_endtime_box_rect.collidepoint(x, y):
                    active_input_endtime_box = not active_input_endtime_box
                    active_input_name_box = False
                    active_input_class_box = False
                    active_input_starttime_box = False
                else:
                    active_input_class_box = False
                    active_input_name_box = False
                    active_input_starttime_box = False
                    active_input_endtime_box = False
            # 키보드 클릭
            elif event.type == pygame.KEYDOWN:
                if active_input_class_box:
                    if event.unicode.isalpha() or event.unicode.isdigit() or event.unicode.isspace():
                        input_class += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        input_class = input_class[:-1]
                elif active_input_name_box:
                    if event.unicode.isalpha() or event.unicode.isdigit() or event.unicode.isspace():
                        input_name += event.unicode
                    elif event.key == pygame.K_BACKSPACE:
                        input_name = input_name[:-1]
                elif active_input_starttime_box:
                    if event.key == pygame.K_RETURN:
                        try:
                            start_time = datetime.strptime(input_starttime, "%H:%M:%S").time()
                            start_datetime = datetime.combine(current_date, start_time)
                            print(start_datetime)
                        except ValueError:
                            print("시간을 HH:MM:SS 형식으로 입력하세요.")
                            input_starttime = ""
                            continue
                    elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        input_starttime += event.unicode
                    elif event.key == pygame.K_SEMICOLON and event.mod & pygame.KMOD_SHIFT:
                        input_starttime += ":"
                    elif event.key == pygame.K_BACKSPACE:
                        input_starttime = input_starttime[:-1]
                elif active_input_endtime_box:
                    if event.key == pygame.K_RETURN:
                        try:
                            end_time = datetime.strptime(input_endtime, "%H:%M:%S").time()
                            end_datetime = datetime.combine(current_date, end_time)
                            print(end_datetime)
                        except ValueError:
                            print("시간을 HH:MM:SS 형식으로 입력하세요.")
                            input_endtime = ""
                            continue
                    elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        input_endtime += event.unicode
                    elif event.key == pygame.K_SEMICOLON and event.mod & pygame.KMOD_SHIFT:
                        input_endtime += ":"
                    elif event.key == pygame.K_BACKSPACE:
                        input_endtime = input_endtime[:-1]

        screen.fill((255, 255, 255))

        # 상명대 로고
        screen.blit(smu, [(screen_width - smu_width)/2, (screen_height - smu_height)/2 - 100])

        # 입력 상자
        font_box = pygame.font.Font(None,25)
        input_font = pygame.font.Font(None, 28)

        class_text = font_box.render("Class name", True, (220, 220, 220))
        class_rect = class_text.get_rect(center=input_class_box_rect.center)
        screen.blit(class_text, class_rect)
        pygame.draw.rect(screen, (128, 128, 128), input_class_box_rect, 2)
        input_surface = input_font.render(input_class, True, (0, 0, 0))
        screen.blit(input_surface, (input_class_box_rect.x + 5, input_class_box_rect.y + 5))

        name_text = font_box.render("Professor name", True, (220, 220, 220))
        name_rect = name_text.get_rect(center=input_name_box_rect.center)
        screen.blit(name_text, name_rect)
        pygame.draw.rect(screen, (128, 128, 128), input_name_box_rect, 2)
        input_surface = input_font.render(input_name, True, (0, 0, 0))
        screen.blit(input_surface, (input_name_box_rect.x + 5, input_name_box_rect.y + 5))

        start_text = font_box.render("HH:MM:SS", True, (220, 220, 220))
        start_rect = start_text.get_rect(center=input_starttime_box_rect.center)
        screen.blit(start_text, start_rect)
        pygame.draw.rect(screen, (128, 128, 128), input_starttime_box_rect, 2)
        input_surface = input_font.render(input_starttime, True, (0, 0, 0))
        screen.blit(input_surface, (input_starttime_box_rect.x + 5, input_starttime_box_rect.y + 5))

        end_text = font_box.render("HH:MM:SS", True, (220, 220, 220))
        end_rect = end_text.get_rect(center=input_endtime_box_rect.center)
        screen.blit(end_text, end_rect)
        pygame.draw.rect(screen, (128, 128, 128), input_endtime_box_rect, 2)
        input_surface = input_font.render(input_endtime, True, (0, 0, 0))
        screen.blit(input_surface, (input_endtime_box_rect.x + 5, input_endtime_box_rect.y + 5))

        pygame.draw.rect(screen, (1, 74, 141), start_button_rect)
        button_text = font_box.render("CHECK", 1, (0, 0, 0))
        button_rect = button_text.get_rect(center=start_button_rect.center)
        screen.blit(button_text, button_rect)
        

        pygame.display.flip()   # 화면 업데이트

    # 파일에 데이터 저장
    with open("data.txt", "w") as file:
        file.write(f"{input_class}\n{input_name}\n{input_starttime}\n{input_endtime}")

    with open("data.txt", "r") as file:
        input_class = file.readline().strip()
        input_name = file.readline().strip()
        input_starttime = file.readline().strip()
        input_endtime = file.readline().strip()

    current_date = datetime.now().date()# 현재 날짜

    start_datetime = datetime.strptime(input_starttime, "%H:%M:%S").time()
    start_time = datetime.combine(current_date, start_datetime)

    end_datetime = datetime.strptime(input_endtime, "%H:%M:%S").time()
    end_time = datetime.combine(current_date, end_datetime)

    print(start_time)
    print(end_time)

    pygame.quit()
    return True  # 다음 파일 실행을 위한 플래그

if __name__ == "__main__":
    start()
